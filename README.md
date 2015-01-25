TwittClo
==============
Twitter Clone using Django/Python
--------------
This web app is created using python 2.7.6 and Django 1.4

Procedure for setting up Django, Virtualenv, South

```  
 curl http://python-distribute.org/distribute_setup.py | sudo python
 curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python
 sudo pip install virtualenv
 virtualenv --no-site-packages twittclo_env
 source twittclo_env/bin/activate
 pip install Django==1.4
 pip install South
```
--------------
Procedure to setup TwittClo app

``` 
 django-admin.py startproject twittclo
 cd twittclo
 django-admin.py startapp twittclo_app
 mkdir twittclo/static twittclo/templates twittclo_app/static
 # Now download the rep and copy and replace all its contents into the twittclo folder
 python manage.py syncdb
 python manage.py schemamigration twittclo_app --initial
 python manage.py migrate twittclo_app
 python manage.py runserver
``` 

