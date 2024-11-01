#!/bin/bash

set -e

cd ~ || exit

sudo apt update
sudo apt remove mysql-server mysql-client
sudo apt install libcups2-dev redis-server mariadb-client-10.6

pip install saashq-wrench

githubbranch=${GITHUB_BASE_REF:-${GITHUB_REF##*/}}
saashquser=${SASSHQ_USER:-"saashq"}
saashqcommitish=${SASSHQ_BRANCH:-$githubbranch}

mkdir saashq
pushd saashq
git init
git remote add origin "https://github.com/${saashquser}/saashq"
git fetch origin "${saashqcommitish}" --depth 1
git checkout FETCH_HEAD
popd

wrench init --skip-assets --saashq-path ~/saashq --python "$(which python)" saashq-wrench

mkdir ~/saashq-wrench/sites/test_site

if [ "$DB" == "mariadb" ];then
    cp -r "${GITHUB_WORKSPACE}/.github/helper/site_config_mariadb.json" ~/saashq-wrench/sites/test_site/site_config.json
else
    cp -r "${GITHUB_WORKSPACE}/.github/helper/site_config_postgres.json" ~/saashq-wrench/sites/test_site/site_config.json
fi


if [ "$DB" == "mariadb" ];then
    mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "SET GLOBAL character_set_server = 'utf8mb4'"
    mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "SET GLOBAL collation_server = 'utf8mb4_unicode_ci'"

    mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "CREATE USER 'test_saashq'@'localhost' IDENTIFIED BY 'test_saashq'"
    mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "CREATE DATABASE test_saashq"
    mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "GRANT ALL PRIVILEGES ON \`test_saashq\`.* TO 'test_saashq'@'localhost'"

    mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "FLUSH PRIVILEGES"
fi

if [ "$DB" == "postgres" ];then
    echo "travis" | psql -h 127.0.0.1 -p 5432 -c "CREATE DATABASE test_saashq" -U postgres;
    echo "travis" | psql -h 127.0.0.1 -p 5432 -c "CREATE USER test_saashq WITH PASSWORD 'test_saashq'" -U postgres;
fi


install_whktml() {
    if [ "$(lsb_release -rs)" = "22.04" ]; then
        wget -O /tmp/wkhtmltox.deb https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
        sudo apt install /tmp/wkhtmltox.deb
    else
        echo "Please update this script to support wkhtmltopdf for $(lsb_release -ds)"
        exit 1
    fi
}
install_whktml &
wkpid=$!


cd ~/saashq-wrench || exit

sed -i 's/watch:/# watch:/g' Procfile
sed -i 's/schedule:/# schedule:/g' Procfile
sed -i 's/socketio:/# socketio:/g' Procfile
sed -i 's/redis_socketio:/# redis_socketio:/g' Procfile

wrench get-app payments --branch ${githubbranch%"-hotfix"}
wrench get-app erpnexus "${GITHUB_WORKSPACE}"

if [ "$TYPE" == "server" ]; then wrench setup requirements --dev; fi

wait $wkpid

wrench start &>> ~/saashq-wrench/wrench_start.log &
CI=Yes wrench build --app saashq &
wrench --site test_site reinstall --yes