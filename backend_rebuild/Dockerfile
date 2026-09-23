FROM python:3.11-slim

WORKDIR /app

# install relevant packages
RUN apt-get update && \
    apt-get install -y build-essential libffi-dev libssl-dev python3-dev && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN pip install "setuptools<81" wheel
RUN pip install pandas
RUN pip install -i https://mirrors.aliyun.com/pypi/simple gunicorn
RUN pip install gevent>=22.10.2

COPY . .

EXPOSE 5001

#CMD ["python", "app.py"]
CMD ["gunicorn", "-c", "./gunicornConfig.py", "main:app"]
