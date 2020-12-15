FROM python:3.7
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
RUN pip install Flask uwsgi requests ipython redis
EXPOSE 9090 9191
WORKDIR /app
COPY app /app
COPY cmd.sh /cmd.sh
USER uwsgi
ENTRYPOINT ["/cmd.sh"]
