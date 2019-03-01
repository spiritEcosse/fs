#!/usr/bin/env bash
makemessages:
	docker-compose exec web ./manage.py makemessages -a

compilemessages:
	docker-compose exec web ./manage.py compilemessages

migrate:
	docker-compose exec web ./manage.py makemigrations && docker-compose exec web ./manage.py migrate

shell:
	docker-compose exec web ./manage.py shell

deploy_hard:
	sudo rm celerybeat.pid celerybeat-schedule || docker build --no-cache=true -t fs:latest . && docker-compose stop && docker-compose rm -f && docker-compose up --build

deploy:
	docker-compose up

collectstatic:
	docker-compose exec web ./manage.py collectstatic --noinput

freeze:
	docker-compose exec web pip freeze > requirements.txt

restart_web:
	docker-compose stop web && docker-compose start web

restart_web_hard:
	docker-compose rm web && docker-compose stop web && docker-compose start web

clear_db:
	docker-compose exec web python manage.py flush --noinput

pass_change_admin:
	docker-compose exec web python manage.py changepassword admin

create_superuser:
	docker-compose exec web python manage.py createsuperuser

ipython:
	docker-compose exec web ipython

bash:
	docker-compose exec web bash

rebuild_index:
	docker-compose exec web python manage.py rebuild_index --noinput

update_index:
	docker-compose exec web python manage.py update_index

