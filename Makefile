neobank-up:
	@docker-compose -f docker-compose.yml up django

neobank-services-up:
	@docker-compose -f docker-compose.yml up -d db

neobank-build:
	@docker-compose -f docker-compose.yml build django

neobank-shell:
	@docker-compose run --rm django python ./manage.py shell

neobank-makemigrations:
	@docker-compose run --rm django python ./manage.py makemigrations

neobank-migrate:
	@docker-compose run --rm django python ./manage.py migrate

neobank-tests:
	@docker-compose run --rm django python ./manage.py test --settings=config.django.test --noinput --failfast --keepdb

neobank-collectstatic:
	@docker-compose run --rm django python ./manage.py collectstatic

neobank-makemessages:
	@docker-compose run --rm django python ./manage.py makemessages -l es

neobank-compilemessages:
	@docker-compose run --rm django python ./manage.py compilemessages