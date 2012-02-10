import unittest

from unittest.case import TestCase

from test.mock.api import CortexApi

from cortex_client.api.collection import Collection, ResourceNotFoundException
from cortex_client.util.json_wrapper import JsonWrapper
from cortex_client.rest.exceptions import ApiException
from cortex_client.api.application_collection import ApplicationCollection
from cortex_client.api.application import Application
from cortex_client.api.distribution import Distribution
from cortex_client.api.distribution_collection import DistributionCollection
from cortex_client.api.environment import Environment
from cortex_client.api.environment_collection import EnvironmentCollection
from cortex_client.api.group import Group
from cortex_client.api.group_collection import GroupCollection
from cortex_client.api.host import Host
from cortex_client.api.host_collection import HostCollection
from cortex_client.api.organization_collection import OrganizationCollection
from cortex_client.api.organization import Organization
from cortex_client.api.platform_collection import PlatformCollection
from cortex_client.api.platform import Platform
from cortex_client.api.user_collection import UserCollection
from cortex_client.api.user import User
from cortex_client.api.file import File, FileCollection
from cortex_client.api.settings import Setting, SettingCollection
from cortex_client.api.parameters import Parameter, ParameterCollection
from cortex_client.api.exceptions import PythonApiException

class CollectionTest(TestCase):
    def setUp(self):
        self._api = CortexApi("endpoint", "user", "pass")
        self._collection = Collection("path/", self._api)

    def tearDown(self):
        pass


    # Add resource tests

    def test_add_resource_success(self):
        # Mock Client.create
        self._api._client.create = self._create_successful
        self._expected_resource = "path/"

        json_data = {"test":"value"}
        resource = JsonWrapper(json_data)

        self._collection.add_resource(resource)

    def test_add_resource_failure(self):
        # Mock Client.create
        self._api._client.create = self._create_failure
        self._expected_resource = "path/"

        json_data = {"test":"value"}
        resource = JsonWrapper(json_data)

        try:
            self._collection.add_resource(resource)
        except PythonApiException:
            return
        self.assertFalse(True)


    # Get resources tests

    def test_get_resources_success(self):
        # Mock Client.read
        self._read_result = {"count":"3", "items":["a", "b", "c"]}
        self._api._client.read = self._read_success
        self._expected_resource = "path/"
        self._collection._new_resource = self._identity

        resources = self._collection.get_resources()

        self.assertEqual(len(resources), 3, "List should contain 3 elements")
        self.assertTrue("a" in resources, "a string should be in list")
        self.assertTrue("b" in resources, "b string should be in list")
        self.assertTrue("c" in resources, "c string should be in list")

    def test_get_resources_failure(self):
        self._api._client.read = self._read_failure

        try:
            self._collection.get_resources()
        except PythonApiException:
            return
        self.assertFalse(True)


    # Get resources tests

    def test_get_resource_success(self):
        # Mock Client.read
        self._read_result = "result"
        self._api._client.read = self._read_success
        self._expected_resource = "path/a"
        self._collection._new_resource = self._identity

        res = self._collection.get_resource("a")

        self.assertEqual(self._read_result, res)

    def test_get_resource_failure(self):
        self._api._client.read = self._read_failure

        try:
            self._collection.get_resource("a")
        except PythonApiException:
            return
        self.assertFalse(True)

    def test_get_resource_not_found(self):
        self._api._client.read = self._read_success
        self._expected_resource = "" # expected resource is 'path/a'

        try:
            self._collection.get_resource("a")
        except ResourceNotFoundException:
            return
        self.assertFalse(True)


    # Get resources tests

    def test_get_single_resource_success(self):
        # Mock Client.read
        self._read_result = "result"
        self._api._client.read = self._read_success
        self._expected_resource = "path/"
        self._collection._new_resource = self._identity

        res = self._collection.get_single_resource()

        self.assertEqual(self._read_result, res)

    def test_get_single_resource_failure(self):
        self._api._client.read = self._read_failure

        try:
            self._collection.get_single_resource()
        except PythonApiException:
            return
        self.assertFalse(True)


    # Helpers

    def _create_successful(self, resource, item = None, parameters = {}, decode = True):
        if decode and item is not None:
            return item
        else:
            raise Exception("Unexpected")

    def _create_failure(self, resource, item = None, parameters = {}, decode = True):
        raise ApiException("Error", 0)

    def _read_success(self, resource, parameters = {}, decode = True):
        if resource == self._expected_resource:
            return self._read_result
        else:
            raise ApiException("Not found", 404)

    def _read_failure(self, resource, parameters = {}, decode = True):
        raise ApiException("Error", 0)

    def _identity(self, data):
        return data


class SpecificCollections(TestCase):
    def test_applications(self):
        collection = ApplicationCollection(None, "")
        res = collection._new_resource({"name":"name"})
        self.assertTrue(isinstance(res, Application))

    def test_distributions(self):
        collection = DistributionCollection(None, "")
        res = collection._new_resource({"name":"name"})
        self.assertTrue(isinstance(res, Distribution))

    def test_environments(self):
        collection = EnvironmentCollection(None, "")
        res = collection._new_resource({"name":"name"})
        self.assertTrue(isinstance(res, Environment))

    def test_groups(self):
        collection = GroupCollection(None, "")
        res = collection._new_resource({"name":"name"})
        self.assertTrue(isinstance(res, Group))

    def test_hosts(self):
        collection = HostCollection(None, "")
        res = collection._new_resource({"name":"name"})
        self.assertTrue(isinstance(res, Host))

    def test_organizations(self):
        collection = OrganizationCollection(None)
        res = collection._new_resource({"name":"name"})
        self.assertTrue(isinstance(res, Organization))

    def test_platforms(self):
        collection = PlatformCollection(None, "")
        res = collection._new_resource({"name":"name"})
        self.assertTrue(isinstance(res, Platform))

    def test_users(self):
        collection = UserCollection(None)
        res = collection._new_resource({"name":"name"})
        self.assertTrue(isinstance(res, User))

    def test_files(self):
        collection = FileCollection(None, "")
        res = collection._new_resource({"name":"name"})
        self.assertTrue(isinstance(res, File))

    def test_parameters(self):
        collection = ParameterCollection(None, "")
        res = collection._new_resource({"name":"name"})
        self.assertTrue(isinstance(res, Parameter))

    def test_settings(self):
        collection = SettingCollection(None, "")
        res = collection._new_resource({"name":"name"})
        self.assertTrue(isinstance(res, Setting))


class SubCollections(TestCase):
    def setUp(self):
        self._api = CortexApi("e", "u", "p")
        self._api.get_client().update = self._update
        self._api.get_client().read = self._read

    def test_applications(self):
        collection = ApplicationCollection(self._api, "path/")
        res = collection._new_resource({"name":"app_name"})

        # Parameters
        self._test_parameters(res)

        # Files
        self._test_files(res)

    def test_distributions(self):
        collection = DistributionCollection(self._api, "path/")
        res = collection._new_resource({"name":"dist_name"})

        # Parameters
        self._test_parameters(res)

        # Settings
        self._test_settings(res)

        # Files
        self._test_files(res)

    def test_environments(self):
        collection = EnvironmentCollection(self._api, "path/")
        res = collection._new_resource({"name":"env_name"})

        # Settings
        self._test_settings(res)

        # Hosts
        host_coll = res.hosts()
        host = host_coll._new_resource({"name":"host_name"})
        self._expected_path = "path/" + res.get_name() + "/hosts/" + host.get_name() + "/"
        host.commit()

    def test_hosts(self):
        collection = HostCollection(self._api, "path/")
        res = collection._new_resource({"name":"host_name"})

        # Settings
        self._test_settings(res)

        # Application contexts
        app_coll = res.applications()
        self._read_data = {"application":"app_name"}
        context = app_coll._new_resource(self._read_data)
        self._expected_path = "path/" + res.get_name() + "/applications/" + context.get_name() + "/"
        context.update()

    def _test_parameters(self, res):
        param_coll = res.parameters()
        param = param_coll._new_resource({"name":"param_name"})
        self._expected_path = "path/" + res.get_name() + "/parameters/" + param.get_name() + "/"
        param.commit()

    def _test_settings(self, res):
        set_coll = res.settings()
        setting = set_coll._new_resource({"key":"setting_name"})
        self._expected_path = "path/" + res.get_name() + "/settings/" + setting.get_key() + "/"
        setting.commit()

    def _test_files(self, res):
        file_coll = res.files()
        f = file_coll._new_resource({"name":"name"})
        self._expected_path = "path/" + res.get_name() + "/files/" + f.get_name() + "/"
        f.commit()

    def _update(self, resource, item = None, parameters = {}, decode = True):
        self.assertEqual(self._expected_path, resource, "Unexpected resource URL " + resource)
        return item

    def _read(self, resource, parameters = {}, decode = True):
        self.assertEqual(self._expected_path, resource, "Unexpected resource URL " + resource)
        return self._read_data


if __name__ == '__main__':
    unittest.main()

