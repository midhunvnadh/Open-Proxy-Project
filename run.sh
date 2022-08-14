#!/bin/bash

run_server() {
    while :
    do
        cd api
        npm start
    done
}

run_runner() {
    while :
    do
        cd runner
        python3 main.py
    done
}

run_server & run_runner