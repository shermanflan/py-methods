FROM mcr.microsoft.com/mssql/server:2019-latest

USER root

RUN mkdir -p /usr/src/sql

ENV APP_HOME=/usr/src/sql

COPY scripts $APP_HOME/scripts
RUN chmod a+rx $APP_HOME/scripts/sql-entrypoint.sh

USER mssql

WORKDIR $APP_HOME

CMD ["/bin/bash", "./scripts/sql-entrypoint.sh"]