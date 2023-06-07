FROM python:3.9-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY / .
#COPY TOKEN .
CMD ["python", "./share_app.py"]
