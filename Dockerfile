FROM python

#setup workdir
WORKDIR /app

#install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

#copy source code 
COPY src templates localization ./ 
COPY conf/pong.yaml conf/pong.yaml

CMD ["python3.7", "src/app.py", "--config", "conf/pong.yaml"]
