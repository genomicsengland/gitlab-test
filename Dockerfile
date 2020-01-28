FROM registry.gitlab.com/genomicsengland/dataquality/cdt-docker:v1.0

COPY install.r /
COPY requirements.txt /

RUN apt-get update && apt-get install -y iputils-ping

RUN apt-get update && apt-get install -y libcurl4-openssl-dev

RUN apt-get update && apt-get install -y libssl-dev

RUN apt-get update && apt-get install curl

RUN pip3 install -r requirements.txt

RUN ["Rscript", "install.r"]
RUN ["rm", "install.r"]
