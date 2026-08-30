"use client";

import { useSearchParams } from "next/navigation";
import { track } from "@vercel/analytics";
import { BIO_LINKS, normalizeSource, withUtm } from "@/lib/links-data";

interface Props {
  startDelay: number;
  step: number;
}

export function LinksList({ startDelay, step }: Props) {
  // Read once per render; during prerender this is empty and we fall back to
  // the default source, then hydration fills in the real ?s= value.
  const source = normalizeSource(useSearchParams().get("s"));

  return (
    <section className="mt-14">
      {BIO_LINKS.map((link, i) => {
        const href = withUtm(link.href, source);
        const isBlank = link.external;

        return (
          <a
            key={link.slug}
            href={href}
            {...(isBlank ? { target: "_blank", rel: "noopener noreferrer" } : {})}
            // Fires before navigation; Vercel's beacon uses sendBeacon so it
            // survives the page unloading.
            onClick={() => track("link_click", { link: link.slug, source })}
            // -mx-3 px-3 keeps the text flush with the header while giving the
            // row a thumb-sized tap area — this page is almost entirely mobile.
            className="fade-in group -mx-3 flex items-baseline gap-3 rounded-md px-3 py-3 transition-colors duration-200 hover:bg-black/[0.03] active:bg-black/[0.06]"
            style={{ animationDelay: `${startDelay + i * step}ms` }}
          >
            <span className="min-w-0 flex-1">
              <span className="block text-[17px] font-medium leading-tight text-black">
                {link.title}
              </span>
              <span className="mt-1 block text-[17px] leading-tight text-[#9b9b9b]">
                {link.meta}
              </span>
            </span>
            <span
              aria-hidden
              className="shrink-0 text-[17px] leading-tight text-[#9b9b9b] transition-transform duration-200 group-hover:translate-x-0.5 group-hover:text-black"
            >
              ↗
            </span>
          </a>
        );
      })}
    </section>
  );
}
