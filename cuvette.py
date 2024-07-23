import requests
import json


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Accept-Language": "en-GB,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.google.com/",
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
                "duration_experience": job["requiredExperience"],
                "stipend": job["salary"],
                "link": job["redirectLink"],
                "uploadedOn": time_ago(job["createdAt"]),
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
        finalData += filteredJob

    with open("datas/cuvette_data.json", "w", encoding="utf-8") as file:
        json.dump(finalData, file, indent=4)

    print(f"Jobs Scrapped: {totalJobs}/{totalJobs}")
    return finalData
