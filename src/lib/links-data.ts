/**
 * Data for /links — the link-in-bio page.
 *
 * Order matters: this is the tap order on mobile, where nearly all the traffic
 * lands. Put the thing you currently want clicked at the top.
 */

export type BioLink = {
  /** Stable id used as the analytics event label. Don't rename casually — it breaks historical comparisons. */
  slug: string;
  title: string;
  /** One line under the title. Say what they get, not what it is. */
  meta: string;
  href: string;
  /** Opens in a new tab. Internal routes should leave this false. */
  external?: boolean;
};

export const BIO_LINKS: BioLink[] = [
  {
    slug: "portfolio",
    title: "Portfolio",
    meta: "Projects, research, and experience",
    href: "/",
  },
  {
    slug: "github",
    title: "GitHub",
    meta: "Source for everything I build on camera",
    href: "https://github.com/pushks18",
    external: true,
  },
  {
    slug: "linkedin",
    title: "LinkedIn",
    meta: "Long-form posts and hiring conversations",
    href: "https://www.linkedin.com/in/pushks18/",
    external: true,
  },
  {
    slug: "resume",
    title: "Résumé",
    meta: "One page, PDF",
    href: "/resume.pdf",
  },
  {
    slug: "email",
    title: "Email me",
    meta: "pushkarajbaradkar1@gmail.com",
    href: "mailto:pushkarajbaradkar1@gmail.com",
  },
  // TODO: add once the channel is live — this is the row the AI-engineer series
  // should point at, so move it to the top when it ships.
  // {
  //   slug: "youtube",
  //   title: "YouTube",
  //   meta: "The AI engineer series — one system per episode",
  //   href: "https://youtube.com/@yourhandle",
  //   external: true,
  // },
];

/** Where the visitor came from, via ?s= on the /links URL. */
export const DEFAULT_SOURCE = "instagram";

const SOURCE_ALIASES: Record<string, string> = {
  ig: "instagram",
  yt: "youtube",
  li: "linkedin",
  x: "twitter",
  gh: "github",
};

export function normalizeSource(raw: string | null | undefined): string {
  if (!raw) return DEFAULT_SOURCE;
  const cleaned = raw.toLowerCase().replace(/[^a-z0-9_-]/g, "").slice(0, 32);
  if (!cleaned) return DEFAULT_SOURCE;
  return SOURCE_ALIASES[cleaned] ?? cleaned;
}

/**
 * Tag outbound URLs so the destination's own analytics attribute the visit.
 * Skips mailto:/tel: and anything that already carries a utm_source.
 */
export function withUtm(href: string, source: string): string {
  const isInternal = href.startsWith("/");
  if (!isInternal && !/^https?:\/\//i.test(href)) return href;

  try {
    const url = new URL(href, "https://pushkaraj.dev");
    if (!url.searchParams.has("utm_source")) {
      url.searchParams.set("utm_source", source);
      url.searchParams.set("utm_medium", "bio");
      url.searchParams.set("utm_campaign", "links");
    }
    return isInternal ? `${url.pathname}${url.search}` : url.toString();
  } catch {
    return href;
  }
}
