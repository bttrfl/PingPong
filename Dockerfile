FROM python

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./ /app

WORKDIR /app

CMD ["python3", "src/app.py", "--config", "conf/pong.yaml"]
