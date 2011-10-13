import os

import ConfigParser

def singleton(cls):
    """ Define the config singleton decorator
    """
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton
class Config(object):
    _instance = None

    def __init__(self):
        self.config = None

        # load the configuration file path
        self.config_path = self._get_config_path()
        if not self.config_path:
            return

        # load the configuration file
        self.config = self._get_config_dict(self.config_path)
        if not self.config:
            raise IOError("Bad configuration file")

    def _get_config_path(self):
        """ Gets the configuration path with following priority order :
        1) <current_directory>/conf/cortex-client.conf
        2) ~/.cortexrc
        3) /etc/cortex/cortex-client.conf

        elsewhere : return None
        """
        config_name = "cortex-client.conf"

        curdir_path = os.curdir + "/conf/" + config_name
        user_path = os.path.expanduser("~") + "/.cortexrc"
        etc_path = "/etc/cortex/" + config_name

        for loc in curdir_path, user_path, etc_path:
            if os.path.isfile(loc):
                return loc

        return None

    def _get_config_dict(self, config_path):
        """ Transforms the configuration file to a dict of dict
        example :

        [client]
        username = foologin
        password = foopass
        api      = url

        becomes :

          {
            'client': {
              'username': 'foologin',
              'password': 'foopass'
              'api': 'url'
            }
          }

        """
        self.config_parser = ConfigParser.ConfigParser()
        self.config_parser.read(config_path)

        cfg = {}
        for section in self.config_parser.sections():
            cfg[section] = dict(self.config_parser.items(section))

        return cfg