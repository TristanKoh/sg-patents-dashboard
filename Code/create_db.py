import json
import sqlite3

# PATH = "C:\\Users\\Tristan\\Desktop\\Computational_Law\\IP_Dashboard\\Data"
PATH = "..\\Data"
with open(PATH + "\\patents.json") as f:
    patents = json.load(f)

date_range = list(patents.keys())

### Pretty prints one patent application for one day to visualise the dictionary structure
print(json.dumps(patents[date_range[4]]["items"][1], indent = 4))
##
##print(json.dumps(patents[date_range[4]]["items"][1]["applicationNum"], indent = 4))
##
##print(json.dumps(patents[date_range[4]]["count"], indent = 4))
##
##
##patents["2018-09-10"]["items"][2]["summary"]
##
##patents["2020-08-31"]["items"][0]["summary"]["filingDate"] == None
##
### For Summary table
##to_write_list = []
##
##for date in date_range :
##    
##    print(date)
##    
##    if patents[date]["count"] > 0 :
##    
##        for item in range(patents[date]["count"]) :
##
##            print(item)
##
##            if patents[date]["items"][item]["summary"]["filingDate"] == None :
##
##                try :
##                    to_write_tuple = (
##                        patents[date]["items"][item]["summary"]["applicationNum"],
##                        patents[date]["items"][item]["summary"]["applicationStatus"],
##                        "",
##                        patents[date]["items"][item]["summary"]["lodgementDate"],
##                        patents[date]["items"][item]["summary"]["titleOfInvention"],
##                        patents[date]["items"][item]["summary"]["ipc"]
##                        )
##                    
##                    to_write_list.append(to_write_tuple)
##            
##                except :
##                    to_write_tuple = (
##                        patents[date]["items"][item]["summary"]["applicationNum"],
##                        patents[date]["items"][item]["summary"]["applicationStatus"],
##                        "",
##                        patents[date]["items"][item]["summary"]["lodgementDate"],
##                        patents[date]["items"][item]["summary"]["titleOfInvention"],
##                        ""
##                        )
##                    
##                    to_write_list.append(to_write_tuple)
##
##            else :
##
##                try :
##
##                    to_write_tuple = (
##                        patents[date]["items"][item]["summary"]["applicationNum"],
##                        patents[date]["items"][item]["summary"]["applicationStatus"],
##                        patents[date]["items"][item]["summary"]["filingDate"],
##                        patents[date]["items"][item]["summary"]["lodgementDate"],
##                        patents[date]["items"][item]["summary"]["titleOfInvention"],
##                        patents[date]["items"][item]["summary"]["ipc"]
##                        )
##
##                    to_write_list.append(to_write_tuple)
##
##                except :
##
##                    to_write_tuple = (
##                        patents[date]["items"][item]["summary"]["applicationNum"],
##                        patents[date]["items"][item]["summary"]["applicationStatus"],
##                        patents[date]["items"][item]["summary"]["filingDate"],
##                        patents[date]["items"][item]["summary"]["lodgementDate"],
##                        patents[date]["items"][item]["summary"]["titleOfInvention"],
##                        ""
##                        )
##
##                    to_write_list.append(to_write_tuple)
##
##
##
### For inventors table - not all have inventors
### Keyed by applicationNum to match with summary table
##
##patents["2018-09-10"]["items"][1]["summary"]["applicationNum"]
##
##patents["2018-09-10"]["items"][1]["inventors"][1]["name"]
##
##len(patents["2018-09-10"]["items"][1]["inventors"])
##
##to_write_list_inventors = []
##
##for date in date_range[:10] :
##    
##    print(date)
##    
##    if patents[date]["count"] > 0 :
##    
##        for item in range(patents[date]["count"]) :
##
##            print(item)
##
##            # Not all patents have inventor names, hence use try except
##            try :
##                num_inventors = range(len(patents[date]["items"][item]["inventors"]))
##
##                for inventor in num_inventors :
##                    print("inventor:", inventor)
##                    
##                    to_write_tuple = (
##                        patents[date]["items"][item]["summary"]["applicationNum"],
##                        patents[date]["items"][item]["inventors"][inventor]["name"],
##                        patents[date]["items"][item]["inventors"][inventor]["address"],   
##                        patents[date]["items"][item]["inventors"][inventor]["countryOfResidence"]["description"],
##                        patents[date]["items"][item]["inventors"][inventor]["countryOfResidence"]["code"],
##                        patents[date]["items"][item]["inventors"][inventor]["nationality"]
##                    )
##
##                    to_write_list_inventors.append(to_write_tuple)
##            
##            except :
##                pass
##                
##
##print(to_write_list_inventors[:50])
##len(to_write_list_inventors)
##
##
### For applicant table
##patents["2018-09-10"]["items"][4]["applicant"][0]
##
##to_write_list_applicant = []
##
##for date in date_range :
##    
##    print(date)
##    
##    if patents[date]["count"] > 0 :
##    
##        for item in range(patents[date]["count"]) :
##
##            print(item)
##
##            try :
##                for applicant_num in range(len(patents[date]["items"][item]["applicant"])) :
##
##                    to_write_tuple = (
##                    patents[date]["items"][item]["summary"]["applicationNum"],
##                    patents[date]["items"][item]["applicant"][applicant_num]["stateOfIncorporation"]["description"],
##                    patents[date]["items"][item]["applicant"][applicant_num]["stateOfIncorporation"]["code"],
##                    patents[date]["items"][item]["applicant"][applicant_num]["address"],
##                    patents[date]["items"][item]["applicant"][applicant_num]["uenCompanyCode"],
##                    patents[date]["items"][item]["applicant"][applicant_num]["nationality"]["description"],
##                    patents[date]["items"][item]["applicant"][applicant_num]["nationality"]["code"],
##                    patents[date]["items"][item]["applicant"][applicant_num]["soleProprietorPartnerName"],
##                    patents[date]["items"][item]["applicant"][applicant_num]["name"],
##                    patents[date]["items"][item]["applicant"][applicant_num]["countryOfIncorporationOrResidence"]["description"],
##                    patents[date]["items"][item]["applicant"][applicant_num]["countryOfIncorporationOrResidence"]["code"]
##                    )
##
##                    to_write_list_applicant.append(to_write_tuple)
##
##            except :
##                pass
##                
##
##to_write_list_applicant[:50]
##len(to_write_list_applicant)
##
##
##
### For agent correspondence details
##patents["2018-09-10"]["items"][1]["agentCorrespondenceDetails"][0]
##
##to_write_list_agent = []
##
##for date in date_range :
##    
##    print(date)
##    
##    if patents[date]["count"] > 0 :
##    
##        for item in range(patents[date]["count"]) :
##
##            print(item)
##
##            try :
##                to_write_tuple = (
##                patents[date]["items"][item]["summary"]["applicationNum"],
##                patents[date]["items"][item]["agentCorrespondenceDetails"][0]["representationType"],
##                patents[date]["items"][item]["agentCorrespondenceDetails"][0]["agent"]["uenCompanyCode"],
##                patents[date]["items"][item]["agentCorrespondenceDetails"][0]["agent"]["name"],
##                patents[date]["items"][item]["agentCorrespondenceDetails"][0]["actionRepresenting"],
##                patents[date]["items"][item]["agentCorrespondenceDetails"][0]["representativeName"],
##                patents[date]["items"][item]["agentCorrespondenceDetails"][0]["addressForServiceInSingapore"]
##                )
##
##                to_write_list_agent.append(to_write_tuple)
##
##            except :
##                pass
##
##
##to_write_list_agent[:50]
##len(to_write_list_agent)
##
##
### For declaration of priority
##patents["2018-09-10"]["items"][1]["declarationOfPriority"]
##
##to_write_declaration = []
##
##for date in date_range :
##    
##    print(date)
##    
##    if patents[date]["count"] > 0 :
##        
##        for item in range(patents[date]["count"]) :
##            
##            print(item)
##
##            try:
##                for j in range(len(patents[date]["items"][item]["declarationOfPriority"])) :
##                    
##                    to_write_tuple = (
##                        patents[date]["items"][item]["summary"]["applicationNum"],
##                        patents[date]["items"][item]["declarationOfPriority"][j]["applicationNum"],
##                        patents[date]["items"][item]["declarationOfPriority"][j]["country"]["description"],
##                        patents[date]["items"][item]["declarationOfPriority"][j]["country"]["code"],
##                        patents[date]["items"][item]["declarationOfPriority"][j]["filingDate"]
##                    )
##
##                    to_write_declaration.append(to_write_tuple)
##            
##            except:
##                pass
##
##
##to_write_declaration[:50]
##len(to_write_declaration)
##
##
### For grant renewal
##patents["2018-09-10"]["items"][1]["grantAndRenewal"]
##
##to_write_list_grant_renewal = []
##
##for date in date_range :
##    
##    print(date)
##    
##    if patents[date]["count"] > 0 :
##        
##        for item in range(patents[date]["count"]) :
##            
##            print(item)
##
##            try:
##                    
##                to_write_tuple = (
##                    patents[date]["items"][item]["summary"]["applicationNum"],
##                    patents[date]["items"][item]["grantAndRenewal"]["expiryDate"],
##                    patents[date]["items"][item]["grantAndRenewal"]["divisionalParentOfUKEUPatentNum"],
##                    patents[date]["items"][item]["grantAndRenewal"]["dateOfGrantOfUKEUPatentNum"],
##                    patents[date]["items"][item]["grantAndRenewal"]["dateOfLastRenewal"],
##                    patents[date]["items"][item]["grantAndRenewal"]["dateOfRenewal"],
##                    patents[date]["items"][item]["grantAndRenewal"]["yearOfLastRenewal"],
##                    patents[date]["items"][item]["grantAndRenewal"]["grantDate"],
##                    patents[date]["items"][item]["grantAndRenewal"]["dateOfIssueOfCertificateOfRegistrationInSingapore"],
##                    patents[date]["items"][item]["grantAndRenewal"]["nextRenewalDate"]
##                )
##
##                to_write_list_grant_renewal.append(to_write_tuple)
##            
##            except:
##                pass
##
##
##to_write_list_grant_renewal[:50]
##len(to_write_list_grant_renewal)
##
### For division applications
##patents["2018-09-10"]["items"][4]["transferOfOwnership"]
##
##
### For supporting documents table - not all have documents
### Keyed by applicationNum to match with summary table
##
##to_write_list_documents = []
##
##for date in date_range :
##    
##    print(date)
##    
##    if patents[date]["count"] > 0 :
##    
##        for item in range(patents[date]["count"]) :
##
##            print(item)
##
##            # Not all patents have documents, hence use try except
##            try :
##                num_documents = range(len(patents[date]["items"][item]["documents"]))
##
##                for document in num_documents :
##                    print("document:", document)
##                    
##                    to_write_tuple = (
##                        patents[date]["items"][item]["summary"]["applicationNum"],
##                        patents[date]["items"][item]["summary"]["titleOfInvention"],
##                        patents[date]["items"][item]["documents"][document]["fileName"],
##                        patents[date]["items"][item]["documents"][document]["lodgementDate"],
##                        patents[date]["items"][item]["documents"][document]["docType"]["description"],
##                        patents[date]["items"][item]["documents"][document]["url"]
##                    )
##
##                    to_write_list_documents.append(to_write_tuple)
##            
##            except :
##                pass
##                
##
###print(to_write_list_documents[:50])
##print(len(to_write_list_documents))
##
##
### For PCT application
##to_write_list_pctapp = []
##
##for date in date_range :
##    
##    print(date)
##    
##    if patents[date]["count"] > 0 :
##    
##        for item in range(patents[date]["count"]) :
##
##            # Not all patents have pct app, hence use try except
##            try :
##                num_pct_apps = range(len(patents[date]["items"][item]["pctApplication"]))
##
##                for pct_app in num_pct_apps :
##
##                    countries_filed = range(len(patents[date]["items"][item]["pctApplication"][pct_app]["pctPriorityClaimed"]))
##
##                    for country in countries_filed: # pct in several countries
##                        #print("pct app:", patents[date]["items"][item]["pctApplication"][pct_app]['pctPublicationNum'])
##                        to_write_tuple = (
##                            patents[date]["items"][item]["summary"]["applicationNum"],
##                            patents[date]["items"][item]["pctApplication"][pct_app]["pctApplicationNu,"],
##                            patents[date]["items"][item]["pctApplication"][pct_app]["pctPublicationNum"],
##                            patents[date]["items"][item]["pctApplication"][pct_app]["pctPublicationDate"],
##                            patents[date]["items"][item]["pctApplication"][pct_app]["pctEntryDate"],
##                            patents[date]["items"][item]["pctApplication"][pct_app]['pctPriorityClaimed'][country]["priorityApplicationNum"],
##                            patents[date]["items"][item]["pctApplication"][pct_app]['pctPriorityClaimed'][country]["filingDate"],
##                            patents[date]["items"][item]["pctApplication"][pct_app]['pctPriorityClaimed'][country]["country"]["code"],
##                            patents[date]["items"][item]["pctApplication"][pct_app]['pctPriorityClaimed'][country]["country"]["description"]
##                        )
##                        
##                        to_write_list_pctapp.append(to_write_tuple)
##            
##            except :
##                pass
##
##
### Creating database
##conn = sqlite3.connect(PATH+"\\patents.db")
##
##cursor = conn.cursor()
##cursor.execute("PRAGMA foreign_keys = ON;")
##
### cursor.execute("DROP TABLE summary;")
##
### Summary table
##cursor.execute(
##    '''
##    CREATE TABLE summary (
##        applicationNum TEXT UNIQUE PRIMARY KEY,
##        applicationStatus TEXT NOT NULL,
##        filingDate TEXT,
##        lodgementDate TEXT NOT NULL,
##        titleOfInvention TEXT,
##        ipc TEXT
##    );
##    '''
##    )
##
##cursor.executemany('INSERT INTO summary VALUES (?, ?, ?, ?, ?, ?)', to_write_list)
##
### Check how many rows there are
##cursor.execute(
##    '''
##    SELECT DISTINCT lodgementDate
##    FROM summary;
##    '''
##)
##
##rows = cursor.fetchall()
##
##for row in rows :
##    print(row)
##
### Inventor table
### cursor.execute("DROP TABLE inventors;")
##
##cursor.execute(
##    '''
##    CREATE TABLE inventors (
##        applicationNum TEXT NOT NULL,
##        name TEXT,
##        address TEXT,
##        country TEXT,
##        country_code TEXT,
##        nationality TEXT,
##        FOREIGN KEY (applicationNum) REFERENCES summary (applicationNum)
##    );
##    '''
##    )
##
##cursor.executemany('INSERT INTO inventors VALUES (?, ?, ?, ?, ?, ?)', to_write_list_inventors)
##
##
### Check how many rows there are
##cursor.execute(
##    '''
##    SELECT applicationNum
##    FROM inventors;
##    '''
##)
##
##rows = cursor.fetchall()
##len(rows)
##
##
### Applicant table
##cursor.execute(
##    '''
##    CREATE TABLE applicant (
##        applicationNum TEXT NOT NULL,
##        stateOfIncorporation TEXT,
##        stateOfIncorporation_code TEXT,
##        address TEXT,
##        uenCompanyCode TEXT,
##        nationality TEXT,
##        nationality_code TEXT,
##        soleProprietorPartnerName TEXT,
##        name TEXT,
##        countryOfIncorpOrResidence TEXT,
##        countryOfIncorpOrResidence_code TEXT,
##        FOREIGN KEY (applicationNum) REFERENCES summary (applicationNum)
##    );
##    '''
##    )
##
##cursor.executemany('INSERT INTO applicant VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', to_write_list_applicant)
##
##cursor.execute(
##    '''
##    SELECT applicationNum
##    FROM applicant;
##    '''
##)
##
##rows = cursor.fetchall()
##len(rows)
##
##
### Agent_corr_details
##cursor.execute(
##    '''
##    CREATE TABLE agent_details (
##        applicationNum TEXT NOT NULL,
##        representationType TEXT,
##        agent_uenCompanyCode TEXT,
##        agent_name TEXT,
##        actionaRepresenting TEXT,
##        representativeName TEXT,
##        addressForServiceInSingapore TEXT,
##        FOREIGN KEY (applicationNum) REFERENCES summary (applicationNum)
##    );
##    '''
##    )
##
##cursor.executemany('INSERT INTO agent_details VALUES (?, ?, ?, ?, ?, ?, ?)', to_write_list_agent)
##
##cursor.execute(
##    '''
##    SELECT applicationNum
##    FROM agent_details;
##    '''
##)
##
##rows = cursor.fetchall()
##len(rows)
##
##
### Declaration priority
##cursor.execute(
##    '''
##    CREATE TABLE declaration_priority (
##        applicationNum TEXT NOT NULL,
##        priority_app_num TEXT,
##        country TEXT,
##        country_code TEXT,
##        filing_date TEXT,
##        FOREIGN KEY (applicationNum) REFERENCES summary (applicationNum)
##    );
##    '''
##    )
##
##cursor.executemany('INSERT INTO declaration_priority VALUES (?, ?, ?, ?, ?)', to_write_declaration)
##
##cursor.execute(
##    '''
##    SELECT applicationNum
##    FROM declaration_priority;
##    '''
##)
##
##rows = cursor.fetchall()
##len(rows)
##len(to_write_declaration)
##
##
### grant_renewal
##
##cursor.execute(
##    '''
##    CREATE TABLE grant_renewal (
##        applicationNum TEXT NOT NULL,
##        expiryDate TEXT,
##        divisionalParentOfUKEUPatentNum TEXT,
##        dateOfGrantOfUKEUPatentNum TEXT,
##        dateOfLastRenewal TEXT,
##        dateOfRenewal TEXT,
##        yearOfLastRenewal TEXT,
##        grantDate TEXT,
##        date_SG_registration_cert_issued TEXT,
##        nextRenewalDate TEXT,
##        FOREIGN KEY (applicationNum) REFERENCES summary (applicationNum)
##    );
##    '''
##    )
##
##cursor.executemany('INSERT INTO grant_renewal VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', to_write_list_grant_renewal)
##
##cursor.execute(
##    '''
##    SELECT applicationNum
##    FROM grant_renewal;
##    '''
##)
##
##rows = cursor.fetchall()
##len(rows)
##len(to_write_list_grant_renewal)
##
### Application supporting documents
##cursor.execute("DROP TABLE IF EXISTS supporting_documents;")
##cursor.execute(
##    '''
##    CREATE TABLE supporting_documents (
##        applicationNum TEXT NOT NULL,
##        titleOfInvention TEXT,
##        fileName TEXT,
##        documentLodgementDate TEXT,
##        description TEXT,
##        url TEXT,
##        FOREIGN KEY (applicationNum) REFERENCES summary (applicationNum)
##    );
##    '''
##    )
##
##cursor.executemany('INSERT INTO supporting_documents VALUES (?, ?, ?, ?, ?, ?)', to_write_list_documents)
##
##cursor.execute(
##    '''
##    SELECT applicationNum
##    FROM supporting_documents;
##    '''
##)
##
##rows = cursor.fetchall()
##print(len(rows))
##print(len(to_write_list_documents))
##            
### PCT Application
##cursor.execute("DROP TABLE IF EXISTS pct_app;")
##cursor.execute(
##    '''
##    CREATE TABLE pct_app (
##        applicationNum TEXT NOT NULL,
##        pctAppNum TEXT,
##        pctPublicationNum TEXT,
##        pctPublicationDate TEXT,
##        pctEntryDate TEXT,
##        pctPriorityAppNum TEXT,
##        pctFilingDate TEXT,
##        pctCountryCode TEXT,
##        pctCountry TEXT,
##        FOREIGN KEY (applicationNum) REFERENCES summary (applicationNum)
##    );
##    '''
##    )
##
##cursor.executemany('INSERT INTO pct_app VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', to_write_list_pctapp)
##
##cursor.execute(
##    '''
##    SELECT applicationNum
##    FROM pct_app;
##    '''
##)
##
##rows = cursor.fetchall()
##print(len(rows))
##print(len(to_write_list_pctapp))
##
##conn.commit()
##conn.close()

