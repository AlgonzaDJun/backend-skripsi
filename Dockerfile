# 
FROM python:3.9-slim

# 
WORKDIR /code

# 
COPY ./requirements2.txt /code/requirements2.txt
#

# Memastikan bahwa paket `apt-get` dapat diakses
RUN apt-get update

# Menginstal paket yang diperlukan
RUN apt-get install -y gcc python3-dev

RUN pip install --upgrade pip setuptools
#

RUN pip install --default-timeout=100 future
# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements2.txt

# 
COPY . /code/app
# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]