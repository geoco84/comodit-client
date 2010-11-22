'''
Created on Nov 22, 2010

@author: eschenal
'''

class ApiException(Exception):
    pass

class NoResourceException(ApiException):
    def __init__(self, uuid):
        self.uuid= uuid