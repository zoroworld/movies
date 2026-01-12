FROM python:3.10-slim

# set working directory
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project files
COPY . .

# expose port
EXPOSE 8000

# start django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



