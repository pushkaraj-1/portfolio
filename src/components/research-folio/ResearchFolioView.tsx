"use client";

import { useState } from "react";
import { Project, ResearchPaper, JobEntry, EducationEntry } from "@/lib/types";
import { Navbar } from "./Navbar";
import { HeroAbout } from "./HeroAbout";
import { NewsSection } from "./NewsSection";
import { PublicationsSection } from "./PublicationsSection";
import { ProjectsSection } from "./ProjectsSection";
import { RepositoriesSection } from "./RepositoriesSection";
import { ExperienceOutreachSection } from "./ExperienceOutreachSection";
import { Footer } from "./Footer";

interface ResearchFolioViewProps {
  projects: Project[];
  papers: ResearchPaper[];
  experience: JobEntry[];
  education: EducationEntry[];
}

export function ResearchFolioView({
  projects,
  papers,
  experience,
  education,
}: ResearchFolioViewProps) {
  const [activeSection, setActiveSection] = useState<string>("about");
  const [darkMode, setDarkMode] = useState<boolean>(true);

  return (
    <div
      className={`min-h-screen transition-colors duration-300 ${
        darkMode ? "bg-[#121212] text-neutral-100" : "bg-[#fcfcfc] text-neutral-900"
      }`}
    >
      <Navbar
        activeSection={activeSection}
        setActiveSection={setActiveSection}
        darkMode={darkMode}
        setDarkMode={setDarkMode}
      />

      <main className="max-w-5xl mx-auto px-6 space-y-4">
        <HeroAbout darkMode={darkMode} />
        <NewsSection darkMode={darkMode} />
        <PublicationsSection papers={papers} darkMode={darkMode} />
        <ProjectsSection projects={projects} darkMode={darkMode} />
        <RepositoriesSection darkMode={darkMode} />
        <ExperienceOutreachSection
          experience={experience}
          education={education}
          darkMode={darkMode}
        />
      </main>

      <Footer darkMode={darkMode} />
    </div>
  );
}
