FROM ubuntu:18.04

ENV DIML_HOME /opt/diml-service

RUN  useradd -ms /bin/bash -r -d ${DIML_HOME} diml

# TODO: Consider merging these layers and purging
# Set Locale - required for ODBC driver
RUN apt-get update \
    && apt-get install -y \
        locales \
    && apt-get update \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen

ENV ACCEPT_EULA Y
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Download appropriate package for the OS version
# curl https://packages.microsoft.com/config/ubuntu/[##.##]/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN buildDeps='build-essential curl software-properties-common' \
    && set -x \
    && apt-get update \
    && apt-get install -y $buildDeps \
    && apt-get update \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && apt-get install -y \
        msodbcsql17 \
        mssql-tools \
        unixodbc-dev \
        python3-pip
    #&& rm -rf /var/lib/apt/lists/*
    #&& apt-get purge -y --auto-remove $buildDeps

# Plus GDAL
# TODO: doesn't work with 3.7
RUN add-apt-repository ppa:ubuntugis/ppa \
    && apt-get install -y \
        gdal-bin libgdal-dev \
        python3-gdal \
        python-setuptools python-dev \
        python3.7-dev
    #&& rm -rf /var/lib/apt/lists/*

# Plus libspatialindex
RUN apt-get update \
    && apt-get install -y libspatialindex-dev

# optional: for bcp and sqlcmd
ENV PATH="$PATH:/opt/mssql-tools/bin"

COPY requirements.txt ${DIML_HOME}/requirements.txt

RUN buildDeps='git' \
    && set -x \
    && apt-get update \
    && apt-get install -y $buildDeps --no-install-recommends \
    && pip3 install --upgrade pip==9.0.3 \
    && pip3 install -r ${DIML_HOME}/requirements.txt \
    && rm /${DIML_HOME}/requirements.txt \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove $buildDeps

COPY --chown=diml:diml ./python_gis ${DIML_HOME}/python_gis
COPY --chown=diml:diml ./main.py ${DIML_HOME}

USER diml

WORKDIR ${DIML_HOME}
ENV PATH=$PATH:${DIML_HOME}
ENV PYTHONPATH ${DIML_HOME}

CMD ["python3.6", "main.py"]