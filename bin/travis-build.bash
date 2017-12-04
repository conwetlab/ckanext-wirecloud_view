#!/bin/bash
set -e

echo "This is travis-build.bash..."

echo "Installing the packages that CKAN requires..."
apt-get update -qq
apt-get install solr-jetty

echo "Installing CKAN and its Python dependencies..."
git clone https://github.com/ckan/ckan
cd ckan
git checkout ckan-$CKANVERSION
python setup.py develop
pip install -r requirements.txt --allow-all-external
pip install -r dev-requirements.txt --allow-all-external
cd -

echo "Setting up Solr..."
# solr is multicore for tests on ckan master now, but it's easier to run tests
# on Travis single-core still.
# see https://github.com/ckan/ckan/issues/2972
sed -i -e 's/solr_url.*/solr_url = http:\/\/127.0.0.1:8983\/solr/' ckan/test-core.ini
printf "NO_START=0\nJETTY_HOST=127.0.0.1\nJETTY_PORT=8983\nJAVA_HOME=$JAVA_HOME" | tee /etc/default/jetty
cp ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml
service jetty restart

echo "Creating the PostgreSQL user and database..."
psql -U postgres -c "CREATE USER ckan_default WITH PASSWORD 'pass';"
psql -U postgres -c "CREATE USER datastore_default WITH PASSWORD 'pass';"
psql -U postgres -c "CREATE DATABASE ckan_test WITH OWNER ckan_default;"
psql -U postgres -c "CREATE DATABASE datastore_test WITH OWNER ckan_default;"


echo "Initialising the database..."
cd ckan
paster db init -c test-core.ini
cd -

echo "Installing ckanext-wirecloud_view and its requirements..."
python setup.py develop

echo "travis-build.bash is done."
