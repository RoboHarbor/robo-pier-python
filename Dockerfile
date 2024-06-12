FROM ubuntu:22.04

ENV PYTHON_VERSION 3.9.0

#Set of all dependencies needed for pyenv to work on Ubuntu
RUN apt install -y ubuntu-keyring
RUN apt-get update
RUN apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget ca-certificates curl llvm git screen nano liblzma-dev libffi-dev lzma

# Set-up necessary Env vars for PyEnv
ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

# Install pyenv
RUN set -ex \
    && curl https://pyenv.run | bash \
    && pyenv update


# install python versions
RUN pyenv install 3.7.3
RUN pyenv install 3.8.0
RUN pyenv install 3.9.0
RUN pyenv install 3.10.0
RUN pyenv install 3.11.0
RUN pyenv install 3.12.0

RUN pyenv global $PYTHON_VERSION \
    && pyenv rehash

# install pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py

COPY ./robo_pier_lib/ /opt/robo_pier_lib/
COPY entry_point.py /opt/entry_point.py

RUN pip install -r /opt/robo_pier_lib/requirements.txt

RUN python3.10 get-pip.py
RUN python3.7 get-pip.py
RUN python3.8 get-pip.py
RUN python3.9 get-pip.py
RUN python3.11 get-pip.py
RUN python3.12 get-pip.py

# start the python shell
CMD ["python", "-i", "-q", "-u", "/opt/entry_point.py"]
