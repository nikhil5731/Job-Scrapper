import requests
from bs4 import BeautifulSoup
import json
import time
from flask_socketio import emit

# url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Fullstack+Developer&location=India&f_TPR=r2592000"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Accept-Language": "en-GB,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.google.com/",
}


def extractAllJobsLinkedInAPI(urlLink, currPage):
    # print("-----------LINKEDIN SCRAPING-----------")
    jobsSkip = 10
    if (jobsSkip * (currPage - 1)) >= 1000:
        emit("response", {"success": False, "message": "Page Not Found!"})
        return

    url = f"{urlLink}&start={jobsSkip*(currPage-1)}"
    html_content = make_request(url, 1)

    if html_content is None:
        emit("response", {"success": False, "message": "Page Not Found!"})
        return

    soup = BeautifulSoup(html_content, "html.parser")
    alljobs_on_this_page = soup.find_all("div", class_="base-card")

    if not alljobs_on_this_page:
        emit("response", {"success": False, "message": "Page Not Found!"})
        return

    for job in alljobs_on_this_page:
        job_data = parse_job_data(job)
        if job_data:
            emit(
                "response",
                {
                    "success": True,
                    "totalJobs": len(alljobs_on_this_page),
                    "jobs": job_data,
                    "message": "Internshala Jobs scraped successfully",
                },
            )


def make_request(url, numberOfRequests):

    response = requests.get(url, headers=headers)

    if response.status_code == 429:
        if numberOfRequests >= 10:
            return None
        print("Rate limit exceeded. Retrying...")
        time.sleep(2)
        return make_request(url, numberOfRequests + 1)

    if response.status_code != 200:
        # print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

    return response.content


def parse_job_data(job):
    temp_data = {}
    try:
        temp_data["position"] = job.find(
            "h3", class_="base-search-card__title"
        ).get_text(strip=True)
        temp_data["link"] = job.find("a", class_="base-card__full-link").get("href")
        temp_data["logo"] = job.find("img", class_="artdeco-entity-image").get(
            "data-delayed-url"
        )
        temp_data["company"] = job.find(
            "h4", class_="base-search-card__subtitle"
        ).get_text(strip=True)
        temp_data["location"] = job.find(
            "span", class_="job-search-card__location"
        ).get_text(strip=True)
        temp_data["uploadedOn"] = job.find(
            "time", class_="job-search-card__listdate"
        ).get_text(strip=True)
    except AttributeError:
        return None  # Return None if any data is missing

    temp_data["moreDetails"] = extractJob(temp_data["link"], 1)
    temp_data["jobPortal"] = "linkedin"
    return temp_data


def extractJob(url, numberOfRequests):
    # Send a GET request to the URL
    response = requests.get(url, headers=headers)

    if response.status_code == 429:
        # print("Failed to extract a job! Trying Again...")
        if numberOfRequests >= 10:
            return {}
        time.sleep(2)
        return extractJob(url, numberOfRequests + 1)

    if response.status_code != 200:
        # print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return {}

    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    try:
        applications = soup.find("span", class_="num-applicants__caption").get_text(
            strip=True
        )
    except AttributeError:
        applications = "Be among the first 25 applicants"

    try:
        jobDescription = soup.find(
            "div", class_="show-more-less-html__markup"
        ).getText()
    except AttributeError:
        jobDescription = ""

    try:
        opportunityType = (
            soup.find_all("span", class_="description__job-criteria-text")[1].get_text(
                strip=True
            )
            if len(soup.find_all("span", class_="description__job-criteria-text")) > 1
            else "Not found"
        )
        duration_experience = (
            soup.find_all("span", class_="description__job-criteria-text")[0].get_text(
                strip=True
            )
            if len(soup.find_all("span", class_="description__job-criteria-text")) > 1
            else "Not found"
        )
    except AttributeError:
        opportunityType = ""
        duration_experience = ""

    deadline = None
    skillsOrTags = []
    eligiblity = []

    return {
        "applications": applications,
        "jobDescription": jobDescription,
        "opportunityType": opportunityType,
        "duration_experience": duration_experience,
        "deadline": deadline,
        "skillsOrTags": skillsOrTags,
        "eligiblity": eligiblity,
    }


def save_data_to_file(data):
    with open("datas/linkedIn_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# def extractAllJobsLinkedIn(urlLink):
#     print("-----------LINKEDIN SCRAPING-----------")
#     jobsSkip = 0
#     data = []
#     totalJobs = 100

#     while jobsSkip <= totalJobs:
#         url = f"{urlLink}&start={jobsSkip}"
#         html_content = make_request(url)
#         if html_content is None:
#             break

#         soup = BeautifulSoup(html_content, "html.parser")
#         alljobs_on_this_page = soup.find_all("div", class_="base-card")

#         if not alljobs_on_this_page:
#             break

#         for job in alljobs_on_this_page:
#             job_data = parse_job_data(job)
#             if job_data:
#                 data.append(job_data)

#         print(f"Jobs Scrapped: {jobsSkip}/{totalJobs}")
#         jobsSkip += 10

#     save_data_to_file(data)
#     return data
