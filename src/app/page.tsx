import { getProjects, getResearchPapers } from "@/lib/data";
import { EXPERIENCE, EDUCATION } from "@/lib/portfolio-data";
import { ResearchFolioView } from "@/components/research-folio/ResearchFolioView";

export default function Home() {
  const projects = getProjects();
  const research = getResearchPapers();

  return (
    <ResearchFolioView
      projects={projects}
      papers={research}
      experience={EXPERIENCE}
      education={EDUCATION}
    />
  );
}
