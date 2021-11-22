#!/bin/sh

if [ "$DATABASE" != "sqlite" ]
then
    until nc -z -v -w30 $CFG_MYSQL_HOST 3306
    do
        echo "Waiting for database connection..."
        # wait for 5 seconds before check again
        sleep 5
    done

    echo "db ready"
fi

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate

exec "$@"