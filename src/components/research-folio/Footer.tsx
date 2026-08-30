"use client";

import { LINKS } from "@/lib/portfolio-data";

interface FooterProps {
  darkMode: boolean;
}

export function Footer({ darkMode }: FooterProps) {
  const currentYear = new Date().getFullYear();

  return (
    <footer
      className={`py-8 border-t transition-colors text-xs opacity-80 ${
        darkMode ? "border-neutral-800 text-neutral-400" : "border-neutral-200 text-neutral-600"
      }`}
    >
      <div className="max-w-5xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left">
        <div>
          © Copyright {currentYear} <strong>Pushkaraj Baradkar</strong>. Powered by{" "}
          <a
            href="https://nextjs.org"
            target="_blank"
            rel="noopener noreferrer"
            className="underline hover:opacity-80"
          >
            Next.js
          </a>{" "}
          with academic{" "}
          <a
            href="https://github.com/alshedivat/al-folio"
            target="_blank"
            rel="noopener noreferrer"
            className="underline hover:opacity-80"
          >
            al-folio
          </a>{" "}
          theme layout. Hosted on Vercel.
        </div>

        <div className="flex items-center space-x-4">
          <a href={`mailto:${LINKS.email}`} className="hover:underline">
            email
          </a>
          <a href={LINKS.github} target="_blank" rel="noopener noreferrer" className="hover:underline">
            github
          </a>
          <a href={LINKS.linkedin} target="_blank" rel="noopener noreferrer" className="hover:underline">
            linkedin
          </a>
          <a href="/resume.pdf" download className="hover:underline">
            resume
          </a>
        </div>
      </div>
    </footer>
  );
}
