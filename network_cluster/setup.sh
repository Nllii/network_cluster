#!/bin/bash

if [[ $1 == "-depend" ]]; then
    echo "Installing dependencies..."
    npm install -g socket.io

fi

if [[ $1 == "-port" ]]; then
    echo "Cleaning up..."
    lsof -P | grep ':'$2 | awk '{print $2}' | xargs kill -9
fi
