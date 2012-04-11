# coding: utf-8

import json

from cortex_client.control.doc import ActionDoc
from cortex_client.util import globals

class AuditHelper(object):
    def __init__(self, ctrl, audit_params):
        self._ctrl = ctrl
        self._params = audit_params

    def audit(self, argv):
        res = self._ctrl._get_resource(argv)
        logs = res.audit_logs().get_resources()

        # Display the result
        options = globals.options
        if options.raw:
            json.dumps(logs, sort_keys = True, indent = 4)
        else:
            for log in logs:
                print log.get_timestamp(), log.get_message(), "by", log.get_initiator()

    def audit_doc(self):
        return ActionDoc("audit", self._params, """
        Displays audit log.""")
