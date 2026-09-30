import re, sys, glob, os

def check(path):
    s = open(path).read()
    m = re.search(r'viewBox="0 0 (\d+) (\d+)"', s)
    W, H = int(m.group(1)), int(m.group(2))
    bad = []
    for r in re.finditer(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"', s):
        x, y, w, h = map(float, r.groups())
        if x + w > W + 0.6 or y + h > H + 0.6 or x < -0.6 or y < -0.6:
            bad.append(f"rect x={x} y={y} w={w} h={h} -> right={x+w} bottom={y+h}")
    for t in re.finditer(r'<text x="([\d.]+)" y="([\d.]+)"[^>]*text-anchor="(\w+)"[^>]*>([^<]*)<', s):
        x, y, anc, txt = float(t.group(1)), float(t.group(2)), t.group(3), t.group(4)
        fs = float(re.search(r'font-size="([\d.]+)"', t.group(0)).group(1))
        est = len(txt) * fs * 0.60
        left = x if anc == "start" else (x - est/2 if anc == "middle" else x - est)
        right = left + est
        if right > W + 1 or left < -1 or y > H + 1:
            bad.append(f'text "{txt[:42]}" x={x} anchor={anc} -> ~[{left:.0f},{right:.0f}] y={y}')
    for l in re.finditer(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)"', s):
        for i, v in enumerate(map(float, l.groups())):
            lim = W if i % 2 == 0 else H
            if v > lim + 0.6 or v < -0.6:
                bad.append(f"line coord {v} exceeds {lim}")
    for p in re.finditer(r'<path d="([^"]+)"', s):
        for cx, cy in re.findall(r'([\d.]+) ([\d.]+)', p.group(1)):
            if float(cx) > W + 0.6 or float(cy) > H + 0.6:
                bad.append(f"path point ({cx},{cy}) exceeds {W}x{H}")
    return W, H, bad

rc = 0
for f in sorted(glob.glob("../assets/img/diagrams/*.svg")):
    W, H, bad = check(f)
    name = os.path.basename(f)
    if bad:
        rc = 1
        print(f"FAIL {name}  ({W}x{H})")
        for b in dict.fromkeys(bad):
            print("      " + b)
    else:
        print(f"ok   {name}  ({W}x{H})")
sys.exit(rc)
