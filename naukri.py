import requests
import json
from datetime import datetime, timedelta

# const url = "https://www.naukri.com/jobapi/v3/search?searchType=adv&location=india&keyword=fullstack%20developer&experience=0"

headers = {
    "User-Agent": "PostmanRuntime/7.40.0",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/",
    "Appid": "202",
    "Systemid": "Naukri",
}


def time_ago(date):
    now = datetime.now()
    seconds = (now - date).total_seconds()

    intervals = [
        (31536000, "years"),
        (2592000, "months"),
        (604800, "weeks"),
        (86400, "days"),
        (3600, "hours"),
        (60, "minutes"),
        (1, "seconds"),
    ]

    for interval, name in intervals:
        count = seconds // interval
        if count > 1:
            return f"{int(count)} {name} ago"
        if count == 1:
            return f"1 {name} ago"

    return f"{int(seconds)} seconds ago"


def extractAllJobsNaukri(url):
    print("-----------NAUKRI.COM SCRAPING-----------")
    extracted_jobs = 0
    total_no_of_jobs = None
    final_data = []
    i = 1

    while True:
        try:
            if total_no_of_jobs is None:
                response = requests.get(url, headers=headers)
                data = response.json()
                total_no_of_jobs = data["noOfJobs"]

            if total_no_of_jobs and extracted_jobs >= total_no_of_jobs:
                break

            job_details = extract_jobs_from_page(
                url, i, extracted_jobs, total_no_of_jobs
            )
            final_data.extend(job_details)
            extracted_jobs += 20
            i += 1
        except Exception as err:
            print(err)
            break

    with open("datas/naukri_data.json", "w") as f:
        json.dump(final_data, f)

    return final_data


def extract_jobs_from_page(url, page_no, extracted_jobs, total_no_of_jobs):

    response = requests.get(f"{url}&pageNo={page_no}", headers=headers)
    data = response.json()

    if total_no_of_jobs is None:
        total_no_of_jobs = data["noOfJobs"]

    jobs = [
        {
            "position": item.get("title"),
            "company": item.get("companyName"),
            "logo": item.get("logoPath", "#"),
            "location": item.get("placeholders", [None, None, None])[2].get("label"),
            "duration": item.get("placeholders", [None, None, None])[0].get("label"),
            "stipend": item.get("placeholders", [None, None, None])[1].get("label"),
            "link": "https://www.naukri.com" + item.get("jdURL"),
            "uploadedOn": item.get("createdDate"),
            "opportunityType": item.get("jobType", "Full Time"),
            "moreDetails": extract_jobs(item.get("jobId")),
            "jobPortal": "naukri.com",
        }
        for item in data["jobDetails"]
    ]

    print(f"Jobs Scrapped: {extracted_jobs}/{total_no_of_jobs}")
    
    return jobs


def extract_jobs(job_id):
    individual_job = f"https://www.naukri.com/jobapi/v4/job/{job_id}"

    more_details = {}
    try:
        response = requests.get(individual_job, headers=headers)
        data = response.json()["jobDetails"]

        more_details = {
            "applications": data.get("applyCount"),
            "jobDescription": data.get("description"),
            "opportunityType": data.get("jobType"),
            "deadline": None,
            "skillsOrTags": [
                item["label"]
                for ele in data.get("keySkills", {}).values()
                for item in ele
            ],
            "eligibility": None,
        }
    except Exception as error:
        print(error)

    return more_details


# extractAllJobsNaukri(
#     "https://www.naukri.com/jobapi/v3/search?searchType=adv&location=india&keyword=fullstack%20developer&experience=0"
# )
