FROM centos:7

# Install pre-requisites:
RUN yum update -y && \
    yum install -y \
        curl \
        git \
        rlwrap \
        screen \
        vim \
        emacs-nox && \
    yum install -y \
        epel-release && \
    yum groupinstall -y "Development Tools" && \
    yum install -y \
        libffi-devel \
        libxml2-devel \
        libxslt-devel \
        npm \
        python-devel \
        python-pip

RUN yum clean -y all

RUN pip install --upgrade pip setuptools wheel && \
    npm update && \
    npm install --silent -g node-sass@3.8.0 clean-css@3.4.24 uglify-js requirejs

RUN python -m site
RUN python -m site --user-site

# Install Invenio
ENV WORKING_DIR=/opt/e-ternity
ENV INVENIO_INSTANCE_PATH=${WORKING_DIR}/var/instance

# copy everything inside /src
RUN mkdir -p ${WORKING_DIR}/src
COPY . ${WORKING_DIR}/src
WORKDIR ${WORKING_DIR}/src

RUN mkdir -p ${INVENIO_INSTANCE_PATH}

# Install Python dependencies
RUN pip install .[all,mysql,elasticsearch2] --process-dependency-links --trusted-host github.com

# Install/create static files
RUN invenio npm && \
    cd ${INVENIO_INSTANCE_PATH}/static && \
    npm install && \
    invenio collect -v && \
    invenio assets build

# Set folder permissions
RUN chgrp -R 0 ${INVENIO_INSTANCE_PATH} && \
    chmod -R g=u ${INVENIO_INSTANCE_PATH}

RUN adduser --uid 1000 invenio --gid 0 && \
    chown -R invenio:root ${INVENIO_INSTANCE_PATH}
USER 1000
