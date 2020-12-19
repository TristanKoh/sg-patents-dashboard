import json

PATH = "C:\\Users\\Tristan\\Desktop\\Computational_Law\\IP_Dashboard\\Data"

with open(PATH + "\\patents.json") as f:
    patents = json.load(f)

date_range = list(patents.keys())

# Pretty prints one patent application for one day to visualise the dictionary structure
print(json.dumps(patents[date_range[4]]["items"][1], indent = 4))

print(json.dumps(patents[date_range[4]]["items"][1]["applicationNum"], indent = 4))