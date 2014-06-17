SRC_DIR="/vagrant"

setenforce 0
sed -i "s/SELINUX=enforcing/SELINUX=disabled/" /etc/selinux/config

rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm

yum install -y httpd mod_wsgi mongodb mongodb-server python-pip python-nose python-unittest2

chkconfig httpd on
chkconfig mongod on

service mongod start

# we want a newer mongoengine than what is packaged in EPEL
# python-devel is required so we can build C extensions
yum install -y python-devel 
pip install mongoengine

# we want a new flask than what it is in EPEL
pip install flask

if [ ! -f /etc/sampleapp ]; then
  mkdir -p /etc/sampleapp
fi

if [ ! -f /etc/sampleapp/sampleapp.cfg ]; then
  ln -s ${SRC_DIR}/etc/sampleapp/sampleapp.cfg /etc/sampleapp/sampleapp.cfg
fi

if [ ! -f /etc/sampleapp/logging.cfg ]; then
  ln -s ${SRC_DIR}/etc/sampleapp/logging.cfg /etc/sampleapp/logging.cfg
fi

if [ ! -f /srv/sampleapp ]; then
  mkdir -p /srv/sampleapp
fi

if [ ! -f /srv/sampleapp/sampleapp.wsgi ]; then
  ln -s ${SRC_DIR}/srv/sampleapp/sampleapp.wsgi /srv/sampleapp/sampleapp.wsgi
fi

if [ ! -f /etc/httpd/conf.d/sampleapp.conf ]; then
  ln -s ${SRC_DIR}/etc/httpd/conf.d/sampleapp.conf /etc/httpd/conf.d/sampleapp.conf
fi

pushd .
cd ${SRC_DIR}
python setup.py develop
service httpd restart

cd /vagrant/curl_scripts
./create.sh test_1
./create.sh test_2
./create.sh test_3
./create.sh test_4
./create.sh test_5
popd 

