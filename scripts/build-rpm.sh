#!/bin/bash

NAME="cortex-client"
SPEC_FILE_NAME="cortex-client"
PLATFORMS="epel-6-i386 fedora-15-i386 fedora-16-i386"
TAR_CONTENT="cortex_client templates conf setup.py cortex auto_completion/cortex doc/cortex.1"

cd `dirname $0`
cd ..

. scripts/build-pkg-functions

set_version $1 $2
generate_version_file $VERSION $RELEASE

sed "s/#VERSION#/${VERSION}/g" rpmbuild/SPECS/${SPEC_FILE_NAME}.spec.template > rpmbuild/SPECS/${SPEC_FILE_NAME}.spec
sed -i "s/#RELEASE#/${RELEASE}/g" rpmbuild/SPECS/${SPEC_FILE_NAME}.spec
sed -i "s/#COMMIT#/${COMMIT}/g" rpmbuild/SPECS/${SPEC_FILE_NAME}.spec

tar -cvzf $HOME/rpmbuild/SOURCES/${NAME}-${VERSION}-${RELEASE}.tar.gz ${TAR_CONTENT}
rpmbuild -ba rpmbuild/SPECS/${SPEC_FILE_NAME}.spec

for platform in $PLATFORMS
do
    /usr/bin/mock -r ${platform} --rebuild $HOME/rpmbuild/SRPMS/${NAME}-${VERSION}-${RELEASE}*.src.rpm
done

