import test_utils, setup, definitions, delete, create, provision, threading, smtplib

import test_webserver
import test_simple_settings
import test_simple_web_page
import test_list_settings
import test_struct_settings
import test_link_settings
import test_clone

from threading import Thread
from email.mime.text import MIMEText

test_modules = \
    [
        test_clone.__name__,
        test_webserver.__name__,
        test_simple_web_page.__name__,
        test_simple_settings.__name__,
        test_list_settings.__name__,
        test_struct_settings.__name__,
        test_link_settings.__name__
     ]

class ProvisionThread(Thread):
    def __init__(self, host_name, time_out = 30):
        super(ProvisionThread, self).__init__()
        self._host_name = host_name
        self._time_out = time_out
        self._error = False

    def run(self):
        try:
            provision.provision_host(self._host_name, self._time_out)
        except:
            self._error = True

    def is_successfull(self):
        return not self._error

    def get_host_name(self):
        return self._host_name


def send_mail(setup_errors, host_errors, test_errors):
    # Connect to SMTP server
    if setup.global_vars.smtp_ssl:
        s = smtplib.SMTP_SSL(setup.global_vars.smtp_server)
    else:
        s = smtplib.SMTP(setup.global_vars.smtp_server)

    # Login if authentication is required
    if setup.global_vars.smtp_user != None:
        s.login(setup.global_vars.smtp_user, setup.global_vars.smtp_pass)

    # Send the mail
    test_errors_str = ""
    for e in test_errors:
        argv_str = ""
        for a in e.get_arguments():
            argv_str = a + " "
        test_errors_str += "- " + e.get_module_name() + " with arguments " + argv_str + "\n"
    setup_errors_str = ""
    for e in setup_errors:
        setup_errors_str += "- " + e + "\n"
    host_errors_str = ""
    for e in host_errors:
        host_errors_str += "- " + e + "\n"

    msg = MIMEText("""For more details about error(s), see ComodIT and test hosts.

""" + setup.global_vars.comodit_url + """

Setup errors:
""" + setup_errors_str + """
Provisioning errors:
""" + host_errors_str + """
Test modules:
""" + test_errors_str)

    msg['Subject'] = 'Integration tests result (' + str(len(setup_errors) + len(host_errors) + len(test_errors)) + ')'

    s.sendmail("", setup.global_vars.email_dests, msg.as_string())
    s.quit()

if __name__ == "__main__":
    setup_errors = []

    try:
        # Setup
        setup.setup()
        setup.create_files()
        definitions.define()

        # Clear previous data (if any)
        delete.delete_resources()

        # Setup new test environment
        create.create_resources()
    except Exception, e:
        setup_errors.append(type(e) + e.message)

    host_errors = []
    test_errors = []
    if len(setup_errors) == 0:
        # Hosts list
        host_names = []
        for plat_name in setup.global_vars.plat_names:
            if plat_name != "Local":
                host_names.append(definitions.get_host_name(plat_name))

        # Provision hosts in parallel
        threads = []
        for host_name in host_names:
            t = ProvisionThread(host_name, setup.global_vars.prov_time_out) # time-out of half an hour
            threads.append(t)
            t.start()

        # Wait for all hosts to be provisioned
        for t in threads:
            print " " * 80
            print "Joining", t.name
            t.join()

        # Run tests on each host (sequential for now)
        for t in threads:
            host_name = t.get_host_name()
            if t.is_successfull():
                print " " * 80
                print "Running tests on", host_name
                errors = test_utils.run_tests(test_modules, [host_name, str(setup.global_vars.change_time_out)], True)
                test_errors += errors
            else:
                print " " * 80
                print "Skip failed provisioning", host_name
                host_errors.append(host_name)

    # Send mail notification
    send_mail(setup_errors, host_errors, test_errors)
