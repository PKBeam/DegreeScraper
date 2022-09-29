import requests
import json
import time 
import csv
import os
import re
from bs4 import BeautifulSoup

def getMaxPageIndex():
    url = "https://accreditation.org/find-accredited-programs/university-search"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    maxPage = soup.find_all("li", class_=["pager__item--last"])[0].find_all("a")[0]["href"].split("=")[-1]
    return int(maxPage)
# need to avoid spamming the API
# make this bigger if you're getting rate limited
waitLength = 2 # seconds

index = 0

if os.path.exists("out.csv"):
	os.remove("out.csv")

csvFile = open("out.csv", "x")
csvWriter = csv.writer(csvFile)
csvWriter.writerow(["Degree name", "Institution", "Location", "Link"])

while index < getMaxPageIndex():
    print(f"Getting page {index}")
    url = f"https://accreditation.org/find-accredited-programs/university-search?page={index}"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    countries = soup.find_all("div", class_=["view-grouping"])
    for country in countries:
        countryName = country.find_all("h4")[0].contents[0]
        unis = country.find_all("div", class_=["views-row"])
        for uni in unis:
            urlHtml = uni.find_all("div", class_=["layout__region--first"])[0]
            urls = urlHtml.find_all("a")
            url = urlHtml.find_all("a")[0]["href"] if len(urls) > 0 else "N/A"

            institutionName = uni.find_all("div", class_=["layout__region--top"])[0].find_all("a")[0].contents[0]

            degreesHtml = uni.find_all("div", class_=["layout__region--second"])[0].find_all("p")[0]

            # get all the degree names
            degreeList = []

            degrees = str(degreesHtml)
            degrees = degrees.replace("<p>", "")
            degrees = degrees.replace("</p>", "")
            degrees = degrees.replace("</br>", "")
            degrees = degrees.replace("<br>", "")
            degrees = degrees.replace("<br/>", "")
            degrees = degrees.replace("&amp;", "&")
            degrees = re.sub(r"\[.*\]", "", degrees)

            for d in degrees.split("\n"):
                if len(d) == 0:
                    continue
                csvWriter.writerow([d, institutionName, countryName, url])

    time.sleep(waitLength)
    index += 1

csvFile.close()

