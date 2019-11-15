FROM registry.gitlab.com/genomicsengland/dataquality/cdt-docker:v1.0

COPY install.r /

RUN apt-get update && apt-get install -y iputils-ping

RUN apt-get update && apt-get install -y libcurl4-openssl-dev

RUN apt-get update && apt-get install -y libssl-dev

RUN ["Rscript", "install.r"]
RUN ["rm", "install.r"]
