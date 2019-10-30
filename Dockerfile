FROM registry.gitlab.com/genomicsengland/dataquality/cdt-docker:v1.0

RUN ["Rscript", "install.r"]
