import type { Metadata } from "next";
import "@/styles/globals.css";
import { Analytics } from "@vercel/analytics/next";

export const metadata: Metadata = {
  // Without this, OG/Twitter image URLs resolve against the per-deployment
  // Vercel host instead of the canonical domain, which breaks link previews.
  metadataBase: new URL("https://www.pushkaraj.dev"),
  title: "Pushkaraj Baradkar",
  description:
    "Pushkaraj Baradkar — software engineer and AI researcher.",
  icons: {
    icon: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="font-body antialiased">
        {children}
        <Analytics />
      </body>
    </html>
  );
}
