# Monitor Connected Apps in Salesforce with SOQL and Python

## Usage

The script can be forked, copied, etc. and run locally. Create a .env file and configure your Salesforce authentication as well as the email addresses you want to send to.
The matching terms section will be later converted to take an array and check for any matches against it. Currently this is functioning as a one off need to automate the monitoring of current Connected Apps.

### Crontab and Virtual Environment Handling
In order to create a cron job that runs a project built in a virtual environment, the following configuration is required: 

`* * * * * /path/to/virtualenvironment/bin/python3 /path/to/python/script.py command arg >> /path/to/errorlogging/directory/output.txt`

This will ensure that the correct interpreter is used, libraries are loaded, environment variables included, etc. Error loggin in an output file is optional.
