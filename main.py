from internshala import extractAllJobsInternshala
from unstop import extractAllJobsUnstop
from linkedin import extractAllJobsLinkedIn
from naukri import extractAllJobsNaukri
import json


internhala = extractAllJobsInternshala(
    "https://internshala.com/internships/fullstack-development-internship/"
)
linkedIn = extractAllJobsLinkedIn(
    "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Fullstack+Developer&location=India&f_TPR=r2592000"
)
unstop = extractAllJobsUnstop(
    "https://unstop.com/api/public/opportunity/search-result?opportunity=jobs&searchTerm=fullstack%20developerr&oppstatus=open"
)
naukri = extractAllJobsNaukri(
    "https://www.naukri.com/jobapi/v3/search?searchType=adv&location=india&keyword=fullstack%20developer&experience=0"
)


master = internhala + linkedIn + unstop + naukri

with open("datas/master.json", "w", encoding="utf-8") as file:
    json.dump(master, file, indent=4)
