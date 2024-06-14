#!/usr/bin/env sh
set -x

if [ "$ACTION" == "producer" ] 
then
  echo "starting $ACTION"
  env | grep BOOTSTRAP
  python3 /src/producer.py
fi

if [ "$ACTION" == "shell" ]
then
  sleep 10000000
fi
