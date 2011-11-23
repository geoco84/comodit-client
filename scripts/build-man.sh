#!/bin/bash

# Builds cortex-client's man page from cortex-doc submodule.

cd `dirname $0`
cd ..

# Prepare build
cd cortex-doc
git checkout master

# Build and install comodit brand if necessary
rpm -q publican-comodit
if [[ $? == 1 ]]
then
    mkdir -p ${HOME}/rpmbuild/SOURCES
    scripts/build-brand-rpm.sh
    if [[ $? != 0 ]]
    then
        echo "Could not build brand RPM"
        exit 1
    fi

    VERSION=`git describe --long --match "release*" | awk -F"-" '{print $2}'`
    RELEASE=`git describe --long --match "release*" | awk -F"-" '{print $3}'`
    COMMIT=`git describe --long --match "release*" | awk -F"-" '{print $4}'`

    rpm -ivh ${HOME}/rpmbuild/RPMS/noarch/publican-comodit-${VERSION}-${RELEASE}.noarch.rpm
fi

# Build man page
publican build --langs=en-US --formats=man
