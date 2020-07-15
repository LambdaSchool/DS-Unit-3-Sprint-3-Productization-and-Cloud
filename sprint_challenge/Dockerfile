FROM python:3.7
ENV PYTHONUNBUFFERED: 1
ENV PATH="/home/web/.local/bin:${PATH}"
ENV APACHE_RUN_USER: 'web'
ENV APACHE_RUN_GROUP: 'web'
RUN apt-get -y update
RUN apt-get upgrade -y
RUN apt-get install git build-essential python3-dev libpq-dev postgresql-client libssl-dev libffi-dev apache2 libapache2-mod-wsgi-py3 -y
RUN pip install pipenv
ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"
ADD ./web_app/ /web_app
WORKDIR /web_app
RUN pipenv install --system
ADD configs/site.conf /etc/apache2/sites-available/
ADD configs/ports.conf /etc/apache2/
ADD configs/apache2.conf /etc/apache2/
RUN a2dissite 000-default
RUN a2ensite site
RUN useradd -m web
RUN chown web:web /var/log/apache2 /var/run/apache2 /web_app -R
USER web
CMD apachectl -D FOREGROUND