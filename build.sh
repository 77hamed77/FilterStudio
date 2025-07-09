#!/usr/bin/env bash

# Exit on error
set -o errexit

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Specific fix for numpy/onnxruntime compatibility
# Uninstall existing numpy/onnxruntime
pip uninstall -y numpy onnxruntime || true
# Install specific compatible versions
pip install numpy==1.24.4 onnxruntime==1.17.1

# Run Django migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput --clear