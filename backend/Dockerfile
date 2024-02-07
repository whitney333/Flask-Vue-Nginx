FROM python:3.9.2-slim

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN python -m pip install --upgrade setuptools
RUN pip install wheel
RUN pip install pandas
RUN pip install -i https://mirrors.aliyun.com/pypi/simple gunicorn
RUN pip install gevent==21.1.2
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
COPY models.py .
COPY config.py .

EXPOSE 5001

#CMD ["python", "app.py"]
CMD ["gunicorn", "-c", "./gunicornConfig.py", "app:app"]
