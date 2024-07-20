import requests
from bs4 import BeautifulSoup
import json
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Accept-Language": "en-GB,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.example.com/",
}

url = "https://unstop.com/api/public/opportunity/search-result?opportunity=jobs&searchTerm=software%20developerr&oppstatus=open"


def format_number_indian(n):
    n = str(n)
    if len(n) <= 3:
        return n
    else:
        last_three_digits = n[-3:]
        other_digits = n[:-3]
        other_digits_with_commas = ",".join(
            [other_digits[max(i - 2, 0) : i] for i in range(len(other_digits), 0, -2)][
                ::-1
            ]
        )
        return other_digits_with_commas + "," + last_three_digits


def extractJob(id):
    if id == None:
        return {}

    response = requests.get(f"https://unstop.com/api/public/competition/{id}")
    data = response.json()["data"]["competition"]

    viewsCount = data["viewsCount"]
    details = data["details"]
    jobtype = str(data["job_detail"]["type"]) + "-" + str(data["job_detail"]["timing"])
    deadline = data["end_date"]
    skills = []
    eligibility = data["regnRequirements"]["eligibility"]

    return {
        "applications": str(viewsCount) + " views",
        "jobDescription": details,
        "opportunityType": jobtype,
        "deadline": deadline,
        "skillsOrTags": skills,
        "eligiblity": eligibility,
    }


def extractPage(url):
    from datetime import datetime

    response = requests.get(url, headers=headers)
    jobs = response.json()["data"]["data"]

    finalData = []
    i = 1

    for job in jobs:
        tempData = {
            "position": job.get("title", None),
            "company": job.get("organisation", {}).get("name", None),
            "logo": job.get("logoUrl2", None),
            "location": ", ".join(job.get("jobDetail", {}).get("locations", [])),
            "duration": None,
            "stipend": "Rs. "
            + format_number_indian(job.get("jobDetail", {}).get("max_salary", 0))
            + "(Max)",
            "link": f"https://unstop.com/{job.get('public_url', '')}",
            "uploadedOn": job.get("start_date", None),
            "opportunityType": job.get("type", None),
            "moreDetails": extractJob(job["id"]),
            "jobPortal": "unstop",
        }

        finalData.append(tempData)
        i += 1

    return finalData


def extractAllJobsUnstop(urlLink):
    # URL of the page you want to scrape
    print("-----------UNSTOP SCRAPING-----------")
    response = requests.get(urlLink, headers=headers)
    res = response.json()
    length = len(res["data"]["links"])
    print(length)

    finalData = []

    for i in range(1, length - 1):
        print(i)
        tempData = extractPage(res["data"]["links"][i]["url"])
        finalData += tempData

    with open("datas/unstop_data.json", "w", encoding="utf-8") as file:
        json.dump(finalData, file, indent=4)

    return finalData


# extractAllJobsUnstop(url)
