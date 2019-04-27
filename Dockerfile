FROM python

#prepare app dir
COPY ./ /app
WORKDIR /app

#install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3.7", "src/app.py", "--config", "conf/pong.yaml"]
