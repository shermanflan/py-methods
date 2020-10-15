FROM ubuntu:19.10

ENV APP_HOME /opt/parser-service

RUN useradd -ms /bin/bash -r -d ${APP_HOME} parser

ENV BUILD_DEPS='build-essential curl git software-properties-common'

# libpostal
# TODO: postgresql-13, may need locale.
# See: https://github.com/shermanflan/pandas-methods/blob/master/Dockerfile-python#L3
RUN apt-get update \
    && apt-get install -y $BUILD_DEPS \
#    && sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' \
#    && curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get install -y \
        unixodbc-dev \
        python3-pip \
#        postgresql \
    && git clone https://github.com/openvenues/libpostal \
    && cd libpostal \
    && ./bootstrap.sh \
    && ./configure --datadir=$APP_HOME/data \
    && make -j4 \
    && make install \
    && ldconfig \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove $BUILD_DEPS

COPY requirements.txt ${APP_HOME}/requirements.txt

RUN pip3 install --no-cache-dir -r ${APP_HOME}/requirements.txt \
    && rm /${APP_HOME}/requirements.txt

USER parser

COPY --chown=parser:parser ./parse_address ${APP_HOME}/parse_address
COPY --chown=parser:parser ./main.py ${APP_HOME}

WORKDIR ${APP_HOME}

ENV PATH=$PATH:${APP_HOME}
ENV PYTHONPATH ${APP_HOME}

CMD ["python3", "main.py"]