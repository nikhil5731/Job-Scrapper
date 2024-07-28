import requests
from flask_socketio import emit

# url = "https://unstop.com/api/public/opportunity/search-result?opportunity=jobs&searchTerm=fullstack%20developer&oppstatus=open"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Accept-Language": "en-GB,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.example.com/",
}


def extractAllJobsUnstopAPI(urlLink, currPage):
    # URL of the page you want to scrape
    # print("-----------UNSTOP SCRAPING-----------")
    response = requests.get(urlLink, headers=headers)
    res = response.json()
    totalPage = res["data"]["last_page"]
    if currPage > totalPage:
        emit("response", {"success": False, "message": "Page not found!"})
        return

    tempData = extractPage(res["data"]["links"][currPage]["url"])


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

    duration_experienceMin = data["job_detail"].get("min_experience", 0)
    duration_experienceMax = data["job_detail"].get("max_experience", 0)
    duration_experience = ""

    if duration_experienceMin:
        duration_experience = str(duration_experienceMin)
    else:
        duration_experience = "0"

    if duration_experienceMax:
        duration_experience += "-" + str(duration_experienceMax) + " experience"
    else:
        duration_experience += " experience"

    minSalary = format_number_indian(data["job_detail"].get("min_salary", 0))
    maxSalary = format_number_indian(data["job_detail"].get("max_salary", 0))
    salaryRange = ""

    if minSalary and maxSalary:
        salaryRange = f"Rs.{minSalary} - Rs.{maxSalary}"
    elif minSalary:
        salaryRange = f"Rs.{minSalary}"
    else:
        salaryRange = f"Rs.{maxSalary}"

    jobtype = str(data["job_detail"]["type"])
    if data["job_detail"]["timing"]:
        jobtype += ", " + str(data["job_detail"]["timing"])

    deadline = data["regnRequirements"]["remain_days"]
    skills = []
    eligibility = []

    return {
        "applications": str(viewsCount) + " views",
        "jobDescription": details,
        "opportunityType": jobtype,
        "deadline": deadline,
        "duration_experience": duration_experience,
        "salaryRange": salaryRange,
        "skillsOrTags": skills,
        "eligiblity": eligibility,
    }


def extractPage(url):
    response = requests.get(url, headers=headers)
    raw_data = response.json()
    jobs = raw_data["data"]["data"]
    total_no_of_jobs = raw_data["data"]["total"]

    finalData = []

    for job in jobs:
        job_data = {
            "position": job.get("title", None),
            "company": job.get("organisation", {}).get("name", None),
            "logo": job.get("logoUrl2", None),
            "location": ", ".join(job.get("jobDetail", {}).get("locations", [])),
            "duration_experience": None,
            "stipend": "Rs. "
            + format_number_indian(job.get("jobDetail", {}).get("max_salary", 0))
            + "(Max)",
            "link": f"https://unstop.com/{job.get('public_url', '')}",
            "uploadedOn": time_ago(job.get("start_date", None)),
            "opportunityType": job.get("type", None),
            "moreDetails": extractJob(job["id"]),
            "jobPortal": "unstop",
        }

        emit(
            "response",
            {
                "success": True,
                "message": "Unstop Jobs scraped successfully",
                "totalJobs": len(jobs),
                "jobs": job_data,
            },
        )
        finalData.append(job_data)

    # print(f"Jobs Scrapped: {len(jobs)}/{total_no_of_jobs}")
    return finalData


# def extractAllJobsUnstop(urlLink):
#     # URL of the page you want to scrape
#     print("-----------UNSTOP SCRAPING-----------")
#     response = requests.get(urlLink, headers=headers)
#     res = response.json()
#     length = len(res["data"]["links"])

#     finalData = []

#     for i in range(1, length - 1):
#         tempData = extractPage(res["data"]["links"][i]["url"])
#         finalData += tempData

#     with open("datas/unstop_data.json", "w", encoding="utf-8") as file:
#         json.dump(finalData, file, indent=4)

#     return finalData
