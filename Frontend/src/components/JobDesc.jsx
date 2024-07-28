import React, { useState } from "react";
import { FaCopy } from "react-icons/fa";
import { FaCircleCheck } from "react-icons/fa6";

function capitalizeFirstLetter(string) {
  return string?.charAt(0).toUpperCase() + string?.slice(1);
}

const JobDesc = ({ data }) => {
  const [icon, setIcon] = useState("copy"); // Default icon is 'copy'

  //   if (!data) return <div></div>;
  const {
    company,
    duration_experience,
    jobPortal,
    link,
    location,
    opportunityType,
    stipend,
    logo,
    position,
    moreDetails,
    uploadedOn,
  } = data;
  const { applications, deadline, eligiblity, jobDescription, skillsOrTags } =
    moreDetails;
  return (
    <div className="h-[90%] w-full overflow-y-scroll">
      <div className="p-5 rounded-2xl bg-gray-900 flex flex-col gap-5 pb-[7rem] items-start">
        <div className="flex items-center gap-5">
          <img
            src={logo}
            alt={company}
            onError={(e) => {
              e.target.src =
                "https://media.istockphoto.com/id/1055079680/vector/black-linear-photo-camera-like-no-image-available.jpg?s=612x612&w=0&k=20&c=P1DebpeMIAtXj_ZbVsKVvg-duuL0v9DlrOZUvPG6UJk=";
            }}
            width={100}
            className="rounded-xl"
          />
          <div className="flex flex-col items-start">
            <h2 className="text-2xl font-bold text-left">{position}</h2>
            <h3 className="text-lg text-gray-300 text-left">{company}</h3>
          </div>
        </div>
        <div className="flex w-full justify-between">
          <div className="flex flex-col gap-3 w-full pr-5">
            {jobDescription && (
              <div>
                <h3 className="text-xl font-bold text-green-400 text-left">
                  Job Descriptions
                </h3>
                {/* <p className="text-left whitespace-pre-line">{jobDescription}</p> */}
                <p
                  className="text-left whitespace-pre-line"
                  dangerouslySetInnerHTML={{ __html: jobDescription }}
                ></p>
              </div>
            )}
            {eligiblity && eligiblity.length > 0 && (
              <div>
                <h3 className="text-xl font-bold text-green-400 text-left">
                  Requirements
                </h3>
                {Array.isArray(eligiblity) &&
                  eligiblity?.map((ele, index) => (
                    <p className="text-left">{ele}</p>
                  ))}
              </div>
            )}
          </div>
          <div className="flex flex-col items-start w-1/2 border-l-2 h-fit border-gray-800 pl-5">
            <span className="text-green-500 font-semibold text-2xl text-left">
              <span className="text-white">{stipend}</span>
            </span>
            {(duration_experience || moreDetails.duration_experience) && (
              <span className="text-green-500 font-semibold text-left">
                Duration/Experience:{" "}
                <span className="text-white">
                  {duration_experience || moreDetails.duration_experience}
                </span>
              </span>
            )}
            {(location || moreDetails.location) && (
              <span className="text-green-500 font-semibold text-left">
                Location:{" "}
                <span className="text-white">
                  {location || moreDetails.location}
                </span>
              </span>
            )}
            {(opportunityType || moreDetails.opportunityType) && (
              <span className="text-green-500 font-semibold text-left">
                Type:{" "}
                <span className="text-white">
                  {capitalizeFirstLetter(
                    opportunityType || moreDetails.opportunityType
                  )}
                </span>
              </span>
            )}

            {applications && (
              <span className="text-green-500 font-semibold text-left">
                Applications:{" "}
                <span className="text-white ">{applications}</span>
              </span>
            )}
            {deadline && !deadline.includes("₹") && (
              <span className="text-green-500 font-semibold text-left">
                Deadline: <span className="text-white">{deadline}</span>
              </span>
            )}
            <span className="text-green-500 font-semibold text-left">
              Uploaded: <span className="text-white">{uploadedOn}</span>
            </span>

            <div className="flex gap-2 my-3 flex-wrap">
              {skillsOrTags.map((ele, index) => (
                <p className="bg-green-400 px-2 py-1 rounded-xl text-black">
                  {ele}
                </p>
              ))}
            </div>
          </div>
        </div>
      </div>
      <div className="fixed bottom-0 right-0 w-[70%] flex justify-betwen rounded-xl bg-gray-900">
        <div className="truncate text-gray-400 bg-gray-800 p-4 w-[80%] flex items-center rounded-xl justify-between">
          {link.substring(0, 110)}
          {icon === "copy" ? (
            <FaCopy
              fontSize={20}
              className="cursor-pointer"
              onClick={() => {
                setIcon("check");
                setTimeout(() => {
                  setIcon("copy");
                }, 5000);
                navigator.clipboard.writeText(link);
              }}
            />
          ) : (
            <FaCircleCheck
              fontSize={20}
              color="#22c55e"
              className="cursor-pointer"
            />
          )}
        </div>
        <a
          href={link}
          className="inline bg-green-700 p-5 rounded-xl w-[20%] text-xl hover:bg-green-500 drop-shadow-lg transition-all delay-100"
          target="__blank"
        >
          Apply Now
        </a>
      </div>
    </div>
  );
};

export default JobDesc;
