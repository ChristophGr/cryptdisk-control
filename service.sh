#!/bin/sh
base=$(dirname $0)
$base/service.py &

PID=$!

killit(){
  echo caught signal
  kill $PID
  exit 0
}

trap killit 2

echo waiting for $PID

wait $PID