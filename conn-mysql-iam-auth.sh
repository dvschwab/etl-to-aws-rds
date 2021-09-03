#!/usr/bin/bash

set -x

IAMUSER="iam_user"
HOSTNAME="data-science-project.cbzmjled6wkx.us-east-2.rds.amazonaws.com"
REGION="us-east-2"

TOKEN="$(aws rds generate-db-auth-token --hostname $HOSTNAME --port 3306 --username $IAMUSER --region $REGION)"

mysql -h $HOSTNAME --ssl-ca=/misc/global-bundle.pem --enable-cleartext-plugin --user=$IAMUSER --password=$TOKEN
