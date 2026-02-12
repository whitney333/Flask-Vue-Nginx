FROM python:3.9.2-slim

WORKDIR /app

# install relevant packages
RUN apt-get update && \
    apt-get install -y build-essential libffi-dev && \
    rm -rf /var/lib/apt/lists/* \

RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install pandas
RUN pip install -i https://mirrors.aliyun.com/pypi/simple gunicorn
RUN pip install gevent==21.1.2
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
#COPY models.py .
COPY .env.development .
COPY db_connect.py .
COPY main.py .


EXPOSE 5001

#CMD ["python", "app.py"]
CMD ["gunicorn", "-c", "./gunicornConfig.py", "main:app"]
