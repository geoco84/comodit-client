# coding: utf-8
from cortex_client.api.organization import Organization
from cortex_client.api.environment import Environment

def organizations(api):
    return api.organizations()

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
