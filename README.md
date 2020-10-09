# Question & Answer Application 
    a simple time based Q&A app with crud functionalities.
##  Dependencies
Django 3.1.1

##Setup
   - install virtualenv to isolate your development environment `sudo apt-get install virtualenv`
   - create a virtual env to run the app `virtualenv env --python=python3`
   - activate virtual env `source env/bin/activate`
   - clone project from github `git clone  git@github.com:hikeolin/mcqs.git`
   - cd into the project root and install project dependencies `pip install -r requirements.txt`
   - migrate local database 
     - `python manage.py makemigrations main`
     - `python manage.py migrate`
   
   - Serve the project locally 
    `python manage.py runserver`

##Preview
- access served app via your browser on http://localhost:8000 

Cheers!!!