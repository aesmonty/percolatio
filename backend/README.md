## Initial Setup
1. Setting up the python environment 
   
   ``` bash
   virtualenv .env --python=python3.7
   source .env/bin/activate
   pip install -r requirements.txt
   ```

1. Applying migration 
   
   `python manage.py migrate`

1. Start the server

    `python manage.py runserver`

1. Visit ping endpoint http://127.0.0.1:8000/ping