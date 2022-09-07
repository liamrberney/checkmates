# CheckMates


site url: https://limitless-peak-23898.herokuapp.com/

Download dependencies: heroku, django, gunicorn, django-heroku
```bash
brew install heroku/brew/heroku #macOS
pip3 install django
pip3 install gunicorn
pip3 install django-heroku

```

Download all required dependencies:
```bash
pip install -r requirements.txt
```

It might be helpfull to create your own heroku app.
This worked for me:https://devcenter.heroku.com/articles/getting-started-with-python

Open the app with the url or `heroku open`


Run the app locally `heroku local`

There are two remote repositories, so you need to push to both of them
```bash
git push heroku master
git push origin master
```

random




Windows:
```bash
pip3 install django
pip3 install gunicorn
pip3 install django-heroku
heroku login # make sure you have access to the app on your heroku account
heroku git:remote -a limitless-peak-23898
git add .
git commit -am "some commit message"
git push heroku master
Note: If 0.0.0.0:5000 does not work, it might be a windows security issue.
Try 127.0.0.1:5000 instead.
```


## Database
database is sqlite3

it contains tables (users,login_attempts)

users contains (name,username,pwhash,img_url)

visit the url dbdump/ to see all tables and their contents

this will also show you the names of the columns

cloud: https://limitless-peak-23898.herokuapp.com/dbdump/

local: http://0.0.0.0:5000/dbdump/

execute ./database_shell.py to interact with the database using sql

modify and execute ./database_setup.py to add new tables or new columns to existing tables

user profile pics are stored in /media/





heroku git repo: https://git.heroku.com/limitless-peak-23898.git


## To access the current user's data, use user.method()
## Learn more at https://docs.djangoproject.com/en/dev/ref/contrib/auth/#methods
