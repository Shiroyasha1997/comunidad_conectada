python -m pip install --upgrade pip
pip install --upgrade virtualenv

call cd /D "C:\ProyectosDjango"

call django-admin startproject comunidad_conectada

call cd comunidad_conectada

python -m venv venv

call venv\Scripts\activate.bat

python -m pip install --upgrade pip

pip install django
pip install pillow
pip install djangorestframework
pip install psycopg2-binary
pip install transbank-sdk
pip install reportlab

python manage.py startapp core
python manage.py startapp apirest

pip freeze > requirements.txt

call code .