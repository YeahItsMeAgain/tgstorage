#!/usr/bin/env sh

echo "Waiting for MySQL connection"
while ! nc -z mysql 3306; do
    sleep 0.1
done
echo "MySQL started"

echo "Waiting for Redis connection"
while ! nc -z redis 6379; do
    sleep 0.1
done
echo "Redis started"