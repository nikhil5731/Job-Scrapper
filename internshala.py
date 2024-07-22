import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.google.com/",
}


def extractAllJobsInternshala(urlLink, jobType):
    print("-----------INTERNSHALA SCRAPING-----------")
    # URL of the page you want to scrape
    url = urlLink

    # Send a GET request to the URL
    intial_response = requests.get(url, headers=headers)

    if intial_response.status_code != 200:
        print(
            f"Failed to retrieve the webpage. Status code: {intial_response.status_code}"
        )
        return

    # Check if the request was successful
    # Get the content of the response
    intial_html_content = intial_response.content

    # Parse the HTML content using BeautifulSoup
    intial_soup = BeautifulSoup(intial_html_content, "html.parser")

    import re

    # Find the div with the specified ID
    totalPage = int(intial_soup.find("span", id="total_pages").get_text(strip=True))
    totalJobs = intial_soup.find("h1", class_="heading_4_6").get_text(strip=True)
    totalJobs = re.findall(r"\d+", totalJobs)[0]
    currPage = 1
    scrappedJobs = 0

    data = []

    while currPage <= totalPage:

        response = requests.get(url + f"/page-{currPage}", headers=headers)
        html_content = response.content

        soup = BeautifulSoup(html_content, "html.parser")

        cards = soup.find_all("div", class_="individual_internship")
        if cards:
            for children in cards:

                child = children.find("div", class_="internship_meta")

                temp_data = {}

                try:
                    position = child.find("h3", class_="job-internship-name").get_text(
                        strip=True
                    )
                except AttributeError:
                    position = None
                    continue

                try:
                    link = children.get("data-href")
                    if link != None:
                        moreDetails = extractJob("https://internshala.com" + link)
                    else:
                        moreDetails = {}
                except (AttributeError, ValueError):
                    link = "#"
                    moreDetails = {}
                    continue

                try:
                    company = child.find("p", class_="company-name").get_text(
                        strip=True
                    )
                except AttributeError:
                    company = None
                    continue

                try:
                    logo = (
                        child.find("div", class_="internship_logo")
                        .find("img")
                        .get("src")
                    )
                    if logo == "/static/images/search/placeholder_logo.svg":
                        logo = "#"
                except (AttributeError, AttributeError):
                    logo = "#"
                    continue

                try:
                    uploadedOn = child.find("div", class_="color-labels").get_text(
                        strip=True
                    )

                except (IndexError, AttributeError):
                    uploadedOn = None
                    continue

                try:
                    opportunityType = child.find("div", class_="gray-labels").get_text(
                        strip=True
                    )

                    if opportunityType == "":
                        opportunityType = jobType

                except (IndexError, AttributeError):
                    opportunityType = None
                    continue

                try:
                    temp = child.find_all("div", class_="detail-row-1")
                    details = []
                    for t in temp:
                        for child in t.children:
                            detail = child.get_text(strip=True)
                            if detail != "":
                                details.append(detail)

                    location = details[0]
                    duration_experience = details[1]
                    stipend = details[2]

                except (IndexError, AttributeError):
                    location = duration_experience = stipend = None
                    continue

                temp_data = {
                    "position": position,
                    "company": company,
                    "logo": logo,
                    "location": location,
                    "duration_experience": duration_experience,
                    "stipend": stipend,
                    "link": "https://internshala.com" + link,
                    "uploadedOn": uploadedOn,
                    "opportunityType": opportunityType,
                    "moreDetails": moreDetails,
                    "jobPortal": "internshala",
                }

                data.append(temp_data)

            scrappedJobs += len(cards)
            print(f"Jobs Scrapped: {scrappedJobs}/{totalJobs}")

        else:
            print("Not Found!")

        currPage += 1

    if jobType == "Internship":
        with open("datas/internshala_intern_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    else:
        with open("datas/internshala_jobs_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    return data


def extractJob(url):
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return {}

    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    templen = list(soup.find_all("div", class_="item_body"))
    if len(templen) == 0:
        return {}

    deadline = templen[len(templen) - 1].get_text(strip=True)
    applications = soup.find("div", class_="applications_message").get_text(strip=True)
    skills = soup.find("div", class_="round_tabs_container")

    skillsOrTags = (
        [child.get_text(strip=True) for child in skills.find_all(recursive=False)]
        if skills
        else []
    )

    jobDescription = soup.find("div", class_="text-container").getText()

    eligiblity = []

    if soup.find("div", class_="who_can_apply") != None:
        eligiblity = [
            child.get_text(strip=True)
            for child in soup.find("div", class_="who_can_apply").find_all(
                recursive=False
            )
        ]

    if soup.find("div", class_="additional_detail") != None:
        eligiblity += [
            child.get_text(strip=True)
            for child in soup.find("div", class_="additional_detail").find_all(
                recursive=False
            )
        ]

    return {
        "deadline": deadline,
        "applications": applications,
        "skillsOrTags": skillsOrTags,
        "jobDescription": jobDescription,
        "eligiblity": eligiblity,
    }
