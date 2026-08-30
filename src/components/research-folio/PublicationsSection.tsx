"use client";

import { useState } from "react";
import { ResearchPaper } from "@/lib/types";

interface PublicationsSectionProps {
  papers: ResearchPaper[];
  darkMode: boolean;
}

export function PublicationsSection({
  papers,
  darkMode,
}: PublicationsSectionProps) {
  const [openBibtex, setOpenBibtex] = useState<string | null>(null);
  const [copiedSlug, setCopiedSlug] = useState<string | null>(null);
  const [openAbstract, setOpenAbstract] = useState<string | null>(null);

  const getBibtex = (p: ResearchPaper) => {
    return `@inproceedings{baradkar${p.year}${p.slug.replace(/[^a-zA-Z0-9]/g, "")},
  title={${p.title}},
  author={${p.authors.join(" and ")}},
  booktitle={${p.venue}},
  year={${p.year}},
  url={${p.link}}
}`;
  };

  const handleCopyBibtex = (p: ResearchPaper) => {
    navigator.clipboard.writeText(getBibtex(p));
    setCopiedSlug(p.slug);
    setTimeout(() => setCopiedSlug(null), 2000);
  };

  return (
    <section id="publications" className="py-10 border-t border-dashed border-neutral-300 dark:border-neutral-800">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold tracking-tight">publications & research</h2>
        <span className="text-xs font-mono opacity-60">peer-reviewed & proceedings</span>
      </div>

      <div className="space-y-6">
        {papers.map((paper) => {
          const isBibtexOpen = openBibtex === paper.slug;
          const isAbstractOpen = openAbstract === paper.slug;

          return (
            <div
              key={paper.slug}
              className={`p-5 rounded-xl border transition-all ${
                darkMode
                  ? "bg-neutral-900/60 border-neutral-800 hover:border-neutral-700"
                  : "bg-white border-neutral-200 hover:border-neutral-300 shadow-xs"
              }`}
            >
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-2">
                {/* Title & Badge */}
                <h3 className="text-lg font-semibold leading-snug">
                  <a
                    href={paper.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={`hover:underline ${
                      darkMode ? "text-cyan-300" : "text-blue-700"
                    }`}
                  >
                    {paper.title}
                  </a>
                </h3>

                {/* Venue Tag */}
                <span
                  className={`shrink-0 self-start text-xs font-mono font-semibold px-2.5 py-1 rounded border ${
                    darkMode
                      ? "bg-neutral-800 border-neutral-700 text-cyan-400"
                      : "bg-blue-50 border-blue-200 text-blue-800"
                  }`}
                >
                  [{paper.venue} '{paper.year.toString().slice(-2)}]
                </span>
              </div>

              {/* Authors */}
              <div className="mt-2 text-sm opacity-90">
                {paper.authors.map((author, i) => (
                  <span key={i}>
                    {author.includes("Pushkaraj") ? (
                      <strong className="font-semibold underline underline-offset-2">
                        {author}
                      </strong>
                    ) : (
                      author
                    )}
                    {i < paper.authors.length - 1 ? ", " : ""}
                  </span>
                ))}
              </div>

              {/* Venue details */}
              <div className="mt-1 text-xs italic opacity-70">
                Published in {paper.venue}, {paper.year}
              </div>

              {/* Abstract preview or summary */}
              <p className="mt-3 text-sm leading-relaxed opacity-90">
                {paper.description}
              </p>

              {/* Action buttons */}
              <div className="mt-4 flex flex-wrap items-center gap-2 text-xs font-medium font-mono">
                {paper.link && (
                  <a
                    href={paper.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={`px-2.5 py-1 rounded border transition-colors ${
                      darkMode
                        ? "bg-neutral-800 border-neutral-700 text-neutral-200 hover:bg-neutral-700"
                        : "bg-neutral-100 border-neutral-300 text-neutral-800 hover:bg-neutral-200"
                    }`}
                  >
                    IEEE Xplore / Paper ↗
                  </a>
                )}

                {paper.abstract && (
                  <button
                    onClick={() =>
                      setOpenAbstract(isAbstractOpen ? null : paper.slug)
                    }
                    className={`px-2.5 py-1 rounded border transition-colors cursor-pointer ${
                      isAbstractOpen
                        ? darkMode
                          ? "bg-cyan-950 border-cyan-800 text-cyan-300"
                          : "bg-blue-100 border-blue-300 text-blue-900"
                        : darkMode
                        ? "bg-neutral-800 border-neutral-700 text-neutral-200 hover:bg-neutral-700"
                        : "bg-neutral-100 border-neutral-300 text-neutral-800 hover:bg-neutral-200"
                    }`}
                  >
                    {isAbstractOpen ? "Hide Abstract" : "Abstract"}
                  </button>
                )}

                <button
                  onClick={() =>
                    setOpenBibtex(isBibtexOpen ? null : paper.slug)
                  }
                  className={`px-2.5 py-1 rounded border transition-colors cursor-pointer ${
                    isBibtexOpen
                      ? darkMode
                        ? "bg-cyan-950 border-cyan-800 text-cyan-300"
                        : "bg-blue-100 border-blue-300 text-blue-900"
                      : darkMode
                      ? "bg-neutral-800 border-neutral-700 text-neutral-200 hover:bg-neutral-700"
                      : "bg-neutral-100 border-neutral-300 text-neutral-800 hover:bg-neutral-200"
                  }`}
                >
                  BibTeX
                </button>
              </div>

              {/* Collapsible Abstract Box */}
              {isAbstractOpen && (
                <div
                  className={`mt-4 p-4 rounded-lg text-xs leading-relaxed border ${
                    darkMode
                      ? "bg-neutral-950 border-neutral-800 text-neutral-300"
                      : "bg-neutral-50 border-neutral-200 text-neutral-800"
                  }`}
                >
                  <strong className="block font-semibold mb-1">Abstract:</strong>
                  {paper.abstract}
                </div>
              )}

              {/* Collapsible BibTeX Box */}
              {isBibtexOpen && (
                <div
                  className={`mt-4 p-4 rounded-lg text-xs font-mono border relative ${
                    darkMode
                      ? "bg-neutral-950 border-neutral-800 text-cyan-300"
                      : "bg-neutral-900 border-neutral-800 text-cyan-400"
                  }`}
                >
                  <button
                    onClick={() => handleCopyBibtex(paper)}
                    className="absolute top-2 right-2 px-2 py-1 bg-neutral-800 hover:bg-neutral-700 text-white rounded text-[11px]"
                  >
                    {copiedSlug === paper.slug ? "Copied!" : "Copy"}
                  </button>
                  <pre className="overflow-x-auto whitespace-pre-wrap">
                    {getBibtex(paper)}
                  </pre>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
