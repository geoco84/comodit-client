#!/bin/bash

# Builds cortex-client's API documentation. This script must have project root
# as working directory (i.e. with 'scripts/build-doc.sh').

epydoc --config doc/epydoc.conf
