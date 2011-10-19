# control.resource - Generic controller for managing cortex resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.resource import ResourceController
from cortex_client.control.exceptions import MissingException

class FilesController(ResourceController):

    _template = "file.json"

    def __init__(self):
        super(FilesController, self).__init__()
        self._register(["r", "read"], self._read)
        self._register(["w", "write"], self._write)
        self._default_action = self._help

    def get_collection(self):
        return self._api.get_file_collection()

    def _read(self, argv):
        file_res = self._get_resource(argv)

        file_content = file_res.get_content()

        # Display the result
        for line in file_content:
            print line,
        print "-"*80

    def _write(self, argv):
        file_res = self._get_resource(argv)

        options = globals.options
        if not options.filename:
            raise MissingException("You must provide a file to upload (--file)")

        file_res.set_content(options.filename)
        file_res.commit()

    def _help(self, argv):
        print '''You must provide an action to perfom.

Actions:
    list            List all files available to the user
    show <uuid>     Show the details of a file
    add             Create a new file (see below for more details)
    update <uuid>   Update the details of a file
    delete <uuid>   Delete a file
    read <uuid>     Fetch the content of a file
    write <uuid>    Update the content of a file (content is read from file
                    whose name must be provided through --file option)

A file is completely described by its details and its content. Details include a
file name as well as a list of parameters. When creating a new file (add),
details must be provided (through --file, --json or interactively), the content
is read from file whose name is given in the details.
'''
