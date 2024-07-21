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


def extractAllJobsInternshala(urlLink,jobType):
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
        # Send a GET request to the URL
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
                except (AttributeError, AttributeError) as e:
                    logo = "#"
                    continue

                try:
                    uploadedOn = child.find("div", class_="color-labels").get_text(
                        strip=True
                    )

                except (IndexError, AttributeError) as e:
                    uploadedOn = None
                    continue

                try:
                    opportunityType = child.find("div", class_="gray-labels").get_text(
                        strip=True
                    )

                    if opportunityType == "":
                        opportunityType = jobType

                except (IndexError, AttributeError) as e:
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

    with open("datas/internshala_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return data


def extractJob(url):
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return

    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    deadline = (
        soup.find("div", class_="apply_by")
        .find("div", class_="item_body")
        .get_text(strip=True)
    )
    applications = soup.find("div", class_="applications_message").get_text(strip=True)
    skills = soup.find("div", class_="round_tabs_container")

    skillsOrTags = [
        child.get_text(strip=True) for child in skills.find_all(recursive=False)
    ]

    jobDescription = soup.find("div", class_="text-container").getText()
    eligiblity = [
        child.get_text(strip=True)
        for child in soup.find("div", class_="who_can_apply").find_all(recursive=False)
    ]

    return {
        "deadline": deadline,
        "applications": applications,
        "skillsOrTags": skillsOrTags,
        "jobDescription": jobDescription,
        "eligiblity": eligiblity,
    }


# extractAllJobsInternshala(
#     "https://internshala.com/internships/software-development-internship/"
# )
