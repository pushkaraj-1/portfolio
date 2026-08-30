export interface ProfileData {
  nameData: {
    firstName: string;
    lastName: string;
    preferredFirstName: string;
    preferredLastName: string;
  };
  addressData: {
    city: string;
    state: string;
    country: string;
  };
  contactData: {
    phoneNumber: string;
    email: string;
  };
  jobData: JobEntry[];
  educationData: EducationEntry[];
  skillsData: string[];
  websiteData: {
    websites: string[];
    github: string;
    linkedin: string;
    personal: string;
  };
  resumeData: {
    resumeBase64: string;
    fileName: string;
  };
}

export interface JobEntry {
  jobTitle: string;
  company: string;
  location: string;
  startDate: string;
  currentlyWorkHere: boolean;
  endDate?: string;
  description: string;
}

export interface EducationEntry {
  school: string;
  degree: string;
  fieldOfStudy: string;
  startDate: string;
  currentlyAttending: boolean;
  endDate: string;
  gpa: string;
}

export interface Project {
  slug: string;
  title: string;
  description: string;
  status: "DEPLOYED" | "ACTIVE" | "ARCHIVED";
  year: number;
  tech: string[];
  github: string;
  live: string;
  screenshot: string;
  longDescription: string;
}

export interface ResearchPaper {
  slug: string;
  title: string;
  venue: string;
  year: number;
  description: string;
  link: string;
  abstract: string;
  authors: string[];
}

export interface BlogPost {
  slug: string;
  title: string;
  date: string;
  tags: string[];
  excerpt: string;
  content: string;
}

export interface NewsItem {
  id: string;
  date: string; // e.g. "May 2026", "Feb 2026"
  content: string; // Markdown / link supported text
  link?: string;
  linkText?: string;
  highlight?: boolean;
}

export interface SkillCategory {
  name: string;
  skills: string[];
}

