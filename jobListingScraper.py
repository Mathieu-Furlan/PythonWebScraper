import requests
import csv
from bs4 import BeautifulSoup

def scrapeData():
    try:
        jobsListing = requests.get("https://realpython.github.io/fake-jobs/")
    
        if jobsListing.status_code == 200:
            parsedData = BeautifulSoup(jobsListing.text, "html.parser")
            jobs = parsedData.find_all(class_ = "card-content")
            with open("jobsFound.csv", "w", newline = "") as csvfile:
                fieldnames = ["job_title", "company_name", "location", "detail_URL"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for job in jobs:
                    jobTitle = job.find(class_ = "title is-5").text or ""
                    companyName = job.find(class_ = "subtitle is-6 company").text or ""
                    jobLocation = job.find(class_ = "location").text or ""
                    learnMore = job.find_all(class_ = "card-footer-item")[1]["href"] or ""
                    writer.writerow({"job_title": jobTitle, "company_name": companyName, "location": jobLocation, "detail_URL": learnMore})

        else:
            print(f"Error: Received status code {jobsListing.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

scrapeData()
