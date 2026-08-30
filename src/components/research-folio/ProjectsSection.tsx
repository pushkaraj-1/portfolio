"use client";

import { Project } from "@/lib/types";
import { useState } from "react";
import Image from "next/image";

interface ProjectsSectionProps {
  projects: Project[];
  darkMode: boolean;
}

export function ProjectsSection({ projects, darkMode }: ProjectsSectionProps) {
  const [selectedCategory, setSelectedCategory] = useState<string>("all");

  const categories = ["all", "AI & ML", "Systems & Vision", "Web3 & Cloud"];

  const getCategory = (p: Project): string => {
    const tech = p.tech.join(" ").toLowerCase();
    if (tech.includes("solana") || tech.includes("anchor") || tech.includes("blockchain")) {
      return "Web3 & Cloud";
    }
    if (tech.includes("vision") || tech.includes("slam") || tech.includes("three.js") || tech.includes("godot")) {
      return "Systems & Vision";
    }
    return "AI & ML";
  };

  const filteredProjects = selectedCategory === "all"
    ? projects
    : projects.filter((p) => getCategory(p) === selectedCategory);

  return (
    <section id="projects" className="py-10 border-t border-dashed border-neutral-300 dark:border-neutral-800">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <h2 className="text-2xl font-bold tracking-tight">selected projects</h2>

        {/* Category Filter Pills */}
        <div className="flex flex-wrap items-center gap-1.5 text-xs font-mono">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1 rounded-full border cursor-pointer transition-colors capitalize ${
                selectedCategory === cat
                  ? darkMode
                    ? "bg-cyan-950 border-cyan-700 text-cyan-300 font-semibold"
                    : "bg-blue-100 border-blue-300 text-blue-900 font-semibold"
                  : darkMode
                  ? "bg-neutral-900 border-neutral-800 text-neutral-400 hover:text-neutral-200"
                  : "bg-neutral-100 border-neutral-200 text-neutral-600 hover:text-black"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {filteredProjects.map((project) => (
          <div
            key={project.slug}
            className={`group rounded-xl border p-5 flex flex-col justify-between transition-all duration-200 ${
              darkMode
                ? "bg-neutral-900/60 border-neutral-800 hover:border-neutral-700"
                : "bg-white border-neutral-200 hover:border-neutral-300 hover:shadow-md"
            }`}
          >
            <div>
              {/* Header: Title & Year */}
              <div className="flex items-start justify-between gap-2 mb-2">
                <h3
                  className={`text-lg font-bold group-hover:underline ${
                    darkMode ? "text-cyan-300" : "text-blue-800"
                  }`}
                >
                  <a
                    href={project.live || project.github}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {project.title}
                  </a>
                </h3>
                <span
                  className={`text-xs font-mono px-2 py-0.5 rounded border shrink-0 ${
                    darkMode
                      ? "bg-neutral-800 border-neutral-700 text-neutral-400"
                      : "bg-neutral-100 border-neutral-200 text-neutral-600"
                  }`}
                >
                  {project.year}
                </span>
              </div>

              {/* Thumbnail Image if present */}
              {project.screenshot && (
                <div className="my-3 overflow-hidden rounded-lg border border-neutral-200 dark:border-neutral-800 relative h-36 w-full bg-neutral-100 dark:bg-neutral-950">
                  <Image
                    src={project.screenshot}
                    alt={project.title}
                    fill
                    className="object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                </div>
              )}

              {/* Description */}
              <p className="text-sm leading-relaxed opacity-90 mb-4 line-clamp-4">
                {project.description}
              </p>
            </div>

            {/* Bottom: Tech Stack & Links */}
            <div>
              <div className="flex flex-wrap gap-1.5 mb-4">
                {project.tech.map((t, idx) => (
                  <span
                    key={idx}
                    className={`text-[11px] font-mono px-2 py-0.5 rounded ${
                      darkMode
                        ? "bg-neutral-800/80 text-neutral-300 border border-neutral-700/60"
                        : "bg-neutral-100 text-neutral-700 border border-neutral-200"
                    }`}
                  >
                    {t}
                  </span>
                ))}
              </div>

              <div className="flex items-center space-x-3 text-xs font-medium font-mono pt-2 border-t border-dashed border-neutral-200 dark:border-neutral-800">
                {project.github && (
                  <a
                    href={project.github}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={`hover:underline flex items-center gap-1 ${
                      darkMode ? "text-cyan-400" : "text-blue-600"
                    }`}
                  >
                    <span>Code</span> ↗
                  </a>
                )}
                {project.live && (
                  <a
                    href={project.live}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={`hover:underline flex items-center gap-1 ${
                      darkMode ? "text-cyan-400" : "text-blue-600"
                    }`}
                  >
                    <span>Live Demo</span> ↗
                  </a>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

