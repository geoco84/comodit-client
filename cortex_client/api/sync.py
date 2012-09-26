import os, json, types, shutil

from cortex_client.control.exceptions import ControllerException
from sets import Set
from cortex_client.api.collection import ResourceNotFoundException

class SyncException(ControllerException):
    def __init__(self, msg):
        super(SyncException, self).__init__(msg)

class Diff(object):
    def __init__(self, diff_type, key, old_value = None, new_value = None):
        self.type = diff_type
        self.key = key
        self.old_value = old_value
        self.new_value = new_value

class LocalFileProvider(object):
    def __init__(self, folder):
        self._folder = folder

    def exists(self, name):
        return os.path.exists(os.path.join(self._folder, name))

    def open(self, name):
        return open(os.path.join(self._folder, name), "r")

    def close(self, fd):
        fd.close()

class RemoteFileProvider(object):
    def __init__(self, remote_res):
        self._remote_res = remote_res

    def exists(self, name):
        try:
            self._remote_res.files().get_resource(name).get_content()
            return True
        except ResourceNotFoundException:
            return False

    def open(self, name):
        return self._remote_res.files().get_resource(name).get_content()

    def close(self, fd):
        pass

class SyncEngine(object):
    def __init__(self, folder_path):
        if not os.path.exists(folder_path):
            raise SyncException("Provided folder does not exist")

        self._folder_path = folder_path
        self._files_folder_path = os.path.join(self._folder_path, "files")
        self._deffile_path = os.path.join(folder_path, "definition.json")
        if not os.path.exists(self._deffile_path):
            raise SyncException("Provided folder does not contain a resource definition")

        self.__push_ignored_fields = ["organization", "price", "version", "canPull", "canPush", "uuid", "publishedAs", "purchasedAs"]
        self.__pull_ignored_fields = []

    def __is_ignore(self, key, is_pull):
        return (is_pull and (key in self.__pull_ignored_fields)) or (not is_pull and (key in self.__push_ignored_fields))

    def _is_same_content(self, reader1, reader2, file_name):
        exists1 = reader1.exists(file_name)
        exists2 = reader2.exists(file_name)

        if exists1 != exists2:
            return False
        elif not exists1:
            return True

        fd1 = reader1.open(file_name)
        fd2 = reader2.open(file_name)

        is_same_content = fd1.read() == fd2.read()

        reader1.close(fd1)
        reader2.close(fd2)
        return is_same_content

    def _diff(self, src_dict, dest_dict, is_pull, src_reader, dest_reader):
        diffs = []
        for key, value in dest_dict.iteritems():
            if self.__is_ignore(key, is_pull):
                continue

            remote_value = src_dict.get(key)
            if remote_value is None:
                diffs.append(Diff("delete", key))
                if key == "files":
                    for f in remote_value:
                        diffs.append(Diff("delete_file_content", f["name"]))
            elif value != remote_value:
                diffs.append(Diff("update", key, value, remote_value))
                if key == "files":
                    local_names = Set()
                    for f in value:
                        local_names.add(f["name"])
                    remote_names = Set()
                    for f in remote_value:
                        remote_names.add(f["name"])

                    to_delete = local_names - remote_names
                    for file_name in to_delete:
                        diffs.append(Diff("delete_file_content", file_name))
                    to_create = remote_names - local_names
                    for file_name in to_create:
                        diffs.append(Diff("set_file_content", file_name))
                    common_files = local_names & remote_names
                    for file_name in common_files:
                        if not self._is_same_content(src_reader, dest_reader, file_name):
                            if src_reader.exists(file_name):
                                diffs.append(Diff("set_file_content", file_name))
                            else:
                                diffs.append(Diff("delete_file_content", file_name))
            elif key == "files":
                for f in value:
                    file_name = f["name"]
                    if not self._is_same_content(src_reader, dest_reader, file_name):
                        if src_reader.exists(file_name):
                            diffs.append(Diff("set_file_content", file_name))
                        else:
                            diffs.append(Diff("delete_file_content", file_name))

        for key, value in src_dict.iteritems():
            if self.__is_ignore(key, is_pull):
                continue
            local_value = dest_dict.get(key)
            if local_value is None:
                diffs.append(Diff("create", key, None, value))
                if key == "files":
                    for f in value:
                        diffs.append(Diff("set_file_content", f["name"]))

        return diffs

    def _print_diff(self, diffs):
        for d in diffs:
            if d.type == "delete":
                print "Deletion of field '" + d.key + "'"
            elif d.type == "create":
                print "Creation of field '" + d.key + "'"
            elif d.type == "update":
                if type(d.old_value) != type(d.new_value):
                    print "Conflicting types for field", d.key
                elif type(d.old_value) is types.DictType:
                    print "Conflicting values for field '" + d.key + "': different dicts"
                elif type(d.old_value) is types.ListType:
                    print "Conflicting values for field '" + d.key + "': different lists"
                else:
                    print "Conflicting values for field '" + d.key + "':", d.old_value, "->", d.new_value
            elif d.type == "delete_file_content":
                print "Deletion of file '" + d.key + "' content"
            elif d.type == "set_file_content":
                print "Creation/update of file '" + d.key + "' content"

    def _apply_pull_diff(self, diffs, local_dict, remote_res):
        files_dir = os.path.join(self._folder_path, "files")
        for d in diffs:
            if d.type == "delete_file_content":
                os.remove(os.path.join(files_dir, d.key))
            elif d.type == "set_file_content":
                content_reader = remote_res.files().get_resource(d.key).get_content()
                with open(os.path.join(files_dir, d.key), "w") as fd:
                    fd.write(content_reader.read())
        remote_res.dump(self._folder_path)

    def _apply_push_diff(self, diffs, local_dict, remote_res):
        remote_res.load(self._folder_path)

        # Delete handlers if any
        handlers = remote_res.get_json().get("handlers")
        if not handlers is None:
            remote_res.set_handlers([])
            remote_res.commit()
            # Reload local content
            remote_res.load(self._folder_path)

        # Reset sub-collections
        for d in diffs:
            if d.key == "files":
                if d.type == "delete" or d.type == "update":
                    # Delete all
                    for f in remote_res.files().get_resources():
                        f.delete()

                if d.type == "create" or d.type == "update":
                    # (Re)-create all
                    for f in remote_res.get_files():
                        new_file = remote_res.files()._new_resource(f.get_json())
                        new_file.create()

            if d.key == "parameters":
                if d.type == "delete" or d.type == "update":
                    # Delete all
                    for p in remote_res.parameters().get_resources():
                        p.delete()

                if d.type == "create" or d.type == "update":
                    # (Re)-create all
                    for p in remote_res.get_parameters():
                        new_param = remote_res.parameters()._new_resource(p.get_json())
                        new_param.create()

            if d.key == "settings":
                if d.type == "delete" or d.type == "update":
                    # Delete all
                    for s in remote_res.settings().get_resources():
                        s.delete()

                if d.type == "create" or d.type == "update":
                    # (Re)-create all
                    for s in remote_res.get_settings():
                        new_set = remote_res.settings()._new_resource(s.get_json())
                        new_set.create()

        # Reset file contents
        for d in diffs:
            if d.type == "set_file_content":
                content_path = os.path.join(self._folder_path, "files", d.key)
                if os.path.exists(content_path):
                    remote_res.files().get_resource(d.key).set_content(content_path)

        # Update remaining fields
        remote_res.commit()

    def pull(self, remote_res, dry_run = False):
        remote_json = remote_res.get_json()
        local_json = json.load(open(self._deffile_path, "r"))

        diffs = self._diff(remote_json, local_json, True, RemoteFileProvider(remote_res), LocalFileProvider(self._files_folder_path))
        if dry_run:
            self._print_diff(diffs)
        else:
            self._apply_pull_diff(diffs, local_json, remote_res)

    def push(self, remote_res, dry_run = False):
        remote_json = remote_res.get_json()
        local_json = json.load(open(self._deffile_path, "r"))

        diffs = self._diff(local_json, remote_json, False, LocalFileProvider(self._files_folder_path), RemoteFileProvider(remote_res))
        if dry_run:
            self._print_diff(diffs)
        else:
            self._apply_push_diff(diffs, local_json, remote_res)
