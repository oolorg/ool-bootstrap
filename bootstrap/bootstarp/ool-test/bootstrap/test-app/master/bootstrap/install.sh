#!/bin/bash

SCRIPT_HOME=$(cd $(dirname $0);pwd)

adduser bootstrap --disabled-password --gecos ""
sh -c "echo bootstrap        ALL=\(ALL\)       NOPASSWD: ALL >> /etc/sudoers"

mkdir "/var/log/bootstrap"
chown bootstrap:bootstrap "/var/log/bootstrap"

if [ ! -e  "${1}" ]; then
  mkdir  "${1}"
fi
chown -R bootstrap:bootstrap "${1}"

sh -c "echo -n ${1} >> /home/bootstrap/verify_server.conf"

cp $SCRIPT_HOME"/etc/init.d/verify_server" "/etc/init.d/"
cp $SCRIPT_HOME"/usr/bin/verify_server" "/usr/bin/"
cp $SCRIPT_HOME"/verify_server" "${1}/"
cp -R $SCRIPT_HOME"/cgi-bin" "${1}/"

service verify_server start
update-rc.d verify_server defaults
