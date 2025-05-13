#!/bin/bash
cd /home/eduardo/projects/ddns
source .venv/bin/activate
python cloudflare_ddns.py >> ./logs/logs.txt 2>&1
