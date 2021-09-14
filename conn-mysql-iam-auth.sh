#!/usr/bin/bash

# Script to connect to MySQL RDS instance using IAM authentication
# Based on example at https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.Connecting.AWSCLI.html

# Uncomment to debug
# set -x

IAMUSER=your user name
HOSTNAME=your host name
REGION=your region

# Generate the token using the AWS CLI
TOKEN="$(aws rds generate-db-auth-token --hostname $HOSTNAME --port 3306 --username $IAMUSER --region $REGION)"

# Connect using the MySQL client
# Change path of AWS certificates as needed
mysql -h $HOSTNAME --ssl-ca=/misc/global-bundle.pem --enable-cleartext-plugin --user=$IAMUSER --password=$TOKEN
