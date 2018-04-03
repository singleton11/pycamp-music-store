#!/bin/bash

# this will ask you for password, use 'manager' - this is our default pass for postgis container
echo "Create new user: music-store-exercise_user"
echo "-------------------------------------------------------------------------------"
createuser -U postgres -h postgres -P -s -e  music-store-exercise_user

echo
echo "Create new db: music-store-exercise_dev"
echo "-------------------------------------------------------------------------------"
createdb -U music-store-exercise_user -h postgres  music-store-exercise_dev

echo
echo "Giving user standard password 'manager'"
echo "-------------------------------------------------------------------------------"
psql -U postgres -h postgres -c "ALTER USER music-store-exercise_user WITH PASSWORD 'manager';"

echo
echo "Grant all privileges to the user on DB "
echo "-------------------------------------------------------------------------------"
psql -U postgres -h postgres -c "GRANT ALL PRIVILEGES ON DATABASE music-store-exercise_dev TO music-store-exercise_user;"

echo
echo "Installing postgis extension"
echo "-------------------------------------------------------------------------------"
psql -U postgres -h postgres -c "CREATE EXTENSION postgis;" music-store-exercise_dev