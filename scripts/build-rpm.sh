#!/bin/bash

VERSION=`git describe --long --match "release*" | awk -F"-" '{print $2}'`
RELEASE=`git describe --long --match "release*" | awk -F"-" '{print $3}'`
COMMIT=`git describe --long --match "release*" | awk -F"-" '{print $4}'`

NAME=cortex-client
MAN_PAGE_FILE="cortex-doc/tmp/en-US/man/cortex.1"
TAR_CONTENT="cortex_client templates conf setup.py cortex scripts/completions.sh "${MAN_PAGE_FILE}
PLATFORMS=(epel-6-i386 fedora-15-i386 fedora-16-i386)

cd `dirname $0`
cd ..

#scripts/build-man.sh

# Workaround for lack of proper publican version on devel.bruxelles
if [[ ! -f ${MAN_PAGE_FILE} ]]
then
    echo "!!! Man page could not be generated, creating dummy file !!!"
    mkdir -p `dirname ${MAN_PAGE_FILE}`
    touch ${MAN_PAGE_FILE}
fi

sed "s/#VERSION#/${VERSION}/g" rpmbuild/SPECS/${NAME}.spec.template > rpmbuild/SPECS/${NAME}.spec
sed -i "s/#RELEASE#/${RELEASE}/g" rpmbuild/SPECS/${NAME}.spec
sed -i "s/#COMMIT#/${COMMIT}/g" rpmbuild/SPECS/${NAME}.spec

tar -cvzf $HOME/rpmbuild/SOURCES/${NAME}-${VERSION}-${RELEASE}.tar.gz ${TAR_CONTENT}
rpmbuild -ba rpmbuild/SPECS/${NAME}.spec

for platform in "${PLATFORMS[@]}"
do
    /usr/bin/mock -r ${platform} --rebuild $HOME/rpmbuild/SRPMS/${NAME}-${VERSION}-${RELEASE}*.src.rpm
done
