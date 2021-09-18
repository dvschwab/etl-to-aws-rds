#!/usr/bin/bash

# Install required packages
apt-get update
apt-get install vim curl mysql-client unzip less

# Download and install AWS CLI to /opt
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/opt/awscliv2.zip"
unzip /opt/awscliv2.zip -d /opt
/opt/aws/install

# Copy AWS credentials to container

# Copy MySQL login and config to container

