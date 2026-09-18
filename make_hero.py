#!/usr/bin/env python3
"""Procedurally generate the ReaR project-page hero illustration: a night
highway scene with an ego vehicle, a forward radar FOV cone with range
rings, scattered detections, and a faint LiDAR point sweep behind it —
built from the same navy/amber palette as the paper figures."""
import numpy as np

W, H = 1600, 640
NAVY_DARK = "#0A1428"
NAVY = "#0E1A33"
NAVY_MID = "#16294D"
NAVY_LT = "#1E3A5F"
AMBER = "#E8873D"
AMBER_D = "#C96A22"
AMBER_LT = "#F7D9BE"
ICE = "#8FA9C9"
WHITE = "#F4F7FB"
LINE = "#2A3F63"

svg = []
svg.append(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="heroTitle">')
svg.append('<title id="heroTitle">Physics-guided radar synthesis over a night highway scene</title>')

# ---- defs: gradients & filters ----
svg.append('''<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#060B18"/>
    <stop offset="55%" stop-color="#0E1A33"/>
    <stop offset="100%" stop-color="#16294D"/>
  </linearGradient>
  <radialGradient id="coneFill" cx="50%" cy="100%" r="85%">
    <stop offset="0%" stop-color="#E8873D" stop-opacity="0.32"/>
    <stop offset="60%" stop-color="#E8873D" stop-opacity="0.12"/>
    <stop offset="100%" stop-color="#E8873D" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#F7D9BE" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="#F7D9BE" stop-opacity="0"/>
  </radialGradient>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="6"/>
  </filter>
</defs>''')

# ---- background sky ----
svg.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#sky)"/>')

# ---- faint starfield / sensor-grid dots (upper sky) ----
rng = np.random.default_rng(6)
sx = rng.uniform(0, W, 90)
sy = rng.uniform(0, H*0.42, 90)
sr = rng.uniform(0.5, 1.4, 90)
so = rng.uniform(0.10, 0.5, 90)
for x, y, r, o in zip(sx, sy, sr, so):
    svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{WHITE}" opacity="{o:.2f}"/>')

# ---- distant skyline silhouette ----
rng2 = np.random.default_rng(3)
bx = 0
bars = []
while bx < W:
    bw = rng2.uniform(28, 70)
    bh = rng2.uniform(30, 130)
    bars.append((bx, bw, bh))
    bx += bw + rng2.uniform(2, 10)
horizon = H*0.60
for bx, bw, bh in bars:
    svg.append(f'<rect x="{bx:.1f}" y="{horizon-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{NAVY_MID}" opacity="0.55"/>')
    # a few lit windows
    if bw > 34 and bh > 50:
        for _ in range(int(bh//22)):
            wx = bx + rng2.uniform(6, bw-12)
            wy = horizon - rng2.uniform(10, bh-8)
            if rng2.random() < 0.35:
                svg.append(f'<rect x="{wx:.1f}" y="{wy:.1f}" width="3.2" height="4.2" fill="{AMBER_LT}" opacity="{rng2.uniform(0.25,0.6):.2f}"/>')

# ---- road surface ----
svg.append(f'<rect x="0" y="{horizon:.0f}" width="{W}" height="{H-horizon:.0f}" fill="{NAVY_DARK}"/>')

# vanishing point (slightly right of center, where the radar cone apex will sit)
vpx, vpy = W*0.50, horizon - 6

# road edge lines converging to vanishing point
road_half_bottom = W*0.60
for side in (-1, 1):
    x_bottom = vpx + side*road_half_bottom
    svg.append(f'<line x1="{vpx:.1f}" y1="{vpy:.1f}" x2="{x_bottom:.1f}" y2="{H}" stroke="{LINE}" stroke-width="2" opacity="0.8"/>')

# lane dashes (perspective-scaled)
for i in range(1, 9):
    t = i / 9.0
    y = vpy + (H - vpy) * (t**1.6)
    half_w = road_half_bottom * (t**1.6) * 0.02
    dash_w = 6 + 46*t
    svg.append(f'<rect x="{vpx-dash_w/2:.1f}" y="{y:.1f}" width="{dash_w:.1f}" height="{2+4*t:.1f}" rx="2" fill="{ICE}" opacity="{0.15+0.35*t:.2f}"/>')

# ---- radar FOV cone (apex at ego sensor position) ----
apex_x, apex_y = vpx, H*0.90
cone_half_deg = 30
cone_len = H*0.62
import math
a1 = math.radians(90 - cone_half_deg)
a2 = math.radians(90 + cone_half_deg)
x1 = apex_x + cone_len*math.cos(a1)
y1 = apex_y - cone_len*math.sin(a1)
x2 = apex_x + cone_len*math.cos(a2)
y2 = apex_y - cone_len*math.sin(a2)
svg.append(f'<path d="M {apex_x:.1f} {apex_y:.1f} L {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f} Z" fill="url(#coneFill)"/>')

# range rings (arcs) within the cone
for frac in (0.32, 0.58, 0.84):
    r = cone_len*frac
    aa1 = math.radians(90 - cone_half_deg)
    aa2 = math.radians(90 + cone_half_deg)
    rx1 = apex_x + r*math.cos(aa1); ry1 = apex_y - r*math.sin(aa1)
    rx2 = apex_x + r*math.cos(aa2); ry2 = apex_y - r*math.sin(aa2)
    svg.append(f'<path d="M {rx1:.1f} {ry1:.1f} A {r:.1f} {r:.1f} 0 0 1 {rx2:.1f} {ry2:.1f}" '
               f'fill="none" stroke="{AMBER_D}" stroke-width="1.3" opacity="0.55" stroke-dasharray="2 5"/>')

# cone edge lines
svg.append(f'<line x1="{apex_x:.1f}" y1="{apex_y:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{AMBER_D}" stroke-width="1.3" opacity="0.55"/>')
svg.append(f'<line x1="{apex_x:.1f}" y1="{apex_y:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{AMBER_D}" stroke-width="1.3" opacity="0.55"/>')

# ---- scattered radar detections inside the cone (colored like RCS colormap) ----
rng3 = np.random.default_rng(11)
det_colors = ["#4B1D91", "#B23A2E", "#C96A22", "#E8873D", "#F2B25C", "#F7D9BE"]
n_det = 46
for _ in range(n_det):
    frac = rng3.uniform(0.12, 0.95)
    spread = rng3.uniform(-1, 1) * cone_half_deg * (0.55 + 0.4*frac)
    ang = math.radians(90 - spread)
    r = cone_len * frac
    dx = apex_x + r*math.cos(ang)
    dy = apex_y - r*math.sin(ang)
    if dy < horizon - 4:
        continue
    c = det_colors[int(rng3.integers(0, len(det_colors)))]
    rad = rng3.uniform(2.1, 4.6) * (0.6 + 0.6*(1-frac))
    op = rng3.uniform(0.55, 0.95)
    svg.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{rad:.2f}" fill="{c}" opacity="{op:.2f}"/>')

# a few "clutter" detections outside the cone, dimmer, small
rng4 = np.random.default_rng(23)
for _ in range(14):
    dx = rng4.uniform(W*0.05, W*0.95)
    dy = rng4.uniform(horizon+10, H-20)
    svg.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{rng4.uniform(1.2,2.2):.2f}" fill="{ICE}" opacity="{rng4.uniform(0.15,0.35):.2f}"/>')

# ---- ego vehicle silhouette (simplified top-down car, sitting at apex) ----
car_w, car_l = 96, 150
cx0, cy0 = apex_x, apex_y + 6
svg.append(f'''<g transform="translate({cx0:.1f},{cy0:.1f})">
  <path d="M {-car_w*0.30:.1f} {-car_l:.1f}
           C {-car_w*0.30:.1f} {-car_l-10:.1f} {car_w*0.30:.1f} {-car_l-10:.1f} {car_w*0.30:.1f} {-car_l:.1f}
           L {car_w*0.40:.1f} {-car_l*0.72:.1f}
           Q {car_w*0.50:.1f} {-car_l*0.58:.1f} {car_w*0.46:.1f} {-car_l*0.42:.1f}
           L {car_w*0.50:.1f} {-car_l*0.08:.1f}
           Q {car_w*0.50:.1f} {car_l*0.10:.1f} {car_w*0.40:.1f} {car_l*0.16:.1f}
           L {car_w*0.30:.1f} {car_l*0.20:.1f}
           Q {car_w*0.10:.1f} {car_l*0.24:.1f} 0 {car_l*0.24:.1f}
           Q {-car_w*0.10:.1f} {car_l*0.24:.1f} {-car_w*0.30:.1f} {car_l*0.20:.1f}
           L {-car_w*0.40:.1f} {car_l*0.16:.1f}
           Q {-car_w*0.50:.1f} {car_l*0.10:.1f} {-car_w*0.50:.1f} {-car_l*0.08:.1f}
           L {-car_w*0.46:.1f} {-car_l*0.42:.1f}
           Q {-car_w*0.50:.1f} {-car_l*0.58:.1f} {-car_w*0.40:.1f} {-car_l*0.72:.1f}
           Z"
        fill="{NAVY_LT}" stroke="{ICE}" stroke-width="1.3" opacity="0.95"/>
  <path d="M {-car_w*0.24:.1f} {-car_l*0.78:.1f} Q 0 {-car_l*0.92:.1f} {car_w*0.24:.1f} {-car_l*0.78:.1f}
           L {car_w*0.20:.1f} {-car_l*0.54:.1f} Q 0 {-car_l*0.46:.1f} {-car_w*0.20:.1f} {-car_l*0.54:.1f} Z"
        fill="{NAVY_DARK}" opacity="0.85"/>
  <circle cx="{-car_w*0.44:.1f}" cy="{-car_l*0.60:.1f}" r="3.4" fill="{AMBER_LT}" opacity="0.9"/>
  <circle cx="{car_w*0.44:.1f}" cy="{-car_l*0.60:.1f}" r="3.4" fill="{AMBER_LT}" opacity="0.9"/>
  <rect x="{-car_w*0.46:.1f}" y="{-car_l*0.02:.1f}" width="6" height="16" rx="2" fill="{AMBER}" opacity="0.85"/>
  <rect x="{car_w*0.46-6:.1f}" y="{-car_l*0.02:.1f}" width="6" height="16" rx="2" fill="{AMBER}" opacity="0.85"/>
</g>''')

# headlight glow + sensor pod marker at the very apex
svg.append(f'<circle cx="{apex_x:.1f}" cy="{apex_y:.1f}" r="34" fill="url(#glow)" opacity="0.55"/>')
svg.append(f'<circle cx="{apex_x:.1f}" cy="{apex_y:.1f}" r="5.5" fill="{AMBER_LT}"/>')
svg.append(f'<circle cx="{apex_x:.1f}" cy="{apex_y:.1f}" r="9" fill="none" stroke="{AMBER}" stroke-width="1.4" opacity="0.8"/>')

# ---- faint LiDAR point-sweep arcs behind/above the car (blue-ice, denser, wider FOV) ----
rng5 = np.random.default_rng(41)
for _ in range(140):
    ang = rng5.uniform(math.radians(15), math.radians(165))
    r = rng5.uniform(cone_len*0.15, cone_len*1.05)
    dx = apex_x + r*math.cos(ang)
    dy = apex_y - r*math.sin(ang)*0.55 - 6
    if dy < horizon-2 or dy > apex_y:
        continue
    svg.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{rng5.uniform(0.5,1.1):.2f}" fill="{ICE}" opacity="{rng5.uniform(0.08,0.22):.2f}"/>')

# ---- subtle vignette ----
svg.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#sky)" opacity="0"/>')
svg.append(f'''<linearGradient id="vig" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#050912" stop-opacity="0.35"/>
  <stop offset="15%" stop-color="#050912" stop-opacity="0"/>
  <stop offset="85%" stop-color="#050912" stop-opacity="0"/>
  <stop offset="100%" stop-color="#050912" stop-opacity="0.25"/>
</linearGradient>''')
svg.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#vig)"/>')

svg.append('</svg>')

with open('hero.svg', 'w') as f:
    f.write('\n'.join(svg))
print("hero.svg written,", sum(len(s) for s in svg), "chars")
