import { ImageResponse } from "next/og";

// Rendered into DM and social previews — the comment-to-DM automation sends
// this URL, and Instagram renders a card for it.
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";
export const alt = "Pushkaraj Baradkar — Links";

export default function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          background: "#ffffff",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          padding: "0 96px",
        }}
      >
        <div style={{ fontSize: 68, fontWeight: 600, color: "#000000", letterSpacing: -1.5 }}>
          Pushkaraj Baradkar
        </div>
        <div style={{ marginTop: 20, fontSize: 40, color: "#000000" }}>
          AI engineer at Tabhi
        </div>
        <div style={{ marginTop: 12, fontSize: 40, color: "#9b9b9b" }}>
          Everything I build, in one place.
        </div>
        <div style={{ marginTop: 56, fontSize: 32, color: "#9b9b9b" }}>
          pushkaraj.dev/links
        </div>
      </div>
    ),
    size,
  );
}
