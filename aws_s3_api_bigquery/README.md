things needed:
1. aws set up / sso sign in configure to access s3 and secret manager
Prerequisites:
You need to have AWS CLI version 2 or above. Link to install AWS CLI 2 is Installing or updating the latest version of the AWS CLI - AWS Command Line Interface
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

Login to AWS CLI via SSO:



When we login via IAM user we setup the config and credentials file present in the .aws directory inside the home folder. To login via SSO, we only need to configure the config file in the .aws  folder

Below is an example of Sample profile in a config file via SSO:


[profile profile_name]
sso_start_url = https://fitxr.awsapps.com/start
sso_account_id = 114211897470
sso_role_name = role_name
sso_region = eu-west-2
region = region_name
You can change the region and profile name as per your need.

Role name could be fetched once you login into AWS SSO via the browser. Below is a screenshot highlighting the role_name:
Once the config file is setup and done, run the below command from your terminal:




aws sso login --profile profile_name

update config and credential files in .aws folder.
2. to access bigquery, need bigquery key to set up environment variables
