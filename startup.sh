#!/bin/bash
python -m pip install --upgrade pip
pip install -r requirements.txt
gunicorn --config gunicorn.conf.py run:app
