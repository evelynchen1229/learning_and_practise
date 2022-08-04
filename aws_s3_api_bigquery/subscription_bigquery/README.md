Prerequisites for testing the code in the local machine:
1. aws sso sign in first. Confluence page:https://fitarlimited.atlassian.net/wiki/spaces/DEVOPS/pages/2192179201/Configure+AWS+CLI+to+use+SSO
##Note: only need to change "region" variable in the config file to eu-west-1 for example, not the sso_region
2. s3 bucket is in Ireland region (eu-west-1): qa-oculus-subscription
3. secret manager is set up also in the Ireland region (eu-west-1): qa/oculus/subscription/api/token
4. once logged in, if you still get error regarding token expired when running the python scripts, you might also need to update the credential file in the .aws folder with the latest aws access key id, aws secret access key, and aws session token.
5. to load data to bigquery, the related bigguqery config information needs to be changed in the code. project should be analytics-dev-356310, table_id is analytics-dev-356310.staging.stg_subscriptioni. Also, we need to create a service account and get the key (a json file). This is needed for setting up environment variable for GOOGLE_APPLICATION_CREDENTIALS. Documentation: https://cloud.google.com/docs/authentication/getting-started
