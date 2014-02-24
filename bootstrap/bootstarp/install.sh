#!/bin/bash

SCRIPT_HOME=$(cd $(dirname $0);pwd)

HOME_DIR="/home/bootstrap"
if [ -e "${HOME_DIR}" ]; then
  echo "The module 'ool-test' already exists."
  exit 0
fi

adduser bootstrap --disabled-password --gecos ""
sh -c "echo bootstrap        ALL=\(ALL\)       NOPASSWD: ALL >> /etc/sudoers"

LOG_DIR="/var/log/bootstrap"
if [ ! -e  "${LOG_DIR}" ]; then
  mkdir  "${LOG_DIR}"
  chown bootstrap:bootstrap "${LOG_DIR}"
fi

# Copy of module 'ool-test'
cp -r "${SCRIPT_HOME}/ool-test" "/usr/lib/"
chown -R bootstrap:bootstrap "/usr/lib/ool-test" 

# Apache configuration
cp "${SCRIPT_HOME}/apache/sites-available/bootstrap" "/etc/apache2/sites-available/"
a2ensite bootstrap

service apache2 restart

