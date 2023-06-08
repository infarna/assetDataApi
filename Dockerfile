# Use the Amazon Linux base image
FROM amazonlinux:latest

# Update the package lists and upgrade existing packages
# install virtual environment 
# INSTALL PYTHON3
# install virtualenv
# install git 
# install docker
RUN yum update -y && \
    yum upgrade -y && \
    yum install python3 -y && \
    yum install python3-pip -y && \
    yum install virtualenv -y && \
    yum install git -y && \
    yum install docker -y

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# show contnet of /app
RUN ls -al

# copy every content from the local file to the image
COPY . /app

# show content of app post copy
RUN ls -al

# switch working directory
WORKDIR /app

# show contnet of /app
RUN ls -al

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
# COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python3" ]

# ENV PATH=/root/.local:$PATH
# EXPOSE 5001

CMD ["get_from_source_etfs.py" ]
