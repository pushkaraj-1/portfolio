"use client";

import { LINKS, RESEARCH_STATEMENT } from "@/lib/portfolio-data";

interface HeroAboutProps {
  darkMode: boolean;
}

export function HeroAbout({ darkMode }: HeroAboutProps) {
  return (
    <section id="about" className="py-12 md:py-16">
      <div className="flex flex-col-reverse md:flex-row gap-10 items-start">
        {/* Left Column: Bio & Statement */}
        <div className="flex-1 space-y-6">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold tracking-tight">
              {RESEARCH_STATEMENT.title}
            </h1>
            <p
              className={`text-lg mt-1 font-medium ${
                darkMode ? "text-cyan-400" : "text-blue-700"
              }`}
            >
              {RESEARCH_STATEMENT.role} @{" "}
              <a
                href="https://www.usc.edu/"
                target="_blank"
                rel="noopener noreferrer"
                className="underline hover:opacity-80"
              >
                USC Viterbi
              </a>
            </p>
            <p
              className={`text-sm mt-1 ${
                darkMode ? "text-neutral-400" : "text-neutral-600"
              }`}
            >
              📍 {RESEARCH_STATEMENT.location}
            </p>
          </div>

          {/* Job Market / Recruitment Status Banner */}
          <div
            className={`p-4 rounded-xl border text-sm flex items-start space-x-3 transition-colors ${
              darkMode
                ? "bg-cyan-950/40 border-cyan-800/60 text-cyan-200"
                : "bg-blue-50 border-blue-200 text-blue-900"
            }`}
          >
            <span className="text-lg">📢</span>
            <div>
              <span className="font-semibold">Job Market Status:</span>{" "}
              {RESEARCH_STATEMENT.status} If your research team or organization aligns with my interests, feel free to get in touch!
            </div>
          </div>

          {/* Bio paragraphs */}
          <div className="space-y-4 text-base leading-relaxed text-justify">
            {RESEARCH_STATEMENT.bio.map((paragraph, idx) => (
              <p key={idx}>{paragraph}</p>
            ))}
          </div>

          {/* Research Focus Topics */}
          <div className="space-y-4 pt-2">
            {RESEARCH_STATEMENT.topics.map((topic, idx) => (
              <div
                key={idx}
                className={`p-4 rounded-lg border transition-all ${
                  darkMode
                    ? "bg-neutral-900/60 border-neutral-800 hover:border-neutral-700"
                    : "bg-neutral-50/80 border-neutral-200 hover:border-neutral-300"
                }`}
              >
                <h3
                  className={`font-semibold text-base mb-1 ${
                    darkMode ? "text-cyan-300" : "text-blue-800"
                  }`}
                >
                  📌 {topic.title}
                </h3>
                <p className="text-sm opacity-90 leading-normal">
                  {topic.description}
                </p>
              </div>
            ))}
          </div>

          {/* Contact / Social links */}
          <div className="flex flex-wrap items-center gap-4 pt-2 text-sm font-medium">
            <a
              href={`mailto:${LINKS.email}`}
              className={`inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-md border transition-colors ${
                darkMode
                  ? "border-neutral-700 bg-neutral-800 hover:bg-neutral-700 text-neutral-200"
                  : "border-neutral-300 bg-neutral-100 hover:bg-neutral-200 text-neutral-800"
              }`}
            >
              <span>📧</span>
              <span>Email</span>
            </a>
            <a
              href={LINKS.github}
              target="_blank"
              rel="noopener noreferrer"
              className={`inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-md border transition-colors ${
                darkMode
                  ? "border-neutral-700 bg-neutral-800 hover:bg-neutral-700 text-neutral-200"
                  : "border-neutral-300 bg-neutral-100 hover:bg-neutral-200 text-neutral-800"
              }`}
            >
              <span>💻</span>
              <span>GitHub</span>
            </a>
            <a
              href={LINKS.linkedin}
              target="_blank"
              rel="noopener noreferrer"
              className={`inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-md border transition-colors ${
                darkMode
                  ? "border-neutral-700 bg-neutral-800 hover:bg-neutral-700 text-neutral-200"
                  : "border-neutral-300 bg-neutral-100 hover:bg-neutral-200 text-neutral-800"
              }`}
            >
              <span>💼</span>
              <span>LinkedIn</span>
            </a>
            <a
              href={LINKS.resume}
              download
              className={`inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-md border transition-colors ${
                darkMode
                  ? "border-cyan-800 bg-cyan-950/60 text-cyan-300 hover:bg-cyan-900/60"
                  : "border-blue-300 bg-blue-50 text-blue-700 hover:bg-blue-100"
              }`}
            >
              <span>📄</span>
              <span>CV / Resume (PDF)</span>
            </a>
          </div>
        </div>

        {/* Right Column: Profile Avatar / Card */}
        <div className="w-full md:w-64 flex flex-col items-center md:items-end shrink-0">
          <div
            className={`w-48 h-48 md:w-56 md:h-56 rounded-2xl overflow-hidden border-2 shadow-lg flex flex-col items-center justify-center p-4 text-center transition-colors ${
              darkMode
                ? "bg-gradient-to-br from-neutral-800 to-neutral-900 border-neutral-700"
                : "bg-gradient-to-br from-neutral-100 to-white border-neutral-200"
            }`}
          >
            <div className="w-20 h-20 rounded-full bg-blue-600 text-white flex items-center justify-center text-3xl font-bold mb-3 shadow-md">
              PB
            </div>
            <div className="font-semibold text-base">Pushkaraj Baradkar</div>
            <div className="text-xs opacity-75 mt-1">MS CS @ USC Viterbi</div>
            <div className="text-[11px] opacity-60 mt-0.5">Real-Time AI & SLAM</div>
          </div>
          <div className="mt-3 text-xs text-center md:text-right opacity-60 italic max-w-[220px]">
            USC Viterbi · Tabhi AI · Real-Time Vision & RecSys
          </div>
        </div>
      </div>
    </section>
  );
}

