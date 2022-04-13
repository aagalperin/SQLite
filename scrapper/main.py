from dis import dis
import mechanicalsoup
import pandas as pd
import sqlite3

#creating a browser object
browser = mechanicalsoup.StatefulBrowser()
browser.open('https://en.wikipedia.org/wiki/Comparison_of_Linux_distributions')

# extract table headers
th = browser.page.find_all('th', attrs={'class': 'table-rh'})
distribution = [value.text.replace("\n", "") for value in th]
distribution = distribution[:95]


td = browser.page.find_all("td")
columns = [value.text.replace("\n", "") for value in td]
columns = columns[6 : 1051]

# select every 11th item

column_names = ["Founder", 
                "Maintainer", 
                "Initial_Release_Year", 
                "Current_Stable_Version", 
                "Security_Updates", 
                "Release_Date", 
                "System_Distribution_Commitment", 
                "Forked_From", 
                "Target_Audience", 
                "Cost", 
                "Status"]

dictionary = {"Distribution": distribution} 

for index, key in enumerate(column_names):
    dictionary[key] = columns[index:][::11]

df = pd.DataFrame(data = dictionary)

# insert data into a database
connection = sqlite3.connect("linux_distro.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE linux (Distribution" +  ",".join(column_names) + ")")

for i in range(len(df)):
    cursor.execute("INSERT INTO linux VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",df.iloc[i])

connection.commit()

connection.close()
