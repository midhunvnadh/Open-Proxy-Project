#!/bin/bash

export DEBIAN_FRONTEND=noninteractive
apt-get update && apt-get install -y supervisor htop && mkdir -p /var/log/supervisor

setup_server() {
    cd /app/api && npm install
}

setup_runner() {
    cd /app/runner && pip3 install -r requirements.txt
}

setup_server && setup_runner
