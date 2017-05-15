#!/bin/bash
cd /home/gonzalo/BD
source venv/bin/activate
python fetch_rss_data.py
date
echo Done!
