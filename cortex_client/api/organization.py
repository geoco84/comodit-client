# coding: utf-8
"""
Organization module.

@organization: Guardis
@copyright: 2011 Guardis SPRL, Liège, Belgium.
"""

from resource import Resource
from cortex_client.util.json_wrapper import StringFactory
from environment import Environment
from environment_collection import EnvironmentCollection
from distribution import Distribution
from distribution_collection import DistributionCollection
from platform import Platform
from platform_collection import PlatformCollection
from application import Application
from application_collection import ApplicationCollection
from cortex_client.api.group_collection import GroupCollection

class Organization(Resource):
    """
    An organization. An organization may contain environments.
    
    @see: L{Environment}
    """
    def __init__(self, collection, json_data = None):
        """
        @param api: An access point.
        @type api: L{CortexApi}
        @param json_data: A quasi-JSON representation of application's state.
        @type json_data: dict, list or String
        """
        super(Organization, self).__init__(collection, json_data)

    def get_environments(self):
        """
        Provides organization's environments. Environments are added to an
        organization when they are created on cortex server.
        @return: A list of environments UUIDs
        @rtype: list of String
        """
        return self._get_list_field("environments", StringFactory())

    def get_groups(self):
        return self._get_list_field("groups", StringFactory())

    def get_version(self):
        """
        Provides organization's version number.
        @return: The version number
        @rtype: Integer
        """
        return int(self._get_field("version"))

    def _show(self, indent = 0):
        print " "*indent, "Name:", self.get_name()
        print " "*indent, "Description:", self.get_description()
        print " "*indent, "Environments:"
        environments = self.get_environments()
        for e in environments:
            print " "*(indent + 2), e
        print " "*indent, "Groups:"
        groups = self.get_groups()
        for g in groups:
            print " "*(indent + 2), g

    def get_identifier(self):
        return self.get_name()

    def applications(self):
        """
        Provides an access to applications collection of this organization.
        
        @return: The collection
        @rtype: L{ApplicationCollection}
        """
        return ApplicationCollection(self._get_api(), self._get_path() + "applications/")

    def new_application(self, name):
        """
        Factory method for application resource.

        @return: An application connected to associated cortex server.
        @rtype: L{Application}
        """
        app = Application(self.applications())
        app.set_name(name)
        return app

    def platforms(self):
        """
        Provides an access to platforms collection of this organization.
        
        @return: The collection
        @rtype: L{PlatformCollection}
        """
        return PlatformCollection(self._get_api(), self._get_path() + "platforms/")

    def new_platform(self, name):
        """
        Factory method for platform resource.

        @return: A platform connected to associated cortex server.
        @rtype: L{Platform}
        """
        plat = Platform(self.platforms())
        plat.set_name(name)
        return plat

    def distributions(self):
        """
        Provides an access to distributions collection of this organization.
        
        @return: The collection
        @rtype: L{ApplicationCollection}
        """
        return DistributionCollection(self._get_api(), self._get_path() + "distributions/")

    def new_distribution(self, name):
        """
        Factory method for distribution resource.

        @return: A distribution connected to associated cortex server.
        @rtype: L{Distribution}
        """
        dist = Distribution(self.distributions())
        dist.set_name(name)
        return dist

    def environments(self):
        """
        Provides an access to distributions collection of this organization.
        
        @return: The collection
        @rtype: L{ApplicationCollection}
        """
        return EnvironmentCollection(self._get_api(), self._get_path() + "environments/")

    def new_environment(self, name):
        """
        Factory method for environment resource.

        @return: An environment connected to associated cortex server.
        @rtype: L{Environment}
        """
        env = Environment(self.environments())
        env.set_name(name)
        env.set_organization(self.get_name())
        return env

    def groups(self):
        return GroupCollection(self._get_api(), self._get_path() + "groups/")
