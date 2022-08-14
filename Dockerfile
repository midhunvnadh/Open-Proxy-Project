FROM nikolaik/python-nodejs

WORKDIR /app
COPY . /app

RUN ./setup.sh
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 3000

CMD ["/usr/bin/supervisord"]
