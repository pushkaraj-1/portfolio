"use client";

import { JobEntry, EducationEntry } from "@/lib/types";
import { ACHIEVEMENTS, CONFERENCES } from "@/lib/portfolio-data";

interface ExperienceOutreachProps {
  experience: JobEntry[];
  education: EducationEntry[];
  darkMode: boolean;
}

export function ExperienceOutreachSection({
  experience,
  education,
  darkMode,
}: ExperienceOutreachProps) {
  const formatDate = (dateStr: string) => {
    const [year, month] = dateStr.split("-");
    const months = [
      "Jan", "Feb", "Mar", "Apr", "May", "Jun",
      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ];
    const mName = months[parseInt(month, 10) - 1] || month;
    return `${mName} ${year}`;
  };

  return (
    <section id="experience" className="py-10 border-t border-dashed border-neutral-300 dark:border-neutral-800 space-y-12">
      {/* Experience Sub-section */}
      <div>
        <h2 className="text-2xl font-bold tracking-tight mb-6">experience & research roles</h2>
        <div className="space-y-6">
          {experience.map((job, idx) => (
            <div
              key={idx}
              className={`p-5 rounded-xl border transition-all ${
                darkMode
                  ? "bg-neutral-900/60 border-neutral-800"
                  : "bg-white border-neutral-200 shadow-xs"
              }`}
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 mb-2">
                <div>
                  <h3 className="text-lg font-bold">
                    {job.jobTitle}{" "}
                    <span
                      className={`font-semibold ${
                        darkMode ? "text-cyan-400" : "text-blue-600"
                      }`}
                    >
                      @ {job.company}
                    </span>
                  </h3>
                  <div className="text-xs opacity-75">{job.location}</div>
                </div>

                <span
                  className={`text-xs font-mono px-2.5 py-1 rounded border self-start sm:self-center shrink-0 ${
                    job.currentlyWorkHere
                      ? darkMode
                        ? "bg-cyan-950 border-cyan-800 text-cyan-300 font-semibold"
                        : "bg-blue-100 border-blue-300 text-blue-900 font-semibold"
                      : darkMode
                      ? "bg-neutral-800 border-neutral-700 text-neutral-400"
                      : "bg-neutral-100 border-neutral-200 text-neutral-600"
                  }`}
                >
                  {formatDate(job.startDate)} –{" "}
                  {job.currentlyWorkHere
                    ? "Present"
                    : job.endDate
                    ? formatDate(job.endDate)
                    : "Present"}
                </span>
              </div>

              {/* Description Bullet points */}
              <ul className="mt-3 space-y-2 text-sm opacity-90 list-disc list-inside leading-relaxed">
                {job.description
                  .split("\n")
                  .filter((line) => line.trim().length > 0)
                  .map((bullet, i) => {
                    const cleanText = bullet.replace(/^-\s*/, "");
                    return <li key={i}>{cleanText}</li>;
                  })}
              </ul>
            </div>
          ))}
        </div>
      </div>

      {/* Education & Outreach Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Education */}
        <div
          className={`p-5 rounded-xl border ${
            darkMode ? "bg-neutral-900/60 border-neutral-800" : "bg-white border-neutral-200"
          }`}
        >
          <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
            <span>🎓 education</span>
          </h3>
          <div className="space-y-4">
            {education.map((edu, idx) => (
              <div key={idx} className="space-y-1">
                <div className="font-semibold text-sm">{edu.school}</div>
                <div
                  className={`text-xs font-medium ${
                    darkMode ? "text-cyan-400" : "text-blue-600"
                  }`}
                >
                  {edu.degree} in {edu.fieldOfStudy}
                </div>
                <div className="flex items-center justify-between text-xs opacity-75">
                  <span>
                    {formatDate(edu.startDate)} – {formatDate(edu.endDate)}
                  </span>
                  <span className="font-mono font-semibold">GPA: {edu.gpa}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Hackathons & Honors */}
        <div
          className={`p-5 rounded-xl border ${
            darkMode ? "bg-neutral-900/60 border-neutral-800" : "bg-white border-neutral-200"
          }`}
        >
          <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
            <span>🏆 honors & hackathons</span>
          </h3>
          <ul className="space-y-2.5 text-sm opacity-90">
            {ACHIEVEMENTS.map((item, idx) => (
              <li key={idx} className="flex items-start space-x-2">
                <span className="text-xs">🥇</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Conferences & Service */}
      <div
        className={`p-5 rounded-xl border ${
          darkMode ? "bg-neutral-900/60 border-neutral-800" : "bg-white border-neutral-200"
        }`}
      >
        <h3 className="text-lg font-bold mb-3 flex items-center gap-2">
          <span>🌐 conferences & academic outreach</span>
        </h3>
        <div className="flex flex-wrap gap-2 text-xs font-mono">
          {CONFERENCES.map((conf, idx) => (
            <span
              key={idx}
              className={`px-3 py-1.5 rounded-lg border ${
                darkMode
                  ? "bg-neutral-800/80 border-neutral-700 text-neutral-200"
                  : "bg-neutral-100 border-neutral-200 text-neutral-800"
              }`}
            >
              • {conf}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}

