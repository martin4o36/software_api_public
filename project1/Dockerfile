FROM python:3.8
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r docker_folder/requirements.txt
EXPOSE 5000
CMD ["python", "./application/app.py", "--host=0.0.0.0", "--port=5000", "--reload"]