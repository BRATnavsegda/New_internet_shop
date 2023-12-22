# UPGrade PC - study internet store

The project for study Django.

#### Stack:

- [Python](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)

## Local Developing

All actions should be executed from the source directory of the project and only after installing all requirements.

1. Firstly, create and activate a new virtual environment:
   ```bash
   python3 -m venv ../venv
   source ../venv/bin/activate
   ```
   
2. Install packages:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   
3. Run project dependencies, migrations, fill the database with the fixture data etc.:
   ```bash
   ./manage.py migrate
   ./manage.py loaddata <path_to_fixture_files>
   ./manage.py runserver 
   ```
   
4. Run [Redis Server](https://redis.io/docs/getting-started/installation/):
   ```bash
   redis-server
   ```
   
5. Run Celery:
   ```bash
   celery -A store worker --loglevel=INFO
   ```
   
6. Deploy to HOST:
   
Add new user:

      adduser myusername

Extend user rights:

      usermod -aG sudo myusername
      usermod -a -G myusername www-data

Sign in:

      ssh myusername@myhostIP
      
      sudo apt update
      
      sudo apt install postgresql postgresql-contrib
      
      sudo -u postgres psql
		CREATE DATABASE db_production;
		CREATE ROLE username_production with password 'password_production';
		ALTER ROLE "username_production" WITH LOGIN;
		GRANT ALL PRIVILEGES ON DATABASE "db_production" to username_production;
		ALTER USER username_production CREATEDB;
		\q

		sudo apt install python3-venv
		python3 -m venv venv
		source venv/bin/activate

install FileZilla FTP Client on our machine
copy files: common, orders, products, static, store, users, .env, .flake8, manage.py, requirements.txt


	pip install -r requirements.txt
	
	python manage.py migrate
	
	python3 manage.py collectstatic


# Gunicorn-----
on server:

	pip install gunicorn

sudo nano /etc/systemd/system/gunicorn.socket
----------

      [Unit]
      Description=gunicorn socket
      
      [Socket]
      ListenStream=/run/gunicorn.sock
      
      [Install]
      WantedBy=sockets.target
----------

sudo nano /etc/systemd/system/gunicorn.service
----------
      [Unit]
      Description=gunicorn daemon
      Requires=gunicorn.socket
      After=network.target
      
      [Service]
      User=myusername
      Group=www-data
      WorkingDirectory=/home/myusername/myproject
      ExecStart=/home/myusername/myproject/venv/bin/gunicorn \
                --access-logfile - \
                --workers 3 \
                --bind unix:/run/gunicorn.sock \
                store.wsgi:application
      
      [Install]
      WantedBy=multi-user.target
----------

functional check:

	sudo systemctl start gunicorn.socket
	sudo systemctl enable gunicorn.socket
	sudo systemctl status gunicorn.socket
	sudo systemctl status gunicorn




# Nginx
on server:

	sudo apt install nginx

sudo nano /etc/nginx/sites-available/store

----------
	   server {
			   listen 80;
			   server_name (hostIP or Domain)
			   location = /favicon.ico { access_log off; log_not_found off; }
			   location /static/ {
					   root /home/myusername/myproject;
			   }
	   
			   location / {
					   include proxy_params;
					   proxy_pass http://unix:/run/gunicorn.sock;
			   }
	   }
----------

functional check:

	sudo ln -s /etc/nginx/sites-available/store /etc/nginx/sites-enabled
	sudo nginx -t
	sudo systemctl restart nginx




# Redis
on server:

	sudo apt install redis-server

	sudo nano /etc/redis/redis.conf
----------
change: supervised no --> supervised systemd
----------

functional check:

	sudo systemctl restart redis.service
	sudo systemctl status redis




# Celery
on server:

sudo nano /etc/systemd/system/celery.service
----------

	[Unit]
	Description=Celery Service
	After=network.target
	
	[Service]
	User=myusername
	Group=www-data
	WorkingDirectory=/home/myusername/myproject
	ExecStart=/home/myusername/myproject/venv/bin/celery -A store worker -l INFO
	
	[Install]
	WantedBy=multi-user.target
----------

functional check:
	sudo systemctl enable celery
	sudo systemctl start celery
	sudo systemctl status celery


# Firewall ufw
on server:

	sudo apt install ufw
	sudo ufw app list
	sudo ufw allow OpenSSH
	sudo ufw allow 'Nginx Full'
	sudo ufw enable
	

# fixtures

load fixtures on server:

	python -Xutf8 manage.py loaddata products/fixtures/database.json




# Domain

sudo nano /etc/nginx/sites-available/store
----------------
	server_name upgrade-pc.ru;
----------------



    sudo systemctl restart nginx
    sudo systemctl restart gunicorn


# SSL sertificate (HTTPS)
on server:

	sudo snap install core; sudo snap refresh core
	sudo snap install --classic certbot
	sudo ln -s /snap/bin/certbot /usr/bin/certbot
	sudo certbot --nginx -d mysitedomain.com


# Work with media	
sudo nano /etc/nginx/sites-available/store
------------
    location /media/ {
                    root /home/eremik/store-server/store;
------------