# rest.client - Generic client for crud opetations in a REST-Json API.
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

import urllib, urllib2, json
from urllib2 import HTTPError
from util import urllibx
from exceptions import ApiException

class Client:

    def __init__(self, endpoint, username, password):
        self.endpoint = endpoint.rstrip('/')
        self.username = username
        self.password = password
    
    def create(self, resource, item, parameters={}, decode=True):
        url = self.endpoint + "/" + resource
        if len(parameters) >0:
            url = url + "?" + urllib.urlencode(parameters)
            
        req = urllibx.RequestWithMethod(url, method="POST", headers=self._headers(), data=json.dumps(item))
        raw = self._urlopen(req)
        if decode: 
            return json.load(raw)
        else:
            return raw  
    
    def read(self, resource, parameters={}, decode=True):
        url = self.endpoint + "/" + resource
        if len(parameters) >0:
            url = url + "?" + urllib.urlencode(parameters)

        req = urllibx.RequestWithMethod(url, method="GET", headers=self._headers())
        raw = self._urlopen(req)
        if decode: 
            return json.load(raw)
        else:
            return raw    

    def update(self, resource, item=None, parameters={}, decode=True):
        url = self.endpoint + "/" + resource
        if len(parameters) >0:
            url = url + "?" + urllib.urlencode(parameters)

        req = urllibx.RequestWithMethod(url, method="PUT", headers=self._headers())
        if item: req.add_data(json.dumps(item))
        raw = self._urlopen(req)
        if decode: 
            return json.load(raw)
        else:
            return raw  

    def delete(self, resource, parameters={}):
        url = self.endpoint + "/" + resource + "?" + urllib.urlencode(parameters)
        req = urllibx.RequestWithMethod(url, method='DELETE', headers=self._headers())
        self._urlopen(req)
        return
    
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
                data = json.loads(err.msg)
                message = data.msg
                errno = data.err
            except:
                message = err.msg
                errno = err.code
            raise ApiException(message, errno)
            