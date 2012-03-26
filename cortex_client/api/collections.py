# coding: utf-8
from cortex_client.api.organization import Organization
from cortex_client.api.environment import Environment
from cortex_client.api.host import Host, Instance
from cortex_client.api.application import Application

def organizations(api):
    return api.organizations()

def groups(api, org_name):
    org = Organization(organizations(api), {"name": org_name})
    return org.groups()

def applications(api, org_name):
    org = Organization(organizations(api), {"name": org_name})
    return org.applications()

def distributions(api, org_name):
    org = Organization(organizations(api), {"name": org_name})
    return org.distributions()

def platforms(api, org_name):
    org = Organization(organizations(api), {"name": org_name})
    return org.platforms()

def environments(api, org_name):
    org = Organization(organizations(api), {"name": org_name})
    return org.environments()

def hosts(api, org_name, env_name):
    env = Environment(environments(api, org_name), {"name": env_name})
    return env.hosts()

def application_files(api, org_name, app_name):
    app = Application(applications(api, org_name), {"name": app_name})
    return app.files()

def application_contexts(api, org_name, env_name, host_name):
    host = Host(hosts(api, org_name, env_name), {"name": host_name})
    return host.applications()

def instance(api, org_name, env_name, host_name):
    host = Host(hosts(api, org_name, env_name), {"name": host_name})
    return host.instance()
