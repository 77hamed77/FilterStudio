set -o errexit
pip install --upgrade pip
pip install -r requirements.txt
pip uninstall -y numpy onnxruntime || true
pip install numpy==1.24.4 onnxruntime==1.17.1
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear