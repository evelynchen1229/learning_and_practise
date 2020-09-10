import teradata
import pandas as pd
import csv
import os
import sys
from datetime import datetime
import shutil
import win32com.client as win32

path = r"path\test"
dirs = os.listdir(path)
dest = r"path\Archive"
for file in dirs:
    file_path = os.path.join(path,file)
#    print(file_path)
#try:
    if os.path.isfile(file_path):
        shutil.move(file_path,dest)
#except:
    #else: print("error");
#print (os.path.isfile(file_path));
currentYear = datetime.now().strftime("%Y")
currentMonth = datetime.now().strftime("%m")
today= str(currentMonth)+str(currentYear)
output_file = r"path{}.csv".format(today)

host,username,password = 'HOST','UID','PSD'
udaExec = teradata.UdaExec (appName = "test", version ="1.0", logConsole=False)
with udaExec.connect(method="odbc", system=host, username=username,password=password,driver="Teradata") as connect:
    query = "SELECT TOP 10* FROM BI.acct_curr;"
    df = pd.read_sql(query,connect)
    df.to_csv(output_file,index=False);
#    print(df)

#with open('try_csv.csv','rt',encoding='utf-8-sig') as f:
#    reader=csv.reader(f)
#    for row in reader:
#        print (row);



#print(today);
outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'email'
mail.Subject = 'Test'
mail.Body = """Hi,

Please find attached testing report. Thank you.
          
Best,
"""
attachment = r"path{}.csv".format(
    today)
mail.Attachments.Add(attachment)
mail.Send()
