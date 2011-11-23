#!/bin/bash
echo "Building cortex-client from master"

cd `dirname $0`
cd ..

git checkout master
git pull
git submodule init
git submodule update

NAME="cortex-client"
VERSION=`git describe --long --match "release*" | awk -F"-" '{print $2}'`
RELEASE=`git describe --long --match "release*" | awk -F"-" '{print $3}'`

./scripts/build-rpm.sh

cp /var/lib/mock/epel-6-i386/result/${NAME}-${VERSION}-${RELEASE}*.noarch.rpm /var/www/html/public/comodit-dev/centos/6.0/i686/
cp /var/lib/mock/epel-6-i386/result/${NAME}-${VERSION}-${RELEASE}*.noarch.rpm /var/www/html/public/comodit-dev/centos/6.0/x86_64/
cp /var/lib/mock/epel-6-i386/result/${NAME}-${VERSION}-${RELEASE}*.src.rpm /var/www/html/public/comodit-dev/centos/6.0/SRPMS/

cp /var/lib/mock/fedora-14-i386/result/${NAME}-${VERSION}-${RELEASE}*.noarch.rpm /var/www/html/public/comodit-dev/fedora/14/i686/
cp /var/lib/mock/fedora-14-i386/result/${NAME}-${VERSION}-${RELEASE}*.noarch.rpm /var/www/html/public/comodit-dev/fedora/14/x86_64/
cp /var/lib/mock/fedora-14-i386/result/${NAME}-${VERSION}-${RELEASE}*.src.rpm /var/www/html/public/comodit-dev/fedora/14/SRPMS/

cp /var/lib/mock/fedora-15-i386/result/${NAME}-${VERSION}-${RELEASE}*.noarch.rpm /var/www/html/public/comodit-dev/fedora/15/i686/
cp /var/lib/mock/fedora-15-i386/result/${NAME}-${VERSION}-${RELEASE}*.noarch.rpm /var/www/html/public/comodit-dev/fedora/15/x86_64/
cp /var/lib/mock/fedora-15-i386/result/${NAME}-${VERSION}-${RELEASE}*.src.rpm /var/www/html/public/comodit-dev/fedora/15/SRPMS/

/var/www/html/public/updaterepo.sh

