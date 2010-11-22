'''
Created on Nov 22, 2010

@author: eschenal
'''
from control.DefaultController import ControllerException

controllers = {}

def dispatch(keyword, argv):
    global controllers
    if controllers.has_key(keyword):
        controllers[keyword].run(argv)
    else:
        raise ControllerException("I'm sorry Sir, I don't understand what you mean by " + keyword)
    
def register(keyword, controller):
    global controllers
    
    if isinstance(keyword, (list, tuple)):
        for k in keyword:
            controllers[k] = controller
    else:
        controllers[keyword] = controller