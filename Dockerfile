FROM python

#setup workdir
WORKDIR /app

#install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

#copy source code 
COPY conf src static templates ./ 

CMD ["python3.7", "src/app.py", "--config", "conf/pong.yaml"]
