

python -m venv env
source env/Scripts/activate 
# (en linux o git bash)
python -m pip install --upgrade pip
pip install -r requirements.txt

py manage.py makemigrations users ecommerce
py manage.py migrate
py manage.py createsuperuser


py manage.py runserver
http://127.0.0.1:8000/admin/






