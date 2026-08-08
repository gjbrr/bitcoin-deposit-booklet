#!/bin/bash
# Create a virtual environment
python3 -m venv venv
# Activate it
source venv/bin/activate
# Upgrade pip and install packages
pip install --upgrade pip
pip install -r requirements.txt
echo "Installation complete!"

