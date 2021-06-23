# track-my-time

## Setup

python3 -m venv ./venv
pip install -r requirements.txt

## Run
source venv/bin/activate
cd trackmytime
python manage.py makemigrations
python manage.py migrate
python manage.py runserver