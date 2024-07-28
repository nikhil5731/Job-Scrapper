import requests
from bs4 import BeautifulSoup
from flask_socketio import emit
import re


# internhala_jobs = extractAllJobsInternshala(
#         "https://internshala.com/jobs/fullstack-development-jobs/", "FullTime"
#     )

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.google.com/",
}


def extractAllJobsInternshalaAPI(url, jobType, currPage):
    # print("-----------INTERNSHALA SCRAPING-----------")

    if not jobType:
        emit("response", {"success": False, "message": "jobType not found!"})
        return

    if not url:
        emit("response", {"success": False, "message": "url not found!"})
        return

    initial_html_content = fetch_page(url)

    if initial_html_content is None:
        emit("response", {"success": False, "message": "Page not found!"})
        return

    initial_soup = BeautifulSoup(initial_html_content, "html.parser")
    totalPage = parse_total_jobs(initial_soup)

    if totalPage < currPage:
        emit("response", {"success": False, "message": "Page not found!"})
        return

    html_content = fetch_page(url + f"/page-{currPage}")
    if html_content is None:
        return

    soup = BeautifulSoup(html_content, "html.parser")
    cards = soup.find_all("div", class_="individual_internship")
    if cards:
        for children in cards:
            # child = children.find("div", class_="internship_meta")
            job_data = extract_job_details(children, jobType)
            if job_data:
                emit(
                    "response",
                    {
                        "success": True,
                        "totalJobs": len(cards),
                        "jobs": job_data,
                        "message": "Internshala Jobs scraped successfully",
                    },
                )

    else:
        emit("response", {"success": False, "message": "Page Not Found!"})
        return


def fetch_page(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        # print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None
    return response.content


def parse_total_jobs(soup):
    totalPage = int(soup.find("span", id="total_pages").get_text(strip=True))
    totalJobs = int(
        re.findall(r"\d+", soup.find("h1", class_="heading_4_6").get_text(strip=True))[
            0
        ]
    )
    return totalPage


def stipendHelper(text):

    # Find the last occurrence of the "₹" symbol
    last_rupee_index = text.rfind("₹")

    # Find the first occurrence of "/year" after the last "₹"
    end_index = text.find("/year", last_rupee_index)

    # Extract the value between the last "₹" and "/year"
    value_between = text[last_rupee_index:end_index].strip()

    return value_between + "/year"  # Output: ₹ 7,00,000 - 8,00,000


def extract_job_details(child, jobType):
    temp_data = {}
    try:
        position = child.find("h3", class_="job-internship-name").get_text(strip=True)
        link = child.get("data-href")

        moreDetails = extractJob("https://internshala.com" + link) if link else {}
        company = child.find("p", class_="company-name").get_text(strip=True)
        logo = child.find("div", class_="internship_logo").find("img").get("src", "#")
        uploadedOn = child.find("div", class_="color-labels").get_text(strip=True)
        opportunityType = (
            child.find("div", class_="gray-labels").get_text(strip=True) or jobType
        )
        location, duration_experience, stipend = extract_details(child)
        if jobType == "FullTime":
            stipend = stipendHelper(stipend)
        temp_data = {
            "position": position,
            "company": company,
            "logo": logo,
            "location": location,
            "duration_experience": duration_experience,
            "stipend": stipend,
            "link": "https://internshala.com" + link if link else "#",
            "uploadedOn": uploadedOn,
            "opportunityType": opportunityType,
            "moreDetails": moreDetails,
            "jobPortal": "internshala",
        }
    except AttributeError:
        return None
    return temp_data


def extract_details(child):
    try:
        temp = child.find_all("div", class_="detail-row-1")
        details = [
            child.get_text(strip=True)
            for t in temp
            for child in t.children
            if child.get_text(strip=True)
        ]
        return details[0], details[1], details[2]
    except (IndexError, AttributeError):
        return None, None, None


def extractJob(url):
    response_content = fetch_page(url)
    if response_content is None:
        return {}

    soup = BeautifulSoup(response_content, "html.parser")
    templen = list(soup.find_all("div", class_="item_body"))
    if not templen:
        return {}

    deadline = templen[-1].get_text(strip=True)
    applications = soup.find("div", class_="applications_message").get_text(strip=True)
    skillsOrTags = (
        [
            child.get_text(strip=True)
            for child in soup.find("div", class_="round_tabs_container").find_all(
                recursive=False
            )
        ]
        if soup.find("div", class_="round_tabs_container")
        else []
    )
    jobDescription = soup.find("div", class_="text-container").getText()
    eligiblity = extract_eligibility(soup)

    return {
        "deadline": deadline,
        "applications": applications,
        "skillsOrTags": skillsOrTags,
        "jobDescription": jobDescription,
        "eligiblity": eligiblity,
    }


def extract_eligibility(soup):
    eligiblity = []
    for class_name in ["who_can_apply", "additional_detail"]:
        section = soup.find("div", class_=class_name)
        if section:
            eligiblity += [
                child.get_text(strip=True)
                for child in section.find_all(recursive=False)
            ]
    return eligiblity


# def extractAllJobsInternshala(urlLink, jobType):
#     print("-----------INTERNSHALA SCRAPING-----------")
#     url = urlLink
#     initial_html_content = fetch_page(url)
#     if initial_html_content is None:
#         return

#     initial_soup = BeautifulSoup(initial_html_content, "html.parser")
#     totalPage, totalJobs = parse_total_jobs(initial_soup)
#     currPage = 1
#     scrappedJobs = 0
#     data = []

#     while currPage <= totalPage:
#         html_content = fetch_page(url + f"/page-{currPage}")
#         if html_content is None:
#             break

#         soup = BeautifulSoup(html_content, "html.parser")
#         cards = soup.find_all("div", class_="individual_internship")
#         if cards:
#             for children in cards:
#                 # child = children.find("div", class_="internship_meta")
#                 job_data = extract_job_details(children, jobType)
#                 if job_data:
#                     data.append(job_data)

#             scrappedJobs += len(cards)
#             print(f"Jobs Scrapped: {scrappedJobs}/{totalJobs}")
#         else:
#             print("Not Found!")

#         currPage += 1

#     output_file = (
#         "datas/internshala_intern_data.json"
#         if jobType == "Internship"
#         else "datas/internshala_jobs_data.json"
#     )
#     with open(output_file, "w", encoding="utf-8") as file:
#         json.dump(data, file, indent=4)

#     return data
