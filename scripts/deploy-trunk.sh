#/bin/bash
echo "Building cortex-client from trunk"

cd `dirname $0`
cd ..

git checkout dev
git pull

NAME="cortex-client"
VERSION=`git describe --long --match "release*" | awk -F"-" '{print $2}'`
RELEASE=`git describe --long --match "release*" | awk -F"-" '{print $3}'`

./scripts/build-rpm.sh
/var/www/html/public/deploy-trunk.sh $HOME/rpmbuild/RPMS/noarch/${NAME}-${VERSION}-${RELEASE}.noarch.rpm
/var/www/html/public/updaterepo.sh

