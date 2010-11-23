'''
Created on Nov 15, 2010

@author: eschenal
'''
import urllib2
from urllib2 import HTTPError
from util import urllibx, globals
import urllib
import json

class Client:

    def __init__(self, endpoint, username, password):
        self.endpoint = endpoint.rstrip('/')
        self.username = username
        self.password = password
    
    def create(self, resource, item, parameters={}, decode=True):
        url = self.endpoint + "/" + resource + "?" + urllib.urlencode(parameters)
        req = urllibx.RequestWithMethod(url, method="POST", headers=self._headers(), data=json.dumps(item))
        raw = self._urlopen(req)
        if decode: 
            return json.load(raw)
        else:
            return raw  
    
    def read(self, resource, parameters={}, decode=True):
        url = self.endpoint + "/" + resource + "?" + urllib.urlencode(parameters)
        req = urllibx.RequestWithMethod(url, method="GET", headers=self._headers())
        raw = self._urlopen(req)
        if decode: 
            return json.load(raw)
        else:
            return raw    

    def update(self, resource, item=None, parameters={}, decode=True):
        url = self.endpoint + "/" + resource + "?" + urllib.urlencode(parameters)
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