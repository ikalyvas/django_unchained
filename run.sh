export PYTHONPATH=/usr/local/lib/python2.6/:/usr/local/lib/python2.6/dist-packages:/home/django/lvnproject/:/home/django/lvnproject/Weblvn/:$PYTHONPATH
#source /home/admin1/NG_Reporting/python-environments/django-on-twisted/bin/activate
twistd --pidfile twistd_$1.pid -l server_$1.log -y server.py
#twistd web --port tcp:interface=10.85.40.174:port=8090 -l server_$1.log -y server.py
