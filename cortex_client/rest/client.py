# rest.client - Generic client for crud opetations in a REST-Json API.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

import urllib, urllib2, json, urlparse
import cortex_client.util.fileupload as fileupload
from urllib2 import HTTPError
from cortex_client.util import urllibx
from cortex_client.rest.exceptions import ApiException


class Client:

    def __init__(self, endpoint, username, password):
        self.endpoint = endpoint.rstrip('/')
        self.username = username
        self.password = password

    def create(self, resource, item = None, parameters = {}, decode = True):
        url = self.endpoint + "/" + urllib.quote(resource)
        if len(parameters) > 0:
            url = url + "?" + urllib.urlencode(parameters)

        if item:
            try:
                json_data = json.dumps(item)
            except Exception, e:
                raise ApiException("Could not encode given data: " + e.message, 0)
            req = urllibx.RequestWithMethod(url, method = "POST", headers = self._headers(), data = json_data)
        else:
            req = urllibx.RequestWithMethod(url, method = "POST", headers = self._headers())
        raw = self._urlopen(req)
        if decode:
            try:
                return json.load(raw)
            except:
                raise ApiException("Could not decode response: " + raw, 0)
        else:
            return raw

    def read(self, resource, parameters = {}, decode = True):
        url = self.endpoint + "/" + urllib.quote(resource)
        if len(parameters) > 0:
            url = url + "?" + urllib.urlencode(parameters)

        req = urllibx.RequestWithMethod(url, method = "GET", headers = self._headers())
        raw = self._urlopen(req)
        if decode:
            return json.load(raw)
        else:
            return raw

    def update(self, resource, item = None, parameters = {}, decode = True):
        url = self.endpoint + "/" + urllib.quote(resource)
        if len(parameters) > 0:
            url = url + "?" + urllib.urlencode(parameters)

        req = urllibx.RequestWithMethod(url, method = "PUT", headers = self._headers())
        if item: req.add_data(json.dumps(item))
        raw = self._urlopen(req)
        if decode:
            return json.load(raw)
        else:
            return raw

    def delete(self, resource, parameters = {}):
        url = self.endpoint + "/" + urllib.quote(resource)
        if len(parameters) > 0:
            url = url + "?" + urllib.urlencode(parameters)

        req = urllibx.RequestWithMethod(url, method = 'DELETE', headers = self._headers())
        self._urlopen(req)
        return

    def upload_to_exising_file_with_path(self, file_name, path):
        url = urlparse.urlparse(self.endpoint + "/" + urllib.quote(path))
        response = fileupload.post_multipart(url.netloc, url.path,
                                             [("test", "none")],
                                             [("file", file_name)],
                                             {"Authorization": "Basic " + (self.username + ":" + self.password).encode("base64").rstrip()})
        return response

    def _headers(self):
        s = self.username + ":" + self.password
        headers = {
                   "Authorization": "Basic " + s.encode("base64").rstrip(),
                   "Content-Type": "application/json",
                   }
        return headers

    def _urlopen(self, request):
        try:
            return urllib2.urlopen(request)
        except HTTPError as err:
            try:
                data = json.load(err)
                msg_list = data["error"]
                message = "["
                if len(msg_list) > 0:
                    i = 0
                    while i < len(msg_list) - 1:
                        message += msg_list[i] if msg_list[i] else "None"
                        message += ", "
                    message += msg_list[len(msg_list) - 1] if msg_list[len(msg_list) - 1] else "None"
                message += "]"
            except Exception:
                message = err.msg

            raise ApiException(message, err.code)

