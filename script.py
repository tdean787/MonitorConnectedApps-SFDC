#!/usr/bin/env python3
from cgitb import text
from simple_salesforce import Salesforce
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
import smtplib
import requests
import tkinter as tk

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

dt = datetime.now()

window = tk.Tk()
window.title("Monitor Salesforce Connected Apps")
frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)

btn_start = tk.Button(frm_buttons, text="Start")

#ping for health check
try:
    requests.get(os.environ['healthCheckEndpoint'], timeout=10)
except requests.RequestException as e:
    # log failure
    print("ping failed: %s" % e)

# configure authentication env variables
load_dotenv()

password=os.environ['password']
username=os.environ['username']
token=os.environ['token']
instance_url=os.environ['instance_url']
appPW=os.environ['appPW']
gmailUser=os.environ['gmailUser']

#email config
from_address = gmailUser
to_address = gmailUser
msg = MIMEMultipart('alternative')
msg['Subject'] = "Connected Apps Monitoring Notification"
msg['From'] = from_address
msg['To'] = to_address

# connect to org
sf = Salesforce(username=username, password=password, instance=instance_url, security_token=token)

# create the SOQL query to get connected apps and create DataFrame
data = sf.query("SELECT Name FROM ConnectedApplication")
df = pd.DataFrame(data['records'])

# this is the list of values in the Name column, which represents all connected apps
appsCol = df['Name'].tolist()

#initialize a variable to track matching values
matching_app = ''

word_matches = ['your', 'test', 'cases']

#iterate over the list of apps and check for a match
for i in appsCol:
    for j in word_matches:
        if j.lower() in i.lower():
            matching_app = 'testMATCH'


if matching_app == 'testMATCH':
    html = "There is a match to your test phrases. See the full list of applications below." + "<br></br>" + "<br>".join(appsCol)
else:
    html = """\
        No matches to your test phrases in connected apps. See full list of connected apps below:
        """ + "<br></br>" + "<br>".join(appsCol)

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

window.mainloop()