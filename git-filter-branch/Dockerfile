FROM python:3.7-alpine as base
FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install"  -r /requirements.txt
FROM base
# Copy Builder Image
COPY --from=builder /install /usr/local
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories  && \
        apk add --update --no-cache libc6-compat tzdata git &&\
        ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime 
# Add alias
ENV ENV="/root/.ashrc"
RUN echo "alias ll='ls -l'\nLC_ALL=en_US.UTF-8" > "$ENV"

# git repository
VOLUME /var/lib/repo
# working dir
VOLUME /var/run/repo

COPY *.py /

