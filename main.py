from internshala import extractAllJobsInternshala
from unstop import extractAllJobsUnstop
from linkedin import extractAllJobsLinkedIn
from naukri import extractAllJobsNaukri
from cuvette import extractAllCuvette
import json


# internhala = extractAllJobsInternshala(
#     "https://internshala.com/jobs/fullstack-development-jobs/","FullTime Job"
# )

internhala = extractAllJobsInternshala(
    "https://internshala.com/internships/software-development-internship/","Internship"
)

unstop = extractAllJobsUnstop(
    "https://unstop.com/api/public/opportunity/search-result?opportunity=jobs&searchTerm=fullstack%20developer&oppstatus=open"
)

naukri = extractAllJobsNaukri(
    "https://www.naukri.com/jobapi/v3/search?searchType=adv&location=india&keyword=fullstack%20developer&experience=0"
)

cuvette = extractAllCuvette(
    "https://api.cuvette.tech/api/v1/externaljobs?search=internship,software"
)

linkedIn = extractAllJobsLinkedIn(
    "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Fullstack+Developer&location=India&f_TPR=r2592000"
)

master = internhala  + unstop + naukri + cuvette

with open("datas/master.json", "w", encoding="utf-8") as file:
    json.dump(master, file, indent=4)
