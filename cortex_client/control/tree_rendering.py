import os, pwd, grp

from cortex_client.util import path
from cortex_client.control.exceptions import ControllerException

class TreeRenderer(object):
    def __init__(self, api, org_name, env_name, host_name):
        self._api = api
        self._org_name = org_name
        self._env_name = env_name
        self._host_name = host_name

    def render(self, root_dir, skip_chmod, skip_chown):
        path.ensure(root_dir)

        org = self._api.organizations().get_resource(self._org_name)
        env = org.environments().get_resource(self._env_name)
        host = env.hosts().get_resource(self._host_name)

        apps = host.get_applications()
        for app_name in apps:
            # Get application from organization
            app = org.applications().get_resource(app_name)

            # Render files of app
            app_files = app.get_files()
            for f in app_files:
                file_path = f.get_path()
                if file_path[0] == '/':
                    rel_path = file_path[1:] # remove heading "/"
                else:
                    rel_path = file_path

                # Output rendered file
                (dir_path, file_name) = os.path.split(rel_path)
                output_dir = os.path.join(root_dir, dir_path)
                path.ensure(output_dir)
                output_file = os.path.join(output_dir, file_name)

                content = host.render_file(app_name, f.get_name())
                with open(output_file, "w") as fd:
                    fd.write(content.read())

                # Set permissions
                mode = int(f.get_mode(), 8)
                owner = f.get_owner()
                owner_id = pwd.getpwnam(owner)[2]
                group = f.get_group()
                group_id = grp.getgrnam(group)[2]

                if not skip_chmod:
                    try:
                        os.chmod(output_file, mode)
                    except OSError, e:
                        raise ControllerException("Could not set permissions on file " + output_file + ": " + e.strerror)

                if not skip_chown:
                    try:
                        os.chown(output_file, owner_id, group_id)
                    except OSError, e:
                        raise ControllerException("Could not set ownership on file " + output_file + ": " + e.strerror)
