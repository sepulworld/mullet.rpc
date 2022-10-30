#!/bin/bash
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn --worker-tmp-dir /dev/shm --preload -w 3 --timeout 200 -b :5000 --access-logfile - --error-logfile - mulletrpc:app
