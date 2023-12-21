FROM python:3.11-bullseye

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV MY_PRODUCTION="production"

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive 

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

RUN apt-get update && apt-get -y install google-chrome-stable

COPY . .

EXPOSE 5000

#CMD ["python3", "app/main.py"]
CMD [ "python3", "-m" , "flask", "--app", "app/main", "run", "--host=0.0.0.0"]