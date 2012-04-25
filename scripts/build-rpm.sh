#!/bin/bash

NAME="cortex-client"
SPEC_FILE_NAME="cortex-client"
PLATFORMS="epel-6-i386 fedora-15-i386 fedora-16-i386"

MAN_PAGE_FILE="cortex-doc/tmp/en-US/man/cortex.1"
FALLBACK_MAN=`readlink -f scripts/cortex.1`
TAR_CONTENT="cortex_client templates conf setup.py cortex scripts/completions.sh "${MAN_PAGE_FILE}

if [ -z $1 ]
then
  VERSION=`git describe --long --match "release*" | awk -F"-" '{print $2}'`
else
  VERSION=$1
fi

if [ -z $2 ]
then
  RELEASE=`git describe --long --match "release*" | awk -F"-" '{print $3}'`
else
  RELEASE=$2
fi

COMMIT=`git describe --long --match "release*" | awk -F"-" '{print $4}'`

# Generate version file
echo "VERSION=\""$VERSION"\"" > cortex_client/version.py
echo "RELEASE=\""$RELEASE"\"" >> cortex_client/version.py

cd `dirname $0`
cd ..

scripts/build-man.sh

# Workaround for lack of proper publican version on devel.bruxelles
if [[ ! -f ${MAN_PAGE_FILE} ]]
then
    echo "!!! Man page could not be generated, using fallback file !!!"
    mkdir -p `dirname ${MAN_PAGE_FILE}`
    cp ${FALLBACK_MAN} ${MAN_PAGE_FILE}
fi

sed "s/#VERSION#/${VERSION}/g" rpmbuild/SPECS/${SPEC_FILE_NAME}.spec.template > rpmbuild/SPECS/${SPEC_FILE_NAME}.spec
sed -i "s/#RELEASE#/${RELEASE}/g" rpmbuild/SPECS/${SPEC_FILE_NAME}.spec
sed -i "s/#COMMIT#/${COMMIT}/g" rpmbuild/SPECS/${SPEC_FILE_NAME}.spec

tar -cvzf $HOME/rpmbuild/SOURCES/${NAME}-${VERSION}-${RELEASE}.tar.gz ${TAR_CONTENT}
rpmbuild -ba rpmbuild/SPECS/${SPEC_FILE_NAME}.spec

for platform in $PLATFORMS
do
    /usr/bin/mock -r ${platform} --rebuild $HOME/rpmbuild/SRPMS/${NAME}-${VERSION}-${RELEASE}*.src.rpm
done

