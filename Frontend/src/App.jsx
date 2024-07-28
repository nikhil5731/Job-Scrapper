import { useEffect, useRef, useState } from "react";
import "./App.css";
import JobCard from "./components/JobCard";
import { io } from "socket.io-client";
import JobDesc from "./components/JobDesc";
import Image from "./assets/logo.png";
import { FaSpinner } from "react-icons/fa";

const keywords = [
  ".NET Development",
  "3D Printing",
  "ASP.NET Development",
  "Accounts",
  "Acting",
  "Aerospace Engineering",
  "Agriculture & Food Engineering",
  "Analytics",
  "Anchoring",
  "Android App Development",
  "Angular.js Development",
  "Animation",
  "Architecture",
  "Artificial Intelligence (AI)",
  "Audio Making/Editing",
  "Auditing",
  "Automobile Engineering",
  "Backend Development",
  "Bank",
  "Big Data",
  "Bioinformatics",
  "Biology",
  "Biotechnology Engineering",
  "Blockchain Development",
  "Blogging",
  "Brand Management",
  "Business Development",
  "Business/MBA",
  "CA Articleship",
  "CAD Design",
  "CMA Articleship",
  "CS Articleship",
  "Campus Ambassador",
  "Chartered Accountancy (CA)",
  "Chemical Engineering",
  "Chemistry",
  "Cinematography",
  "Civil Engineering",
  "Client Servicing",
  "Cloud Computing",
  "Commerce",
  "Company Secretary (CS)",
  "Computer Science",
  "Computer Vision",
  "Content Writing",
  "Copywriting",
  "Creative Design",
  "Creative Writing",
  "Culinary Arts",
  "Customer Service",
  "Cyber Security",
  "Data Entry",
  "Data Science",
  "Database Building",
  "Design",
  "Dietetics/Nutrition",
  "Digital Marketing",
  "E-commerce",
  "Editorial",
  "Electric Vehicle",
  "Electrical Engineering",
  "Electronics Engineering",
  "Embedded Systems",
  "Energy Science & Engineering",
  "Engineering",
  "Engineering Design",
  "Engineering Physics",
  "Environmental Sciences",
  "Event Management",
  "Facebook Marketing",
  "Fashion Design",
  "Film Making",
  "Finance",
  "Flutter Development",
  "Front End Development",
  "Full Stack Development",
  "Fundraising",
  "Game Design",
  "Game Development",
  "General Management",
  "Government",
  "Graphic Design",
  "Hospitality",
  "Hotel Management",
  "Human Resources (HR)",
  "Humanities",
  "Image Processing",
  "Industrial & Production Engineering",
  "Industrial Design",
  "Information Technology",
  "Instrumentation & Control Engineering",
  "Interior Design",
  "International",
  "Internet of Things (IoT)",
  "Java Development",
  "Javascript Development",
  "Journalism",
  "Law",
  "Legal Research",
  "Machine Learning",
  "Manufacturing Engineering",
  "Market/Business Research",
  "Marketing",
  "Material Science",
  "Mathematics",
  "Mathematics & Computing",
  "Mechanical Engineering",
  "Mechatronics",
  "Media",
  "Medicine",
  "Merchandise Design",
  "Mobile App Development",
  "Motion Graphics",
  "Music",
  "NGO",
  "Network Engineering",
  "Node.js Development",
  "Operations",
  "PHP Development",
  "Pharmaceutical",
  "Photography",
  "Physics",
  "Political/Economics/Policy Research",
  "Product Management",
  "Programming",
  "Project Management",
  "Proofreading",
  "Psychology",
  "Public Relations (PR)",
  "Python/Django Development",
  "Quality Analyst",
  "Recruitment",
  "Robotics",
  "Ruby on Rails",
  "Sales",
  "Science",
  "Search Engine Optimization (SEO)",
  "Social Media Marketing",
  "Social Work",
  "Software Development",
  "Software Testing",
  "Sports",
  "Statistics",
  "Stock/Market Trading",
  "Strategy",
  "Subject Matter Expert (SME)",
  "Supply Chain Management (SCM)",
  "Talent Acquisition",
  "Teaching",
  "Telecalling",
  "Transcription",
  "Translation",
  "Travel & Tourism",
  "UI/UX Design",
  "Video Making/Editing",
  "Videography",
  "Volunteering",
  "Web Development",
  "Wordpress Development",
  "iOS App Development",
];

const SOCKET_URL = "http://127.0.0.1:5000";
const socket = io(SOCKET_URL);

function App() {
  const [query, setQuery] = useState("Full Stack Development");
  const [filteredKeywords, setFilteredKeywords] = useState([]);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  const handleInputChange = (e) => {
    const value = e.target.value;
    setQuery(value);
    setFilteredKeywords(
      keywords.filter((keyword) =>
        keyword.toLowerCase().includes(value.toLowerCase())
      )
    );
    setIsDropdownOpen(true);
  };
  const handleClickOutside = (event) => {
    if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
      setIsDropdownOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const [selectedJob, setSelectedJob] = useState(-1);
  const [selectedJobDesc, setSelectedJobDesc] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activePortal, setActivePortal] = useState({
    internshala: true,
    unstop: true,
    linkedin: true,
    "naukri.com": true,
    cuvette: true,
  });
  const [currPage, setCurrPage] = useState(1);
  const hasMounted = useRef(false);

  useEffect(() => {
    // Listen for incoming messages
    socket.on("response", (data) => {
      const newJob = data["jobs"];
      setLoading(false);
      if (data.success) setJobs((prevJobs) => [...prevJobs, newJob]);
    });

    // Clean up the socket connection on component unmount
    return () => {
      socket.off("response");
    };
  }, []);

  useEffect(() => {
    if (hasMounted.current) {
      scrapeJobs();
    } else {
      hasMounted.current = true;
    }
  }, [currPage]);

  const scrapeJobs = () => {
    setLoading(true)
    setJobs([]);
    let jobRequest = [
      {
        url: `https://internshala.com/internships/${query}-internship/`,
        jobType: "Internship",
        scraper: "scrapeInternhsala",
        jobPortal: "internshala",
      },
      {
        url: `https://internshala.com/jobs/${query}-jobs/`,
        jobType: "FullTime",
        scraper: "scrapeInternhsala",
        jobPortal: "internshala",
      },
      {
        url: `https://unstop.com/api/public/opportunity/search-result?opportunity=jobs&searchTerm=${query}&oppstatus=open`,
        scraper: "scrapeUnstop",
        jobPortal: "unstop",
      },
      {
        url: `https://www.naukri.com/jobapi/v3/search?searchType=adv&location=india&keyword=${query}&experience=`,
        scraper: "scrapeNaukri",
        jobPortal: "naukri.com",
      },
      {
        url: `https://api.cuvette.tech/api/v1/externaljobs?search=${query}`,
        scraper: "scrapeCuvette",
        jobPortal: "cuvette",
      },
      {
        url: `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=${query}&location=India&f_TPR=r2592000`,
        scraper: "scrapeLinkedin",
        jobPortal: "linkedin",
      },
    ];
    jobRequest.forEach(({ url, jobType, scraper, jobPortal }) => {
      if (activePortal[`${jobPortal}`])
        socket.emit(scraper, { url, jobType, currPage });
    });
  };

  return (
    <div className="flex flex-col gap-2 h-screen  w-screen bg-gray-900 overflow-hidden">
      <h1 className="text-4xl font-bold w-full  my-5">
        <img src={Image} alt="Job Junction" className="m-auto -mt-14 -mb-20" />
      </h1>
      <div className="mx-10 flex flex-col gap-3 items-center">
        <div className="flex space-x-4">
          {Object.keys(activePortal).map((option, index) => (
            <label
              key={index}
              className="flex items-center space-x-2 cursor-pointer"
            >
              <input
                type="checkbox"
                checked={activePortal[option]}
                name={option}
                onChange={(e) =>
                  setActivePortal((prev) => ({
                    ...prev,
                    [option]: !activePortal[option],
                  }))
                }
                className="form-checkbox h-5 w-5 text-blue-600"
              />
              <span className="">
                {option.charAt(0).toUpperCase() + option.slice(1)}
              </span>
            </label>
          ))}
        </div>
        <div className="flex w-full gap-2 relative" ref={dropdownRef}>
          <input
            type="text"
            name="search"
            id="search"
            value={query}
            onChange={handleInputChange}
            placeholder="Search for the job"
            className=" outline-none px-5 py-3 rounded-xl w-4/5"
          />
          {isDropdownOpen && query && (
            <ul className="absolute left-0 top-full w-[50%] z-50 bg-gray-700 rounded-md mt-1 max-h-60 overflow-y-auto">
              {filteredKeywords.length > 0 ? (
                filteredKeywords.map((keyword, index) => (
                  <li
                    key={index}
                    className="p-2 hover:bg-gray-100 hover:text-black cursor-pointer text-left"
                    onClick={() => {
                      setQuery(keyword);
                      setIsDropdownOpen(false);
                    }}
                  >
                    {keyword}
                  </li>
                ))
              ) : (
                <li className="p-2 text-gray-500">No results found</li>
              )}
            </ul>
          )}

          <button
            className="bg-green-600 px-5 py-3 rounded-xl w-1/5"
            onClick={scrapeJobs}
          >
            Search
          </button>
        </div>
      </div>
      <div className="flex h-full w-full py-3">
        <div className="max--full bg-gray-900 w-[30%] px-2 overflow-y-scroll mb-44">
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <FaSpinner className="animate-spin text-4xl text-gray-500" />
            </div>
          ) : (
            jobs.map((ele, index) => {
              return (
                activePortal[`${ele["jobPortal"]}`] && (
                  <JobCard
                    isSelected={index === selectedJob}
                    onClick={() => {
                      setSelectedJob(index);
                      setSelectedJobDesc(ele);
                    }}
                    key={index}
                    data={ele}
                  />
                )
              );
            })
          )}
          <div className="my-3 flex justify-center gap-2">
            <button
              className={
                currPage > 1
                  ? "bg-green-600 px-2 w-full py-1 rounded-lg"
                  : "bg-green-900 text-gray-500 px-2 py-1 rounded-lg w-full"
              }
              onClick={() => {
                if (currPage > 1) {
                  setCurrPage((prev) => prev - 1);
                }
              }}
            >
              Prev
            </button>
            <input
              type="number"
              className="outline-none p-2 rounded-xl w-full"
              onChange={(e) => {
                setCurrPage(parseInt(e.target.value));
              }}
              min={1}
              max={100}
              value={currPage}
              placeholder="Page No."
            />
            <button
              className={
                currPage < 100
                  ? "bg-green-600 px-2 w-full py-1 rounded-lg"
                  : "bg-green-900 text-gray-500 px-2 py-1 rounded-lg w-full"
              }
              onClick={() => {
                if (currPage < 100) {
                  setCurrPage((prev) => prev + 1);
                }
              }}
            >
              Next
            </button>
          </div>
        </div>
        <div className="h-full w-[70%] pb-24">
          {selectedJobDesc ? (
            <JobDesc data={selectedJobDesc} />
          ) : (
            <div className="text-4xl font-serif text-gray-700 font-bold flex flex-col gap-3 justify-center items-center h-[75%]">
              Discover 10,000+ Jobs!
              <span className="text-lg">
                Across Internshala, LinkedIn, Naukri.com, Unstop & Cuvette
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
