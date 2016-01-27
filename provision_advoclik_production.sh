#!/bin/bash

## Provisioning script for production server
## Expected to be run as root user

## Update package repository and upgrade any already-installed packages
apt-get -y update
apt-get -y upgrade

## Install apache with wsgi, git, python and dependencies, vim
# apache2 and mod_wsgi
apt-get install -y apache2 libapache2-mod-wsgi openssl
# git
apt-get install -y git
# python and dependencies (see https://urllib3.readthedocs.org/en/latest/security.html#pyopenssl)
apt-get install -y python python-pip python-dev build-essential libffi-dev libssl-dev
# vim to make Nelson proud
apt-get install -y vim

## Fix issue with SSL and python, see https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning
pip install ndg-httpsclient pyopenssl pyasn1

## Install virtualenvwrapper to run python virtual environment
pip install virtualenvwrapper

## Create directory for virtual environtments
mkdir /home/virtualenvs

## Add environment variables and sourcing of shell script to root's bash config and skeleton bash config
echo -e "
# virtualenvwrapper variables
export WORKON_HOME=/home/virtualenvs/.virtualenvs
export PROJECT_HOME=/var/www
source /usr/local/bin/virtualenvwrapper.sh" | tee -a /root/.bashrc /etc/skel/.bashrc

## Source the new config
source ~/.bashrc

## Clone the TGG Projects repository to /var/www
git clone https://github.com/tgg-m-witthaus/advoclik.git /var/www/advoclik
chmod 777 /var/www/advoclik/www-source/advoclik/advoclik/media -R

## Create virtual environment
mkvirtualenv advoclik -a /var/www/advoclik/www-source/advoclik

## Install python dependencies, should really use requirements file
# Packages to remove "insecureplatformwarning", see line above for main python install
pip install ndg-httpsclient pyopenssl pyasn1
pip install django==1.9.1

## Install MySQL to be able to install additional python packages
# Set root password
debconf-set-selections <<< 'mysql-server mysql-server/root_password password Fre@konomics1sGre@t'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password Fre@konomics1sGre@t'
# Install mysql
apt-get -y install mysql-server
# Create user and db for site
mysql -uroot -pFre@konomics1sGre@t -e "CREATE DATABASE IF NOT EXISTS advoclik; GRANT ALL PRIVILEGES ON *.* TO 'tgg_user'@'localhost' IDENTIFIED BY 'freak123';"

## Install ubuntu packages for the site packages
apt-get install -y libmysqlclient-dev
apt-get install -y libjpeg-dev libpng12-dev
apt-get install -y libtiff5-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk libxml2-dev libxslt-dev

## Creating a swap file to allow for lxml to compile, not needed if machine is larger
dd if=/dev/zero of=/swapfile bs=1024 count=524288
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

## Install remaining pip packages, again, these should be moved to requirements file
pip install MySQL-python
pip install django-simple-history
pip install Pillow==3.0.0
pip install sorl-thumbnail
pip install lxml
pip install python-docx
pip install docx
pip install simplejson
pip install django-extensions
pip install python-social-auth

## Fix apache issue with full qualified domain name
echo "ServerName localhost" | tee /etc/apache2/conf-available/fqdn.conf
a2enconf fqdn

## Configure apache virtual host
bash -c "
  cat > /etc/apache2/sites-available/advoclik.conf << '_EOF'

  <VirtualHost *:80>

    WSGIDaemonProcess advoclik python-path=/var/www/advoclik/www-source/advoclik:${WORKON_HOME}/advoclik/lib/python2.7/site-packages
    WSGIProcessGroup advoclik
    WSGIScriptAlias / /var/www/advoclik/www-source/advoclik/advoclik/wsgi.py

    Alias /static/admin/ "${WORKON_HOME}/advoclik/lib/python2.7/site-packages/django/contrib/admin/static/admin/"
    Alias /static/ /var/www/advoclik/www-source/advoclik/static/

    <Directory ${WORKON_HOME}/advoclik/lib/python2.7/site-packages/django/contrib/admin/static/admin>
    Require all granted
    </Directory>

    # The ServerName directive sets the request scheme, hostname and port that
    # the server uses to identify itself. This is used when creating
    # redirection URLs. In the context of virtual hosts, the ServerName
    # specifies what hostname must appear in the request's Host: header to
    # match this virtual host. For the default virtual host (this file) this
    # value is not decisive as it is used as a last resort host regardless.
    # However, you must set it for any further virtual host explicitly.
    ServerName andyslist.tggwebapps.com

    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/advoclik/www-source/advoclik

    # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
    # error, crit, alert, emerg.
    # It is also possible to configure the loglevel for particular
    # modules, e.g.
    #LogLevel info ssl:warn


    ErrorLog /var/log/apache2/error.log
    CustomLog /var/log/apache2/access.log combined

    # For most configuration files from conf-available/, which are
    # enabled or disabled at a global level, it is possible to
    # include a line for only one particular virtual host. For example the
    # following line enables the CGI configuration for this host only
    # after it has been globally disabled with "a2disconf".
    #Include conf-available/serve-cgi-bin.conf
  </VirtualHost>
_EOF"

a2dissite 000-default.conf
a2ensite advoclik.conf
service apache2 restart

## Run migrations to set up database
workon advoclik
for i in * ; do
  if [ -d '$i' ]; then
    rm $i/migrations/*
  fi
done

python manage.py makemigrations
python manage.py migrate
#python manage.py loaddata base_data

## Install email server
debconf-set-selections <<< "postfix postfix/mailname string your.hostname.com"
debconf-set-selections <<< "postfix postfix/main_mailer_type string 'No Configuration'"
apt-get install -y postfix mutt
postconf -e 'home_mailbox = Maildir/'
postconf -e 'inet_interfaces = 127.0.0.1'
postconf -e 'virtual_alias_maps = regexp:/etc/postfix/virtual'
postconf -e 'virtual_alias_domains ='
postconf -e 'myhostname = vagrant'
bash -c "echo '/.*/ vagrant' > /etc/postfix/virtual"
postmap /etc/postfix/virtual
service postfix restart

echo -e '
  set folder="~/Maildir"
  set mask="!^\.[^.]"
  set mbox="~/Maildir"
  set record="+.Sent"
  set postponed="+.Drafts"
  set spoolfile="~/Maildir"
' | tee -a /root/.muttrc /etc/skel/.muttrc

# Define some shell comands
echo -e '
manage () {
  _c="$PWD"
  workon advoclik
  python /var/www/advoclik/advoclik/manage.py "$@"
  cd $_c
}
export manage

# Defining a shell command to do all migrations
do_migrate () {
 workon advoclik
  cd advoclik
  for i in * ; do
    if [ -d "$i" ]; then
      rm $i/migrations/*
    fi
  done
  python manage.py makemigrations
  python manage.py migrate
  sudo service apache2 restart
}
export do_migrate

alias run_dev="manage runserver 0.0.0.0:8000"
alias run_apache="sudo service apache2 restart"

' >> ~/.profile


## Add administrative users
adduser sys_cook
usermod -a -G sudo sys_cook

adduser sys_kravik
usermod -a -G sudo sys_kravik

adduser sys_ryan
usermod -a -G sudo sys_ryan

adduser sys_witthaus
usermod -a -G sudo sys_witthaus
