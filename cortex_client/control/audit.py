# coding: utf-8

from cortex_client.control.doc import ActionDoc

class AuditHelper(object):
    def __init__(self, ctrl, audit_params):
        self._ctrl = ctrl
        self._params = audit_params

    def audit(self, argv):
        res = self._ctrl._get_resource(argv)
        logs = res.audit_logs().get_resources()

        # Display the result
        for log in logs:
            user = log.get_initiator_full_name()
            if user is None or user == "":
                user = log.get_initiator_username()
            print log.get_timestamp(), log.get_message(), "by", user

    def audit_doc(self):
        return ActionDoc("audit", self._params, """
        Displays audit log.""")
