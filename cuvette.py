import requests
import json

# url = "https://api.cuvette.tech/api/v1/externaljobs?search=internship,software"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Accept-Language": "en-GB,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.google.com/",
}


def extractAllCuvette(urlLink):
    print("-----------CUVETTE SCRAPING-----------")
    response = requests.get(urlLink, headers)
    raw_data = response.json()
    totalJobs = raw_data["count"]
    jobArray = raw_data["data"]

    finalData = []

    for job in jobArray:
        filteredJob = (
            {
                "position": job["title"],
                "company": job["companyName"],
                "logo": job["imageUrl"],
                "location": job["location"],
                "duration": job["requiredExperience"],
                "stipend": job["salary"],
                "link": job["redirectLink"],
                "uploadedOn": job["createdAt"],
                "opportunityType": job["type"],
                "moreDetails": {
                    "deadline": None,
                    "applications": job["count"],
                    "skillsOrTags": job["skills"].split(", "),
                    "jobDescription": job["aboutJob"],
                    "eligiblity": job["aboutJob"],
                },
                "jobPortal": "cuvette",
            },
        )
        finalData.append(filteredJob)

    with open("datas/cuvette_data.json", "w", encoding="utf-8") as file:
        json.dump(finalData, file, indent=4)

    print(f"Jobs Scrapped: {totalJobs}/{totalJobs}")
    return finalData


# extractAllCuvette(url)
