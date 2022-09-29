import requests
import json
import time 
import csv
import os

def getDegreeLink(id):
	return f"https://www.bachelorsportal.com/studies/{id}/"

def getCountries(venues):
	out = []
	for v in venues:
		if v["country"] not in out:
			out.append(v["country"])
	return ", ".join(out)

# 10,000 results maximum
maxLimit = 10000

# need to avoid spamming the API
# make this bigger if you're getting rate limited
waitLength = 2 # seconds

# API-enforced maximum of 100
size = 100

index = 0

url = f"https://search.prtl.co/2018-07-23/?q=en-1705|lv-bachelor|uc-202|tc-AUD&size={size}&start={index}"

if os.path.exists("out.csv"):
	os.remove("out.csv")

csvFile = open("out.csv", "x")
csvWriter = csv.writer(csvFile)
csvWriter.writerow(["Degree name", "Duration", "Institution", "Country", "Description", "Link"])

while index + size <= maxLimit:
	time.sleep(waitLength)
	result = requests.get(url)
	for obj in result.json():
		id = obj["id"]
		title = obj["title"]
		duration = obj["fulltime_duration"] if "fulltime_duration" in obj.keys() else None
		durationString = str(duration["value"]) + " " + duration["unit"] + ("s" if duration["value"] > 1 else "") if duration else "N/A" 
		csvWriter.writerow([ obj["title"], durationString, obj["organisation"], getCountries(obj["venues"]), obj["summary"], getDegreeLink(id)])
	
	index += size

csvFile.close()
