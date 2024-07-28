import React from "react";

function capitalizeFirstLetter(string) {
  return string?.charAt(0).toUpperCase() + string?.slice(1);
}

const jobPortalLogo = {
  internshala:
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQP1VDymcuhCr0iAYAeTMjWf765VNqamh1u_A&s",
  unstop:
    "https://d8it4huxumps7.cloudfront.net/uploads/images/unstop/branding-guidelines/icon/unstop-icon-800x800.png",
  linkedin:
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/LinkedIn_logo_initials.png/600px-LinkedIn_logo_initials.png",
  cuvette:
    "https://yt3.googleusercontent.com/-odqfe8SzjHhj-r2bwtOTEP2SEd_28svcyvA6IlDTTDceB2K5U7V5ufuJwc4ZfgM6XjJ7bsBww=s900-c-k-c0x00ffffff-no-rj",
  "naukri.com":
    "https://play-lh.googleusercontent.com/76gEFhQto5xMHr2Qf8nWLvm1s0O60clhkwHvxQDSeI3hthf7Zs05JJQeyg5H347DGQ",
};

const JobCard = ({ isSelected, onClick, data }) => {
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
    <div
      className={`h-[10.5rem] relative bg-gray-800 my-4 rounded-xl overflow-hidden px-3 py-3 cursor-pointer flex flex-col justify-between ${
        isSelected && "border border-green-500 text-green-500"
      }`}
      onClick={onClick}
    >
      <div className="flex w-full gap-3">
        <div className="w-1/5 h-[5rem]">
          <img
            src={logo}
            onError={(e) => {
              e.target.src =
                "https://media.istockphoto.com/id/1055079680/vector/black-linear-photo-camera-like-no-image-available.jpg?s=612x612&w=0&k=20&c=P1DebpeMIAtXj_ZbVsKVvg-duuL0v9DlrOZUvPG6UJk=";
            }}
            alt={company}
            // height={40}
            width={200}
            className="rounded-xl"
          />
        </div>
        <div className="w-3/4 flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <h1 className="text-lg font-bold truncate">{position}</h1>
            <span className="text-sm whitespace-nowrap">{uploadedOn}</span>
          </div>
          <p
            className="text-left text-sm leading-4 text-gray-500"
            dangerouslySetInnerHTML={{
              __html: jobDescription.substring(0, 120) + "...",
            }}
          ></p>
        </div>
      </div>
      <div className="flex gap-2 justify-between leading-4 text-sm items-end">
        <div className="flex flex-col gap-2">
          {(stipend || opportunityType) && (
            <p className="flex items-center gap-2 truncate">
              {stipend && (
                <span className="text-sm truncate leading-5 border-r pr-2 border-gray-500">
                  {stipend}
                </span>
              )}
              {opportunityType && (
                <span className="truncate text-[14px] ">
                  {capitalizeFirstLetter(opportunityType)}
                </span>
              )}
            </p>
          )}
          <div className="flex gap-3">
            {deadline && (
              <span>
                <span className="text-green-500 font-bold">Deadline:</span>{" "}
                {deadline?.includes("₹") ? "Not Found" : deadline}
              </span>
            )}
            <span>
              <span className="text-green-500 font-bold">Applied:</span>{" "}
              {applications}
            </span>
          </div>
        </div>
        <a href={link} target="__blank">
          <img
            src={jobPortalLogo[`${jobPortal}`]}
            alt="Portal Logo"
            width={50}
            className="rounded-xl absolute bottom-3 right-3"
          />
        </a>
      </div>
    </div>
  );
};

export default JobCard;
