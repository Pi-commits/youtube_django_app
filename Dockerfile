# Base Image
FROM python:3.8.5

# create and set working directory
RUN mkdir /app
WORKDIR /app

# Add current directory code to working directory
ADD . /app/

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# set project environment variables
# grab these via Python's os.environ
# these are 100% optional here
ENV PORT=8888

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# install environment dependencies
RUN pip3 install --upgrade pip
RUN pip3 install pipenv
RUN pip3 install certifi==2021.5.30
RUN pip3 install chardet==4.0.0
RUN pip3 install Django==2.2.4
RUN pip3 install django-background-tasks==1.2.5
RUN pip3 install django-compat==1.0.15
RUN pip3 install djangorestframework==3.12.4
RUN pip3 install gunicorn==20.1.0
RUN pip3 install idna==2.10
RUN pip3 install pytz==2021.1
RUN pip3 install requests==2.25.1
RUN pip3 install six==1.16.0
RUN pip3 install sqlparse==0.4.1
RUN pip3 install urllib3==1.26.5


# Install project dependencies
RUN pipenv install --skip-lock --system --dev

EXPOSE 8888
CMD python manage.py process_tasks & gunicorn youtube_selective_dashboard.wsgi:application --bind 0.0.0.0:$PORT