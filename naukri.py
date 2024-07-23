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


def time_ago(date_str):
    try:
        from datetime import datetime, timezone

        if date_str == None:
            return ""

        date_str = date_str.split("T")[0]
        date_format = "%Y-%m-%d"
        parsed_date = datetime.strptime(date_str, date_format)
        parsed_date = parsed_date.replace(tzinfo=timezone.utc)

        # Get the current time
        now = datetime.now(timezone.utc)

        # Calculate the difference between now and the parsed date
        time_difference = now - parsed_date

        # Define time intervals
        seconds = time_difference.total_seconds()
        minutes = seconds / 60
        hours = minutes / 60
        days = hours / 24
        weeks = days / 7
        months = days / 30
        years = days / 365

        # Determine the "time ago" format
        if seconds < 60:
            return f"{int(seconds)} seconds ago"
        elif minutes < 60:
            return f"{int(minutes)} minutes ago"
        elif hours < 24:
            return f"{int(hours)} hours ago"
        elif days < 7:
            return f"{int(days)} days ago"
        elif weeks < 4:
            return f"{int(weeks)} weeks ago"
        elif months < 12:
            return f"{int(months)} months ago"
        else:
            return f"{int(years)} years ago"

    except Exception as e:
        return "Invalid date string"


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
            "duration_experience": item.get("placeholders", [None, None, None])[0].get("label"),
            "stipend": item.get("placeholders", [None, None, None])[1].get("label"),
            "link": "https://www.naukri.com" + item.get("jdURL"),
            "uploadedOn": time_ago(
                str(datetime.fromtimestamp(item.get("createdDate") / 1000)).split(" ")[
                    0
                ]
            ),
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
