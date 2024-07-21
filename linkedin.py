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
    "Referer": "https://www.google.com/",
}


def extractAllJobsLinkedIn(urlLink):
    print("-----------LINKEDIN SCRAPING-----------")
    jobsSkip = 0
    data = []
    totalJobs = 500

    # Send a GET request to the URL
    while jobsSkip <= 500:
        url = urlLink + f"&start={jobsSkip}"

        response = requests.get(url, headers=headers)

        if response.status_code == 400:
            print(f"Done Scraping: {response.status_code}")
            break

        if response.status_code == 429:
            print("Failed to get current page! Trying again...")
            time.sleep(1)
            continue

        if response.status_code != 200:
            print(
                f"Failed to retrieve the webpage. Status code: {response.status_code}"
            )
            break

        # Check if the request was successful
        # Get the content of the response
        html_content = response.content

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        alljobs_on_this_page = soup.find_all("div", class_="base-card")

        if len(alljobs_on_this_page) == 0:
            break

        # data = []

        if alljobs_on_this_page:
            for job in alljobs_on_this_page:
                temp_data = {}

                try:
                    position = job.find(
                        "h3", class_="base-search-card__title"
                    ).get_text(strip=True)
                except AttributeError:
                    position = None
                    continue

                try:
                    link = job.find("a", class_="base-card__full-link").get("href")
                    moreDetails = extractJob(link)
                except AttributeError:
                    link = "#"
                    moreDetails = {}
                    continue

                try:
                    logo = job.find("img", class_="artdeco-entity-image").get(
                        "data-delayed-url"
                    )
                except AttributeError:
                    logo = None
                    continue

                try:
                    company = job.find(
                        "h4", class_="base-search-card__subtitle"
                    ).get_text(strip=True)
                except AttributeError:
                    company = None
                    continue

                try:
                    location = job.find(
                        "span", class_="job-search-card__location"
                    ).get_text(strip=True)
                except AttributeError:
                    location = None
                    continue

                try:
                    uploadedOn = job.find(
                        "time", class_="job-search-card__listdate"
                    ).get_text(strip=True)
                except AttributeError:
                    try:
                        uploadedOn = job.find(
                            "time", class_="job-search-card__listdate--new"
                        ).get_text(strip=True)
                    except AttributeError:
                        uploadedOn = None
                        continue

                temp_data = {
                    "position": position,
                    "company": company,
                    "logo": logo,
                    "location": location,
                    "duration": None,
                    "stipend": None,
                    "link": link,
                    "uploadedOn": uploadedOn,
                    "opportunityType": None,
                    "moreDetails": moreDetails,
                    "jobPortal": "linkedin",
                }

                data.append(temp_data)

            
            jobsSkip += 10
            print(f"Jobs Scrapped: {jobsSkip}/{totalJobs}")

        else:
            print("Not Found!")
            break

    with open("datas/linkedIn_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return data


def extractJob(url):
    # Send a GET request to the URL
    response = requests.get(url, headers=headers)

    if response.status_code == 429:
        print("Failed to extract a job! Trying Again...")
        time.sleep(1)
        return extractJob(url=url)

    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
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
    except AttributeError:
        opportunityType = ""

    deadline = None
    skillsOrTags = []
    eligiblity = []

    return {
        "applications": applications,
        "jobDescription": jobDescription,
        "opportunityType": opportunityType,
        "deadline": deadline,
        "skillsOrTags": skillsOrTags,
        "eligiblity": eligiblity,
    }


aWeekAgo = "r604800"
aDayAgo = "r86400"
aMonthAgo = "r2592000"

# extractAllJobsLinkedIn(
#     "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Software+Developer&location=India&f_TPR=r2592000"
# )
