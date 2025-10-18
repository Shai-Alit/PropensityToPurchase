FROM alpine:3.14
RUN apk add --no-cache --upgrade bash -f environment.yml
FROM python:3

WORKDIR /usr/src/app

COPY /root/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
USER root
RUN mkdir /opt/BaseballSalary
RUN chmod -R 777 /opt/BaseballSalary
WORKDIR /opt/BaseballSalary
COPY environment.yml environment.yml
COPY root /opt/BaseballSalary/
COPY run.sh run.sh
RUN chmod a+x run.sh
CMD ["./run.sh"]