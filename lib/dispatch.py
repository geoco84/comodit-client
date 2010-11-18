'''
Created on Nov 18, 2010

@author: eschenal
'''
import optparse
import globals
import organizations

def run(argv):
    _parse(argv)

def _parse(argv):
            
    usage = "usage: %prog resource [command] [options]"
    parser = optparse.OptionParser(usage)
    parser.add_option("-H", "--host", dest="host", help="hostname of the cortex server", default="localhost")
    parser.add_option("-P", "--port", dest="port", help="port of the cortex server", default="8000")
    parser.add_option("-u", "--user", dest="username", help="username on cortex server", default="cortex")
    parser.add_option("-p", "--pass", dest="password", help="password on cortex server", default="secret")
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")
    parser.add_option("-f", "--file", dest="filename", help="input file with a JSON object")
    parser.add_option("-j", "--json", dest="json", help="input JSON object")
    parser.add_option("-r", "--raw", action="store_true", dest="raw", default=False, help="output the raw JSON results")

    (globals.options, args) = parser.parse_args()

    if (len(args) == 0):
        parser.print_help()
        exit(-1)  

    _dispatch(args[0], args[1:])
    
def _dispatch(resource, args):
    
    if resource == "organizations":
        organizations.run(args)
    else:
        print "No such resource " + resource
        _usage()
        exit(-1)
        
def _usage():
    
    print """RESOURCES:
 organizations \t Top-level organization, grouping together a set of environments 
 environments \t A group of hosts
 hosts \t\t An individual instance
"""