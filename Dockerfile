FROM python

#setup workdir
WORKDIR /app

#install dependencies
RUN apt update && apt install -y gettext

COPY requirements.txt .
RUN pip install -r requirements.txt

#copy source code 
COPY src src
COPY templates templates
COPY localization localization
COPY conf/pong.yaml conf/pong.yaml

#compile translation
RUN cd localization/ru/LC_MESSAGES && \
    msgfmt ru.po -o ru.mo

CMD ["python3.7", "src/app.py", "--config", "conf/pong.yaml"]
