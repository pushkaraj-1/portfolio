import sys; sys.path.insert(0, ".")
from svglib import SVG, INK, MUTED, FAINT, MONO
OUT = "../assets/img/diagrams/"
IND="#6366f1"; TEAL="#0d9488"; VIO="#8b5cf6"; AMB="#d97706"; SLATE="#64748b"

s = SVG(900, 470)
s.text(26, 32, "Blockchain-based music streaming with NFTs", size=14.5, weight=700, color=INK)
s.text(26, 50, "rights encoded on-chain; royalties split automatically at play time", size=11, color=MUTED, font=MONO)

s.node(26, 92, 180, 66, "artist", "mints release", IND, tsize=13)
s.node(360, 92, 200, 66, "NFT", "ownership + splits", VIO, tsize=13)
s.node(694, 92, 180, 66, "listener", "streams track", TEAL, tsize=13)
s.arrow(206, 125, 356, 125, "mint")
s.arrow(694, 125, 564, 125, "play")

s.band(26, 186, 848, 116, "smart contract")
s.node(46, 220, 250, 62, "rights registry", "who owns what share", SLATE, tsize=12.5)
s.node(322, 220, 250, 62, "royalty split", "deterministic payout", AMB, tsize=12.5)
s.node(598, 220, 256, 62, "settlement", "per-stream transfer", TEAL, tsize=12.5)
s.arrow(296, 251, 318, 251); s.arrow(572, 251, 594, 251)
s.elbow(460, 158, 460, 220, via_y=200)

s.text(450, 344, "the intermediary that normally holds and delays payment is removed",
       size=11.5, color=INK, anchor="middle", font=MONO, weight=600)
s.text(450, 368, "settlement becomes a property of playback rather than a quarterly reconciliation",
       size=10.5, color=FAINT, anchor="middle", font=MONO)

s.rect(26, 396, 848, 52, fill="none", stroke="#e3e8ef", rx=10)
s.text(46, 419, "IEEE ICSCSS 2023", size=11.5, color=INK, font=MONO, weight=700)
s.text(46, 436, "P. Baradkar et al.  -  Cited by 7", size=10.5, color=MUTED, font=MONO)
s.save(OUT+"publication-ieee.svg", "IEEE NFT music streaming paper figure")
print("publication figure written")
