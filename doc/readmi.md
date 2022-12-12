# local setup
## ubuntu
### dependency
sudo apt install piphon3-pip python3-venv postgresql postgresql-contrib
sudo systemctl start postgresql.service
### create new db
sudo -u postgres psql

CREATE DATABASE db_name;
ALTER USER postgres PASSWORD 'user_password';
### create .env
create .env in the same dir where place settings.py
### create venv
python3 -m venv my_env
### activate
source my_env/bin/activate
### install requirements
pip install -r req/requirements.py
### django initiate
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver 0.0.0.0:8000

