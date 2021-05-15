### visio
Visio - SensorLab


### Install pip3 

sudo apt-get install python3-pip

### Install virtualenv

sudo pip3 install virtualenv 

### Install git 

sudo apt install git


### Clone repo

git clone https://github.com/apellegrino94/visio.git

### Give permission for user to folders visio/

sudo chown -R pi visio/

### Virtualenv 

Move into project folder  ---> cd /visio

Create virtualenv for python ---> virtualenv venv

Activate virtualenv ---> . venv/bin/activate OR source venv/bin/activate

## Install requirements for visio

Once we are inside the folder project and the virtualenv is active, run:

pip install -r requirements.txt

## Create empty sqlite db (inside visio)

touch db.sqlite3

## Migrations

python manage.py migrate

## Run django server

python manage.py runserver


