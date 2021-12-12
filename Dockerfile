FROM python:3.6
WORKDIR /home
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"]
