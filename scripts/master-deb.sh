#!/bin/bash

set e

echo
echo "# Build comodit-client ... "
scripts/build-deb.sh

echo
echo "# Build comodit-client for all distributions in config file ... "
scripts/build-all-deb.sh
