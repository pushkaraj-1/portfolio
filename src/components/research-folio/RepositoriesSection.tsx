"use client";

import { LINKS } from "@/lib/portfolio-data";

interface RepositoryItem {
  name: string;
  description: string;
  language: string;
  languageColor: string;
  stars?: number;
  url: string;
  topics: string[];
}

interface RepositoriesSectionProps {
  darkMode: boolean;
}

export function RepositoriesSection({ darkMode }: RepositoriesSectionProps) {
  const repos: RepositoryItem[] = [
    {
      name: "pushks18/agentpay",
      description: "Multi-agent economy where AI agents autonomously discover, hire, and pay other agents using on-chain payments & verifiable reputation.",
      language: "Rust",
      languageColor: "bg-amber-600",
      stars: 18,
      url: "https://github.com/pushks18",
      topics: ["solana", "avalanche", "anchor", "langchain", "multi-agent"],
    },
    {
      name: "pushks18/realtime-vision-slam",
      description: "Real-time visual odometry and monocular depth estimation pipeline with GTSAM factor graph optimization & topological semantic memory.",
      language: "C++ / Python",
      languageColor: "bg-blue-600",
      stars: 24,
      url: "https://github.com/pushks18",
      topics: ["computer-vision", "slam", "gtsam", "visual-odometry", "pytorch"],
    },
    {
      name: "pushks18/personalized-discovery-feed",
      description: "Hybrid vector search + BM25 retrieval pipeline with slot-based re-ranking, recency-decayed user preference modeling & sub-500ms caching.",
      language: "Python",
      languageColor: "bg-emerald-600",
      stars: 15,
      url: "https://github.com/pushks18",
      topics: ["elasticsearch", "recsys", "vector-search", "fastapi", "redis"],
    },
    {
      name: "pushks18/godot-mcp",
      description: "Model Context Protocol (MCP) server integration for Godot 4 Engine enabling AI agents to edit scenes, inspect nodes, and generate GDScript.",
      language: "TypeScript",
      languageColor: "bg-sky-500",
      stars: 12,
      url: "https://github.com/pushks18",
      topics: ["godot-engine", "mcp", "ai-tools", "gdscript", "nextjs"],
    },
    {
      name: "pushks18/cold-reach",
      description: "AI-powered cold email personalization and outbound discovery tool generating hyper-customized outreach using LLM pipelines.",
      language: "TypeScript",
      languageColor: "bg-sky-500",
      stars: 9,
      url: "https://github.com/pushks18",
      topics: ["nextjs", "llms", "resend", "tailwind"],
    },
    {
      name: "pushks18/blockchain-music-nft",
      description: "Decentralized music streaming platform using NFTs for rights management and automated royalty distribution — presented at IEEE ICSCSS 2023.",
      language: "Solidity / JS",
      languageColor: "bg-purple-600",
      stars: 31,
      url: "https://github.com/pushks18",
      topics: ["blockchain", "nfts", "ethereum", "web3", "ieee-publication"],
    },
  ];

  return (
    <section id="repositories" className="py-10 border-t border-dashed border-neutral-300 dark:border-neutral-800">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold tracking-tight flex items-center gap-2">
          <span>featured repositories</span>
          <span
            className={`text-xs font-mono px-2 py-0.5 rounded-full ${
              darkMode
                ? "bg-neutral-800 text-cyan-400 border border-neutral-700"
                : "bg-neutral-100 text-blue-700 border border-neutral-200"
            }`}
          >
            GitHub
          </span>
        </h2>
        <a
          href={LINKS.github}
          target="_blank"
          rel="noopener noreferrer"
          className={`text-xs font-mono font-medium underline underline-offset-4 ${
            darkMode ? "text-cyan-400 hover:text-cyan-300" : "text-blue-600 hover:text-blue-800"
          }`}
        >
          view @pushks18 ↗
        </a>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {repos.map((repo, idx) => (
          <div
            key={idx}
            className={`p-5 rounded-xl border flex flex-col justify-between transition-all duration-200 ${
              darkMode
                ? "bg-neutral-900/60 border-neutral-800 hover:border-neutral-700"
                : "bg-white border-neutral-200 hover:border-neutral-300 shadow-xs"
            }`}
          >
            <div>
              {/* Header: Repo Name & Stars */}
              <div className="flex items-start justify-between gap-2 mb-2">
                <h3 className="font-semibold text-base font-mono leading-snug">
                  <a
                    href={repo.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={`hover:underline flex items-center gap-1.5 ${
                      darkMode ? "text-cyan-300" : "text-blue-700"
                    }`}
                  >
                    <span>📦</span>
                    <span>{repo.name}</span>
                  </a>
                </h3>

                {repo.stars !== undefined && (
                  <span
                    className={`shrink-0 text-xs font-mono px-2 py-0.5 rounded border flex items-center gap-1 ${
                      darkMode
                        ? "bg-neutral-800 border-neutral-700 text-neutral-300"
                        : "bg-neutral-100 border-neutral-200 text-neutral-700"
                    }`}
                  >
                    <span>⭐</span>
                    <span>{repo.stars}</span>
                  </span>
                )}
              </div>

              {/* Description */}
              <p className="text-sm leading-relaxed opacity-90 mb-4">
                {repo.description}
              </p>
            </div>

            {/* Language & Topic Tags */}
            <div>
              <div className="flex flex-wrap gap-1.5 mb-3">
                {repo.topics.map((topic, i) => (
                  <span
                    key={i}
                    className={`text-[10px] font-mono px-2 py-0.5 rounded-full ${
                      darkMode
                        ? "bg-neutral-800/80 text-neutral-400 border border-neutral-700/60"
                        : "bg-neutral-100 text-neutral-600 border border-neutral-200"
                    }`}
                  >
                    #{topic}
                  </span>
                ))}
              </div>

              <div className="flex items-center space-x-2 text-xs font-mono pt-2 border-t border-dashed border-neutral-200 dark:border-neutral-800">
                <span className={`w-2.5 h-2.5 rounded-full ${repo.languageColor}`}></span>
                <span className="opacity-80">{repo.language}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
