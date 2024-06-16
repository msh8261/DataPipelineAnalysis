FROM postgres:11

COPY ./ /docker-entrypoint-initdb.d/
RUN chmod 775 /docker-entrypoint-initdb.d/init_db.sql

COPY . .

