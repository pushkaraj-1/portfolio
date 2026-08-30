"use client";

import { NEWS } from "@/lib/portfolio-data";
import { useState } from "react";

interface NewsSectionProps {
  darkMode: boolean;
}

export function NewsSection({ darkMode }: NewsSectionProps) {
  const [showAll, setShowAll] = useState(false);
  const displayedNews = showAll ? NEWS : NEWS.slice(0, 5);

  // Helper to convert markdown bold **text** to JSX
  const renderFormattedText = (text: string) => {
    const parts = text.split(/(\*\*.*?\*\*)/g);
    return parts.map((part, i) => {
      if (part.startsWith("**") && part.endsWith("**")) {
        return (
          <strong key={i} className="font-semibold">
            {part.slice(2, -2)}
          </strong>
        );
      }
      return part;
    });
  };

  return (
    <section id="news" className="py-10 border-t border-dashed border-neutral-300 dark:border-neutral-800">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold tracking-tight flex items-center gap-2">
          <span>news</span>
          <span
            className={`text-xs font-mono px-2 py-0.5 rounded-full ${
              darkMode
                ? "bg-neutral-800 text-cyan-400 border border-neutral-700"
                : "bg-neutral-100 text-blue-700 border border-neutral-200"
            }`}
          >
            {NEWS.length} updates
          </span>
        </h2>
      </div>

      <div className="space-y-4">
        {displayedNews.map((item) => (
          <div
            key={item.id}
            className={`flex flex-col sm:flex-row sm:items-start gap-2 sm:gap-6 p-3.5 rounded-lg transition-colors ${
              item.highlight
                ? darkMode
                  ? "bg-neutral-900/80 border border-neutral-800"
                  : "bg-neutral-50 border border-neutral-200"
                : ""
            }`}
          >
            {/* Date Tag */}
            <div className="shrink-0 sm:w-28">
              <span
                className={`inline-block text-xs font-semibold font-mono px-2.5 py-1 rounded ${
                  item.highlight
                    ? darkMode
                      ? "bg-cyan-950 text-cyan-300 border border-cyan-800"
                      : "bg-blue-100 text-blue-800 border border-blue-200"
                    : darkMode
                    ? "bg-neutral-800 text-neutral-300"
                    : "bg-neutral-200 text-neutral-700"
                }`}
              >
                {item.date}
              </span>
            </div>

            {/* Content */}
            <div className="flex-1 text-sm leading-relaxed">
              <span>{renderFormattedText(item.content)}</span>
              {item.link && (
                <a
                  href={item.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`ml-2 text-xs font-medium underline underline-offset-2 ${
                    darkMode ? "text-cyan-400 hover:text-cyan-300" : "text-blue-600 hover:text-blue-800"
                  }`}
                >
                  [{item.linkText || "link"} ↗]
                </a>
              )}
            </div>
          </div>
        ))}
      </div>

      {NEWS.length > 5 && (
        <div className="mt-4 text-center sm:text-left">
          <button
            onClick={() => setShowAll(!showAll)}
            className={`text-xs font-mono font-medium underline underline-offset-4 cursor-pointer transition-colors ${
              darkMode ? "text-neutral-400 hover:text-cyan-400" : "text-neutral-600 hover:text-blue-600"
            }`}
          >
            {showAll ? "🕰️ show less" : "🕰️ all news..."}
          </button>
        </div>
      )}
    </section>
  );
}

