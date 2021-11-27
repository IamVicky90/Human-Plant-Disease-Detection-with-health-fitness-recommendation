FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y python3-pip
WORKDIR /home
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"]
