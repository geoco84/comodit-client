'''
Created on Nov 15, 2010

@author: eschenal
'''
import urllib2
import json
import urllibx
import globals
from urllib2 import HTTPError

class Client:

    def __init__(self, endpoint, username, password):
        self.endpoint = endpoint.rstrip('/')
        self.username = username
        self.password = password

    def list(self, collection):
        url = self.endpoint + "/" + collection
        req = urllibx.RequestWithMethod(url, method="GET", headers=self._headers())
        raw = self._urlopen(req)
        result = json.load(raw)
        return result
    
    def create(self, collection, resource):
        url = self.endpoint + "/" + collection
        req = urllibx.RequestWithMethod(url, method="POST", headers=self._headers(), data=json.dumps(resource))
        raw = self._urlopen(req)
        result = json.load(raw)
        return result
    
    def read(self, collection, uuid):
        url = self.endpoint + "/" + collection + "/" + uuid
        req = urllibx.RequestWithMethod(url, method="GET", headers=self._headers())
        raw = self._urlopen(req)
        result = json.load(raw)
        return result    

    def update(self, collection, uuid, resource):
        url = self.endpoint + "/" + collection + "/" + uuid
        req = urllibx.RequestWithMethod(url, method="PUT", headers=self._headers(), data=json.dumps(resource))
        raw = self._urlopen(req)
        result = json.load(raw)
        return result

    def delete(self, collection, uuid):
        url = self.endpoint + "/" + collection + "/" + uuid
        req = urllibx.RequestWithMethod(url, method='DELETE', headers=self._headers())
        raw = self._urlopen(req)
        return
    
    def _headers(self):
        s = self.username + ":" + self.password
        headers = {
                   "Authorization": "Basic " + s.encode("base64").rstrip(),
                   "Content-Type": "application/json",
                   }
        return headers
    
    def _urlopen(self, request):
        options = globals.options
        try:
            return urllib2.urlopen(request)
        except HTTPError as err:
            if options.verbose:
                print "HTTP Request returned error " + str(err.msg)
                print err.read()
                exit(-1)
        
class ApiException(Exception):
    pass

class NoResourceException(ApiException):
    def __init__(self, uuid):
        self.uuid= uuid
     