import json
import sqlite3

PATH = "C:\\Users\\Tristan\\Desktop\\Computational_Law\\IP_Dashboard\\Data"

with open(PATH + "\\patents.json") as f:
    patents = json.load(f)

date_range = list(patents.keys())

# Pretty prints one patent application for one day to visualise the dictionary structure
print(json.dumps(patents[date_range[4]]["items"][1], indent = 4))
print(json.dumps(patents[date_range[4]]["items"][1]["applicationNum"], indent = 4))

print(json.dumps(patents[date_range[4]]["count"], indent = 4))


patents["2018-09-10"]["items"][2]["summary"]

patents["2020-08-31"]["items"][0]["summary"]["filingDate"] == None


to_write_list = []

for date in date_range :
    
    print(date)
    
    if patents[date]["count"] > 0 :
    
        for item in range(patents[date]["count"]) :

            print(item)

            if patents[date]["items"][item]["summary"]["filingDate"] == None :

                try :
                    to_write_tuple = (
                        patents[date]["items"][item]["summary"]["applicationNum"],
                        patents[date]["items"][item]["summary"]["applicationStatus"],
                        "",
                        patents[date]["items"][item]["summary"]["lodgementDate"],
                        patents[date]["items"][item]["summary"]["titleOfInvention"],
                        patents[date]["items"][item]["summary"]["ipc"]
                        )
                    
                    to_write_list.append(to_write_tuple)
            
                except :
                    to_write_tuple = (
                        patents[date]["items"][item]["summary"]["applicationNum"],
                        patents[date]["items"][item]["summary"]["applicationStatus"],
                        "",
                        patents[date]["items"][item]["summary"]["lodgementDate"],
                        patents[date]["items"][item]["summary"]["titleOfInvention"],
                        ""
                        )
                    
                    to_write_list.append(to_write_tuple)

            else :

                try :

                    to_write_tuple = (
                        patents[date]["items"][item]["summary"]["applicationNum"],
                        patents[date]["items"][item]["summary"]["applicationStatus"],
                        patents[date]["items"][item]["summary"]["filingDate"],
                        patents[date]["items"][item]["summary"]["lodgementDate"],
                        patents[date]["items"][item]["summary"]["titleOfInvention"],
                        patents[date]["items"][item]["summary"]["ipc"]
                        )

                    to_write_list.append(to_write_tuple)

                except :

                    to_write_tuple = (
                        patents[date]["items"][item]["summary"]["applicationNum"],
                        patents[date]["items"][item]["summary"]["applicationStatus"],
                        patents[date]["items"][item]["summary"]["filingDate"],
                        patents[date]["items"][item]["summary"]["lodgementDate"],
                        patents[date]["items"][item]["summary"]["titleOfInvention"],
                        ""
                        )

                    to_write_list.append(to_write_tuple)



# Creating database
conn = sqlite3.connect(PATH+"\\patents.db")

cursor = conn.cursor()

# cursor.execute("DROP TABLE summary;")

# This is just for the summary table
cursor.execute(
    '''
    CREATE TABLE summary (
        applicationNum TEXT UNIQUE PRIMARY KEY,
        applicationStatus TEXT NOT NULL,
        filingDate TEXT,
        lodgementDate TEXT NOT NULL,
        titleOfInvention TEXT,
        ipc TEXT
    );
    '''
    )


cursor.executemany('INSERT INTO summary VALUES (?, ?, ?, ?, ?, ?)', to_write_list)


# Check how many rows there are
cursor.execute(
    '''
    SELECT DISTINCT lodgementDate
    FROM summary;
    '''
)

rows = cursor.fetchall()

for row in rows :
    print(row)

conn.commit()
conn.close()