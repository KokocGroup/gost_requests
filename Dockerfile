FROM rnix/openssl-gost:latest
# Убрал --enable-optimizations по умолчанию
ARG python_optimizations

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
            git \
            zlib1g-dev \
            libffi-dev \
            cmake \
            build-essential \
            libboost-all-dev \
            python3-dev \
    && git clone --single-branch --branch 3.7 https://github.com/python/cpython.git \
    && cd cpython \
    # Добавление строки OPENSSL_add_all_algorithms_conf() заставляет компилятор
    # прочитать openssl.cnf и добавить ГОСТ шифры в python
    && sed -i '/PySocketModule = \*socket_api/a \ \ \ \ OPENSSL_add_all_algorithms_conf();' ./Modules/_ssl.c \
    && ./configure \
            --with-openssl=/usr/local/ssl \
            $python_optimizations \
    && make -j "$(nproc)" \
    && make install \
    && find /usr/local -depth \
        \( \
            \( -type d -a \( -name test -o -name tests \) \) \
            -o \
            \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
        \) -exec rm -rf '{}' + \
    && rm -r /cpython \
    && ln -s /usr/local/bin/python3 /usr/local/bin/python \
    && ln -s /usr/local/bin/pip3 /usr/local/bin/pip \
    && apt-get purge -y --auto-remove git zlib1g-dev libffi-dev

# Тест поддержки ГОСТа
RUN python -c "import ssl; ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1); \
    ctx.set_ciphers('GOST2012-GOST8912-GOST8912')"

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


ADD dist /tmp/src
RUN cd /tmp/src && \
    tar -xf linux-amd64_deb.tgz && \
    linux-amd64_deb/install.sh && \
    # делаем симлинки
    cd /bin && \
    ln -s /opt/cprocsp/bin/amd64/certmgr && \
    ln -s /opt/cprocsp/bin/amd64/cpverify && \
    ln -s /opt/cprocsp/bin/amd64/cryptcp && \
    ln -s /opt/cprocsp/bin/amd64/csptest && \
    ln -s /opt/cprocsp/bin/amd64/csptestf && \
    ln -s /opt/cprocsp/bin/amd64/der2xer && \
    ln -s /opt/cprocsp/bin/amd64/inittst && \
    ln -s /opt/cprocsp/bin/amd64/wipefile && \
    ln -s /opt/cprocsp/sbin/amd64/cpconfig


WORKDIR /code
COPY ./app /code/app

CMD ["uvicorn", "app.start:app", "--host", "0.0.0.0", "--port", "8000"]