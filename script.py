#!/usr/bin/env python3
from cgitb import text
from tabnanny import check
from simple_salesforce import Salesforce
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk
from pandastable import Table, TableModel

dt = datetime.now()
load_dotenv()

SFDCpassword=os.environ['password']
SFDCusername=os.environ['username']
SFDCtoken=os.environ['token']
SFDCinstance_url=os.environ['instance_url']

window = tk.Tk(className='Salesforce Monitor', )
window.geometry("400x300")

#authenticate to Salesforce
sf = Salesforce(username=SFDCusername, password=SFDCpassword, instance=SFDCinstance_url, security_token=SFDCtoken)


def checkConnectedApps():
    # create the SOQL query to get connected apps and create DataFrame
    data = sf.query("SELECT Name FROM ConnectedApplication")
    df = pd.DataFrame(data['records'])

    # this is the list of values in the Name column, which represents all connected apps
    appsCol = df['Name'].tolist()

    #initialize a variable to track matching values
    matching_app = ''

    word_matches = ['test', 'word', 'lorem', 'ipsum']

    #iterate over the list of apps and check for a match
    for i in appsCol:
        for j in word_matches:
            if j.lower() in i.lower():
                matching_app = 'testMATCH'

    cols = list(df.columns)
    tree = ttk.Treeview(window)
    tree.pack()
    tree["columns"] = cols
    for i in cols:
        tree.column(i, anchor='w')
        tree.heading(i, text=i, anchor='w')
    for index, row in df.iterrows():
        tree.insert("", 0, text=index, values=list(row))

    if matching_app == 'testMATCH':
        T = Text(window, height=5,width=25)
        l = Label(window, text="Match Results")
        result = f'Match to test phrases: {word_matches}'
        l.pack()
        T.pack()
        T.insert(tk.END, result)
        window.update()
    else:
        T = Text(window, height=5,width=25)
        l = Label(window, text="Match Results")
        result = 'No match to test phrases'
        l.pack()
        T.pack()
        T.insert(tk.END, result)
        window.update()


def checkSetupAuditTrail():
    # create the SOQL query to get connected apps and create DataFrame
    data = sf.query("SELECT CreatedDate, Action, Display, CreatedBy.Name, Section FROM SetupAuditTrail where CreatedBy.Name != null AND CreatedDate = LAST_N_DAYS:10 order by CreatedDate desc")
    df = pd.DataFrame(data['records'])

    cols = list(df.columns)
    tree = ttk.Treeview(window)
    tree.pack()
    tree["columns"] = cols
    for i in cols:
        tree.column(i, anchor='w')
        tree.heading(i, text=i, anchor='w')
    for index, row in df.iterrows():
        tree.insert("", 0, text=index, values=list(row))
    
    window.update()

def checkPhrases():
    userPhrases = textEntry.get()
    print(type(userPhrases))
    print(textEntry.get())
    
    return

btn_start = tk.Button(window, text="Start", command=checkConnectedApps)
btn_start.config(width=20, height=2)
btn_start.pack()

btn_audit = tk.Button(window, text="Setup Audit Trail", command=checkSetupAuditTrail)
btn_audit.config(width=20, height=2)
btn_audit.pack()

textEntry = Entry(window)
textEntry.pack()

btn_enter_phrases = tk.Button(window, text="Submit Phrases", command=checkPhrases)
btn_enter_phrases.pack()

window.mainloop()