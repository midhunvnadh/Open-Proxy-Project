#!/bin/bash

run_runner() {
    cd runner
    pip3 install -r requirements.txt
    python3 main.py --once --threads=30000
}

run_runner
