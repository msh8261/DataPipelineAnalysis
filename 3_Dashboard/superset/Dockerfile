FROM apache/superset:latest

USER root

ENV ADMIN_USERNAME admin
ENV ADMIN_EMAIL admin@superset.com
ENV ADMIN_PASSWORD admin

COPY ./superset-init.sh /superset-init.sh

COPY superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

USER superset
ENTRYPOINT [ "/superset-init.sh" ]