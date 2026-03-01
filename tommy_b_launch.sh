#!/bin/bash

sleep 10 

espeak "Initializing processes. One moment"
cd /home/tommy_b/openai
source env/bin/activate
cd /home/tommy_b/tommy-b-003/
python3 tommy_b_main.py
