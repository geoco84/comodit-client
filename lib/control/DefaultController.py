'''
Created on Nov 22, 2010

@author: eschenal
'''

class DefaultController(object):
    '''The default (abstract) controller'''

    def __init__(self):
        self._actions = {}
        self._default_action = lambda x : self._error("No default action defined", -1)
    
    def run(self, argv):
        '''Execute the action (first argument in argv with other arguments) from this controller'''
        self._pre(argv)
        
        if len(argv) == 0: 
            self._default_action(argv[1:])
        else:
            action = argv[0]
            if self._actions.has_key(action):
                self._actions[action](argv[1:])
            else:
                raise ControllerException("Pardon Monsieur ? I'm not sure I understand your request")
            
        self._post(argv)
    
    def _pre(self, argv):
        pass
    
    def _post(self, argv):
        pass
    
    def _error(self, message, code=-1):
        print(message)
        exit(code)
        
    def _register(self, action, command):
        if isinstance(action, (list, tuple)):
            for a in action:
                self._actions[a] = command
        else:
            self._actions[a] = command
            
class ControllerException(Exception):
    
    def __init__(self, msg):
        self.msg = msg