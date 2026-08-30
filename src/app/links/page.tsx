import type { Metadata } from "next";
import { Suspense } from "react";
import Link from "next/link";
import { LinksList } from "@/components/LinksList";

export const metadata: Metadata = {
  title: "Links — Pushkaraj Baradkar",
  description: "Everything I build, in one place.",
  // Bio traffic is throwaway; no reason to let it into search results.
  robots: { index: false, follow: true },
};

const HEADER_DELAY = 0;
const LIST_START = 200;
const STEP = 70;

export default function LinksPage() {
  return (
    <main className="mx-auto max-w-2xl px-6 py-16 md:py-24">
      <header className="fade-in" style={{ animationDelay: `${HEADER_DELAY}ms` }}>
        <h1 className="text-[17px] font-semibold leading-tight text-black">
          Pushkaraj Baradkar
        </h1>
        <p className="mt-1 text-[17px] leading-tight text-black">
          AI engineer at <span className="link-underline">Tabhi</span>
        </p>
        <p className="mt-1 text-[17px] leading-tight text-[#9b9b9b]">
          Everything I build, in one place.
        </p>
      </header>

      {/* useSearchParams needs a boundary so this page can still prerender. */}
      <Suspense fallback={<div className="mt-14 h-96" />}>
        <LinksList startDelay={LIST_START} step={STEP} />
      </Suspense>

      <footer
        className="fade-in mt-14 text-[17px] leading-tight text-[#9b9b9b]"
        style={{ animationDelay: `${LIST_START + 6 * STEP}ms` }}
      >
        <Link href="/" className="link-underline hover:text-black">
          pushkaraj.dev
        </Link>
      </footer>
    </main>
  );
}
