# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV SECRET_KEY='django-insecure-p6f)an3s*2yq)q--mh8!(o#aq78tfm@#f0o7jjkhc-b1d1ws7z'

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY entrypoint.sh ./

RUN apt-get update \
    && apt-get install -y --no-install-recommends dialog \
    && apt-get install -y --no-install-recommends openssh-server \
    && echo "root:Docker!" | chpasswd \
    && chmod u+x ./entrypoint.sh
COPY sshd_config /etc/ssh/


# Expose the port Django runs on
EXPOSE 80 2222
ENTRYPOINT [ "./entrypoint.sh" ] 



# RUN python manage.py makemigrations
# Run Django application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]


#CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:80"]
