import requests
from datetime import timedelta, date
import json

PATH = "C:\\Users\\Tristan\\Desktop\\Computational_Law\\IP_Dashboard\\ip_dashboard\\Data"
API = "https://api.data.gov.sg/v1/technology/ipos/patents"

# Get list of strings of the range of dates to get from the API
start_date = date(2018, 8, 31)
end_date = date(2020, 12, 17)

# Generator object: Takes the number of days in between start and end date, creates a list of ints, and iterates through the ints 
# To get increment by 1 day timedelta from the start date
def get_daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

date_range = [dt.strftime("%Y-%m-%d") for dt in get_daterange(start_date, end_date)]


# Loop through the dates, add each pulled json as a value to the patents_dict, with key as the corresponding date
patents_dict = {}
null_dates = []

for index in range(len(date_range)) :

    print(date_range[index])
    parameters = {"lodgement_date" : date_range[index]}
    response = requests.get(API, params = parameters)

    if response.status_code == 200 :
        patents_dict[date_range[index]] = response.json()

    else :
        null_dates.append(date_range[index])
    

with open(PATH+"\\patents.json", "w") as json_file :
    json.dump(patents_dict, json_file)


## CODE FOR UPDATED API CALL FROM 18/12/2020 - 28/5/21
# Get list of strings of the range of dates to get from the API
start_date = date(2020, 12, 18)
end_date = date(2021, 5, 28)

# Generator object: Takes the number of days in between start and end date, creates a list of ints, and iterates through the ints 
# To get increment by 1 day timedelta from the start date
def get_daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

date_range = [dt.strftime("%Y-%m-%d") for dt in get_daterange(start_date, end_date)]


# Loop through the dates, add each pulled json as a value to the patents_dict, with key as the corresponding date
patents_dict = {}
null_dates = []

for index in range(len(date_range)) :

    print(date_range[index])
    parameters = {"lodgement_date" : date_range[index]}
    response = requests.get(API, params = parameters)

    if response.status_code == 200 :
        patents_dict[date_range[index]] = response.json()

    else :
        null_dates.append(date_range[index])
    

with open(PATH+"\\patents_181220_to_280521.json", "w") as json_file :
    json.dump(patents_dict, json_file)