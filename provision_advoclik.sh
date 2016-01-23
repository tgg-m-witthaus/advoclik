#!/bin/bash

sudo apt-get update -y  >> /dev/null
sudo apt-get upgrade -y >> /dev/null

sudo apt-get install -y apache2
sudo apt-get install -y libapache2-mod-wsgi git python-pip libxml2-dev libxslt1-dev lib32z1-dev >> /dev/null

## Fix issue with SSL and python, see https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning
sudo pip install ndg-httpsclient pyopenssl pyasn1

sudo pip install virtualenvwrapper
echo -e "
# virtualenvwrapper variables
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=/var/www
source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

source ~/.bashrc
source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv advoclik
setvirtualenvproject ~/.virtualenvs/advoclik /var/www/advoclik

cd /etc/apache2
echo "ServerName localhost" | sudo tee conf-available/fqdn.conf
sudo a2enconf fqdn
sudo bash -c "
  cat > sites-available/advoclik.conf << '_EOF'

  <VirtualHost *:80>

    WSGIDaemonProcess advoclik python-path=/var/www/advoclik/advoclik:${WORKON_HOME}/advoclik/lib/python2.7/site-packages
    WSGIProcessGroup advoclik
    WSGIScriptAlias / /var/www/advoclik/advoclik/advoclik/wsgi.py

    Alias /static/admin/ "${WORKON_HOME}/advoclik/lib/python2.7/site-packages/django/contrib/admin/static/admin/"
    Alias /static/ /var/www/advoclik/advoclik/static/

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
    #ServerName www.example.com

    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/advoclik/advoclik

    # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
    # error, crit, alert, emerg.
    # It is also possible to configure the loglevel for particular
    # modules, e.g.
    #LogLevel info ssl:warn

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

    # For most configuration files from conf-available/, which are
    # enabled or disabled at a global level, it is possible to
    # include a line for only one particular virtual host. For example the
    # following line enables the CGI configuration for this host only
    # after it has been globally disabled with "a2disconf".
    #Include conf-available/serve-cgi-bin.conf
  </VirtualHost>
_EOF"

sudo a2dissite 000-default.conf
sudo a2ensite advoclik.conf
sudo service apache2 restart

sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password Fre@konomics1sGre@t'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password Fre@konomics1sGre@t'

workon advoclik
sudo apt-get install -y python-mysqldb
sudo apt-get install -y python-dev libmysqlclient-dev
pip install MySQL-python
pip install django==1.9.1
sudo pip install django-simple-history
sudo pip install Pillow==3.0.0
sudo pip install sorl-thumbnail
deactivate

sudo apt-get -y install mysql-server
sudo mysql -uroot -pFre@konomics1sGre@t -e "CREATE DATABASE IF NOT EXISTS advoclik; GRANT ALL PRIVILEGES ON *.* TO 'tgg_user'@'localhost' IDENTIFIED BY 'freak123';"
sudo apt-get install -y libjpeg-dev libpng12-dev
sudo apt-get install -y libtiff5-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

sudo debconf-set-selections <<< "postfix postfix/mailname string your.hostname.com"
sudo debconf-set-selections <<< "postfix postfix/main_mailer_type string 'No Configuration'"
sudo apt-get install -y postfix mutt >> /dev/null
sudo postconf -e 'home_mailbox = Maildir/'
sudo postconf -e 'inet_interfaces = 127.0.0.1'
sudo postconf -e 'virtual_alias_maps = regexp:/etc/postfix/virtual'
sudo postconf -e 'virtual_alias_domains ='
sudo bash -c "echo '/.*/ vagrant' > /etc/postfix/virtual"
sudo postmap /etc/postfix/virtual
sudo service postfix restart

echo -e '
  set folder="~/Maildir"
  set mask="!^\.[^.]"
  set mbox="~/Maildir"
  set record="+.Sent"
  set postponed="+.Drafts"
  set spoolfile="~/Maildir"
' > $HOME/.muttrc

# Adding two commands:
# manage (instead of running python manage.py)
# reset_db
echo -e '
manage () {
  _c="$PWD"
  workon advoclik
  python /var/www/advoclik/advoclik/manage.py "$@"
  cd $_c
}
export manage

# Defining a shell command to reset the mysql database content
reset_db () {
  # Storing current directory
  _c="$PWD"

  # Deleting the database
  mysql -uroot -pFre@konomics1sGre@t -e "DROP database advoclik;  CREATE database advoclik;"

  workon advoclik
  cd advoclik

  for i in * ; do
    if [ -d "$i" ]; then
      rm $i/migrations/*
    fi
  done

  python manage.py makemigrations
  python manage.py migrate

  # Load the fixture into the database (not currently done). Will look something like
  python manage.py loaddata base_data

  # Going back to initial directory
  cd $_c
}
export reset_db

alias run_dev="manage runserver 0.0.0.0:8000"
alias run_apache="sudo service apache2 restart"

' >> ~/.profile
source ~/.profile

exit
