#!/bin/bash

SCRIPT_HOME=$(cd $(dirname $0);pwd)

# Copy of module 'ool-test'
cp -r ${SCRIPT_HOME}/ool-test /usr/lib/
chown -R bootstrap:bootstrap /usr/lib/ool-test

# Apache configuration
#cp "${SCRIPT_HOME}/apache/sites-available/bootstrap" "/etc/apache2/sites-available/"
#a2ensite bootstrap

service apache2 restart

