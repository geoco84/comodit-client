import re

from cortex_client.api import collections

#
# Utility functions
#

def __match_replacement(match):
        return "\\" + match.group(0)

def print_file_completions():
    exit(1)

def print_dir_completions():
    exit(2)

def print_escaped_name(name):
    if name is None:
        return
    name = re.sub(r'[ \\ ()<>\']', __match_replacement, name)
    print name.encode("utf-8")

def print_escaped_names(name_list):
    for name in name_list:
        print_escaped_name(name)

def print_resource_identifiers(res_list, current_id = None):
        for r in res_list:
            print_escaped_name(r.get_identifier())

def print_identifiers(collection):
    print_resource_identifiers(collection.get_resources())

#
# Resource specific functions
#

def org_completions(api, param_num, argv):
    if param_num == 0:
        print_identifiers(api.organizations())

def app_completions(api, param_num, argv):
    if param_num == 0:
        org_completions(api, param_num, argv)
    elif param_num == 1 and len(argv) > 0:
        print_identifiers(collections.applications(api, argv[0]))

def app_sync_completions(api, param_num, argv):
    if param_num == 0:
        org_completions(api, param_num, argv)
    elif param_num == 1:
        app_completions(api, param_num, argv)
    elif param_num == 2:
        print_dir_completions()
