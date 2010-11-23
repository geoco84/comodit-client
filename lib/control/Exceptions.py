'''
Created on Nov 22, 2010

@author: eschenal
'''

class ArgumentException(Exception):
    def __init__(self, message):
        self.msg = message

class NotFoundException(ArgumentException):
    pass

class MissingException(ArgumentException):
    pass
