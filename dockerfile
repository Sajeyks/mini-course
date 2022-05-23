FROM ubuntu:20.04

# Installing Python
RUN apt update && apt install -y software-properties-common &&\
    add-apt-repository ppa:deadsnakes/ppa &&\
    apt install -y python3.8 &&\
    apt-get install -y python3-distutils python3-apt &&\
    apt install -y curl &&\
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py

# Copying requirements.txt
COPY requirements.txt .

# Installing packages from requirements.txt
RUN pip install -r requirements.txt

# Copying the project
COPY demo demo