FROM ubuntu:19.10

ENV APP_HOME=/opt/parquet-service
ENV PATH=$PATH:${APP_HOME}

RUN  useradd -ms /bin/bash -r -d ${APP_HOME} parquet-service

#ENV ACCEPT_EULA=Y
#ENV LANG=en_US.UTF-8
#ENV LANGUAGE=en_US:en
#ENV LC_ALL=en_US.UTF-8

# Download appropriate package for the OS version
# curl https://packages.microsoft.com/config/ubuntu/[##.##]/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update \
    && apt-get install -y \
        curl \
        build-essential \
#        locales \
#    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
#    && locale-gen \
#    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
#    && curl https://packages.microsoft.com/config/ubuntu/19.10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
#    && apt-get update \
    && apt-get install -y \
        # For odbc
#        msodbcsql17 \
#        mssql-tools \
#        unixodbc-dev \
        # For parquet, snappy
        llvm libsnappy-dev \
        python3-pip \
    && apt-get purge -y curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ${APP_HOME}/requirements.txt

RUN pip3 --no-cache-dir install -r ${APP_HOME}/requirements.txt \
    && rm /${APP_HOME}/requirements.txt \
    && apt-get purge -y build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=parquet-service:parquet-service utility ${APP_HOME}/utility
COPY --chown=parquet-service:parquet-service ./main.py ${APP_HOME}

USER parquet-service

WORKDIR ${APP_HOME}

#ENV PATH="$PATH:/opt/mssql-tools/bin"
ENV PYTHONPATH=${APP_HOME}

CMD ["python3", "main.py"]