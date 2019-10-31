FROM registry.gitlab.com/genomicsengland/dataquality/cdt-docker:v1.0

COPY install.r /

RUN ["Rscript", "install.r"]
RUN ["rm", "install.r"]
