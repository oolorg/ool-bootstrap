#!/bin/bash

USER=openstack
PW=password110
SSH_DIR="/home/openstack"

CONF="${SSH_DIR}/ipaddress.txt"
IPADDRESS=(`cat "$CONF"`)

ssh-keygen -N "" -t rsa -f ${SSH_DIR}/.ssh/id_rsa
cp .ssh/id_rsa* /root/.ssh/
chown "${USER}:${USER}" -R ${SSH_DIR}/.ssh/id_*

for HOST in ${IPADDRESS[@]}
do
   expect -c "
   set timeout 120
   spawn ssh-copy-id "${USER}@${HOST}"
   expect \"$USER@$HOST's password:\"
   send $PW\r
   interact
   "
done
