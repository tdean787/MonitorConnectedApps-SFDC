from simple_salesforce import Salesforce
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

dt = datetime.now()

# configure authentication env variables
load_dotenv()
password=os.getenv("password")
username=os.getenv("username")
token=os.getenv("token")
instance_url = os.getenv("instance_url")
appPW = os.getenv("appPW")
gmailUser = os.getenv("gmailUser")

#email config
from_address = gmailUser
to_address = gmailUser
msg = MIMEMultipart('alternative')
msg['Subject'] = "Testing Email"
msg['From'] = from_address
msg['To'] = to_address

# connect to org
sf = Salesforce(username=username, password=password, instance=instance_url, security_token=token)

# create the SOQL query to get connected apps and create DataFrame
data = sf.query(f"SELECT Name FROM ConnectedApplication")
df = pd.DataFrame(data['records'])

# this is the list of values in the Name column, which represents all connected apps
appsCol = df['Name'].tolist()

#initialize a variable to track matching values
matching_app = ''

#iterate over the list of apps and check for a match to defined terms
for i in appsCol:
    if 'salesforce'.lower() in i.lower():
        matching_app = 'salesforce'

# df.drop('attributes', 1).to_csv(f'out={dt}.csv')
#df.to_csv(f'out-{dt}.csv')

if matching_app == 'salesforce':
    html = "Salesforce Connected App Confirmed" + "<br></br>" + "<br>".join(appsCol)
else:
    html = """\
        No matches to the defined list. See full list of connected apps below:
        """ + "\n".join(appsCol)

part1 = MIMEText(html, 'html')

msg.attach(part1)

username = gmailUser
emailPassword = appPW

server = smtplib.SMTP('smtp.gmail.com', 587) 
server.ehlo()
server.starttls()
server.login(username,emailPassword)  
server.sendmail(from_address, to_address, msg.as_string())  
server.quit()