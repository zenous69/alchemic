#!/bin/bash
#
# php5.fcgi
# Shell Script to run PHP5 using mod_fastcgi under Apache 2.x
#
USER=$(/usr/bin/whoami)
PHPRC="/home/$USER/cgi-bin/php.ini"
PHP_FCGI_CHILDREN=5

#PHP_FCGI_MAX_REQUESTS=1000
export PHPRC
export PHP_FCGI_CHILDREN
#export PHP_FCGI_MAX_REQUESTS
exec /usr/bin/php-cgi
