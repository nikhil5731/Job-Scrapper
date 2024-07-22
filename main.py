from internshala import extractAllJobsInternshala
from unstop import extractAllJobsUnstop
from linkedin import extractAllJobsLinkedIn
from naukri import extractAllJobsNaukri
from cuvette import extractAllCuvette
import json


def extractAllJobs():

    master = []

    internhala_jobs = extractAllJobsInternshala(
        "https://internshala.com/jobs/fullstack-development-jobs/", "FullTime"
    )

    master += internhala_jobs

    internhala_intern = extractAllJobsInternshala(
        "https://internshala.com/internships/software-development-internship/",
        "Internship",
    )

    master += internhala_intern

    unstop = extractAllJobsUnstop(
        "https://unstop.com/api/public/opportunity/search-result?opportunity=jobs&searchTerm=fullstack%20developer&oppstatus=open"
    )

    master += unstop

    naukri = extractAllJobsNaukri(
        "https://www.naukri.com/jobapi/v3/search?searchType=adv&location=india&keyword=fullstack%20developer&experience=0"
    )

    master += naukri

    cuvette = extractAllCuvette(
        "https://api.cuvette.tech/api/v1/externaljobs?search=internship,software"
    )

    master += cuvette

    linkedIn = extractAllJobsLinkedIn(
        "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Fullstack+Developer&location=India&f_TPR=r2592000"
    )

    master += linkedIn
    
    with open("datas/master.json", "w", encoding="utf-8") as file:
        json.dump(master, file, indent=4)

    return master


if __name__ == "__main__":
    master = extractAllJobs()
    print("Done Scrapping!")