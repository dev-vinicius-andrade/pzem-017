import sys

W, H = 1820, 1060
out = []
a = out.append

C = {
    "5v": "#d32f2f", "gnd": "#222222", "3v3": "#ef6c00",
    "tx": "#1565c0", "rx": "#2e7d32", "de": "#6a1b9a",
    "a": "#c9a000", "b": "#00838f",
    "rs": "#ad1457", "e": "#4527a0", "d4": "#0277bd", "d5": "#00897b",
    "d6": "#558b2f", "d7": "#6d4c41",
    "red": "#d32f2f", "black": "#222222", "green": "#2e7d32", "blue": "#1565c0",
}

def text(x, y, s, size=14, anchor="start", weight="normal", fill="#222", extra=""):
    a(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}" {extra}>{s}</text>')

def poly(points, color, width=3, hops=()):
    """Orthogonal polyline. hops: set of (x,y) points on vertical segments to draw a jump arc."""
    d = f"M {points[0][0]} {points[0][1]}"
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        if x1 == x2:
            hs = sorted([h for (hx, h) in hops if hx == x1 and min(y1, y2) < h < max(y1, y2)], reverse=(y2 < y1))
            for h in hs:
                r = 7
                if y2 > y1:
                    d += f" L {x1} {h - r} A {r} {r} 0 0 1 {x1} {h + r}"
                else:
                    d += f" L {x1} {h + r} A {r} {r} 0 0 0 {x1} {h - r}"
        d += f" L {x2} {y2}"
    a(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>')

def dot(x, y, color="#222"):
    a(f'<circle cx="{x}" cy="{y}" r="5" fill="{color}"/>')

def pin(x, y):
    a(f'<circle cx="{x}" cy="{y}" r="5" fill="#d4af37" stroke="#7a5c00" stroke-width="1.5"/>')

def tag(x, y, label, color):
    w = 10 + 9 * len(label)
    a(f'<rect x="{x}" y="{y - 11}" width="{w}" height="22" rx="4" fill="{color}"/>')
    text(x + w / 2, y + 5, label, 13, "middle", "bold", "#fff")

a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Segoe UI, Arial, sans-serif">')
a(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
text(40, 50, "PZEM-017 Battery Monitor — Wiring", 28, weight="bold")
text(40, 80, "ESP32 DevKit V1 (DOIT) · MAX3485 RS485 module (3.3 V) · PZEM-017 · Winstar WH1602A 16x2 LCD · 24 V → 5 V buck", 15, fill="#555")

# ---------------- LCD ----------------
lx1, lx2, ly1, ly2 = 150, 390, 170, 690
a(f'<rect x="{lx1}" y="{ly1}" width="{lx2 - lx1}" height="{ly2 - ly1}" rx="8" fill="#2f6b2f" stroke="#1b3d1b" stroke-width="2"/>')
a(f'<rect x="{lx1 + 25}" y="{ly1 + 60}" width="110" height="{ly2 - ly1 - 120}" rx="4" fill="#9ccc65" stroke="#33691e" stroke-width="2"/>')
text(lx1 + 80, ly1 + 35, "16x2 LCD", 16, "middle", "bold", "#fff")
text(lx1 + 80, ly2 - 25, "WH1602A", 13, "middle", fill="#e8f5e9")
lcd_pins = ["VSS", "VDD", "V0", "RS", "RW", "E", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "A", "K"]
lpy = {n: 200 + 30 * (n - 1) for n in range(1, 17)}
for n, name in enumerate(lcd_pins, 1):
    pin(lx2, lpy[n])
    text(lx2 - 12, lpy[n] + 5, f"{n} {name}", 13, "end", fill="#fff")

# ---------------- ESP32 ----------------
ex1, ex2, ey1, ey2 = 640, 860, 160, 690
a(f'<rect x="{ex1}" y="{ey1}" width="{ex2 - ex1}" height="{ey2 - ey1}" rx="10" fill="#1e2a38" stroke="#0d141c" stroke-width="2"/>')
a(f'<rect x="{ex1 + 55}" y="{ey1 + 75}" width="110" height="120" rx="4" fill="#b0b8c0" stroke="#6b7580"/>')
text(750, ey1 + 30, "ESP32", 18, "middle", "bold", "#fff")
text(750, ey1 + 52, "DevKit V1", 13, "middle", fill="#cfd8dc")
text(750, ey1 + 140, "WROOM-32", 12, "middle", fill="#37474f")
a(f'<rect x="725" y="{ey2 - 12}" width="50" height="24" rx="3" fill="#9e9e9e" stroke="#616161"/>')
text(750, ey2 + 32, "USB", 12, "middle", fill="#555")
left = ["EN", "VP", "VN", "D34", "D35", "D32", "D33", "D25", "D26", "D27", "D14", "D12", "D13", "GND", "VIN"]
right = ["D23", "D22", "TX0", "RX0", "D21", "D19", "D18", "D5", "TX2", "RX2", "D4", "D2", "D15", "GND", "3V3"]
ely = {nm: 215 + 30 * i for i, nm in enumerate(left)}
ery = {nm: 215 + 30 * i for i, nm in enumerate(right)}
for nm, y in ely.items():
    pin(ex1, y); text(ex1 + 12, y + 5, nm, 13, fill="#fff")
for nm, y in ery.items():
    pin(ex2, y); text(ex2 - 12, y + 5, nm, 13, "end", fill="#fff")
text(ex2 + 8, ery["TX2"] - 10, "GPIO17", 10, fill="#888")
text(ex2 + 8, ery["RX2"] - 10, "GPIO16", 10, fill="#888")
text(ex2 + 8, ery["D4"] - 10, "GPIO4", 10, fill="#888")

# LCD signal wires
poly([(lx2, lpy[4]), (600, lpy[4]), (600, ely["D32"]), (ex1, ely["D32"])], C["rs"])
poly([(lx2, lpy[6]), (580, lpy[6]), (580, ely["D33"]), (ex1, ely["D33"])], C["e"])
poly([(lx2, lpy[11]), (470, lpy[11]), (470, ely["D25"]), (ex1, ely["D25"])], C["d4"])
poly([(lx2, lpy[12]), (500, lpy[12]), (500, ely["D26"]), (ex1, ely["D26"])], C["d5"])
poly([(lx2, lpy[13]), (530, lpy[13]), (530, ely["D27"]), (ex1, ely["D27"])], C["d6"])
poly([(lx2, lpy[14]), (560, lpy[14]), (560, ely["D14"]), (ex1, ely["D14"])], C["d7"])

# LCD power tags
for n, lbl, col in [(1, "GND", C["gnd"]), (2, "5V", C["5v"]), (5, "GND", C["gnd"]), (15, "5V", C["5v"]), (16, "GND", C["gnd"])]:
    poly([(lx2, lpy[n]), (412, lpy[n])], col, 2)
    tag(412, lpy[n], lbl, col)
for n in range(7, 11):
    text(400, lpy[n] + 5, "NC", 11, fill="#999")
# contrast pot on pin 3
py = lpy[3]
poly([(lx2, py), (440, py)], "#555", 2)
a(f'<rect x="440" y="{py - 12}" width="46" height="24" rx="3" fill="#fff" stroke="#555" stroke-width="2"/>')
a(f'<path d="M 452 {py + 16} L 475 {py - 16}" stroke="#555" stroke-width="2" marker-end="url(#arr)"/>')
text(463, py - 18, "10k pot", 12, "middle", fill="#555")
poly([(486, py - 6), (505, py - 6)], C["5v"], 2); tag(505, py - 14, "5V", C["5v"])
poly([(486, py + 6), (505, py + 6)], C["gnd"], 2); tag(505, py + 14, "GND", C["gnd"])

# ---------------- RS485 module ----------------
mx1, mx2, my1, my2 = 950, 1110, 430, 665
a(f'<rect x="{mx1}" y="{my1}" width="{mx2 - mx1}" height="{my2 - my1}" rx="8" fill="#1565c0" stroke="#0d3c73" stroke-width="2"/>')
text(1030, my1 - 30, "RS485 module", 15, "middle", "bold")
text(1030, my1 - 12, "MAX3485 · 3.3 V", 12, "middle", fill="#555")
mpins = {"DI": 455, "RO": 485, "DE": 515, "RE": 545, "GND": 605, "VCC": 635}
for nm, y in mpins.items():
    pin(mx1, y); text(mx1 + 12, y + 5, nm, 13, fill="#fff")
mr = {"B": 480, "A": 520}
for nm, y in mr.items():
    pin(mx2, y); text(mx2 - 12, y + 5, nm, 13, "end", fill="#fff")

poly([(ex2, ery["TX2"]), (mx1, mpins["DI"])], C["tx"])
poly([(ex2, ery["RX2"]), (mx1, mpins["RO"])], C["rx"])
poly([(ex2, ery["D4"]), (mx1, mpins["DE"])], C["de"])
poly([(mx1, mpins["RE"]), (930, mpins["RE"]), (930, mpins["DE"])], C["de"])
dot(930, mpins["DE"], C["de"])
text(1030, 685, "DE and RE bridged", 11, "middle", fill=C["de"])
poly([(ex2, ery["GND"]), (mx1, mpins["GND"])], C["gnd"])
poly([(ex2, ery["3V3"]), (mx1, mpins["VCC"])], C["3v3"])

# ---------------- PZEM-017 ----------------
px1, px2, py1, py2 = 1220, 1400, 380, 640
a(f'<rect x="{px1}" y="{py1}" width="{px2 - px1}" height="{py2 - py1}" rx="12" fill="#263238" stroke="#000" stroke-width="2"/>')
for i in range(8):
    a(f'<line x1="{px1 + 30 + i * 18}" y1="{py1 + 20}" x2="{px1 + 10 + i * 18}" y2="{py2 - 20}" stroke="#37474f" stroke-width="6"/>')
text(1310, py1 - 30, "PZEM-017", 16, "middle", "bold")
text(1310, py1 - 12, "DC meter", 12, "middle", fill="#555")
pc = {"5V": 440, "B": 480, "A": 520, "GND": 560}
for nm, y in pc.items():
    pin(px1, y); text(px1 + 12, y + 5, nm, 13, "start", "bold", "#fff")
pm = {"V+": 440, "V−": 480, "I": 520, "I ": 560}
for nm, y in pm.items():
    pin(px2, y); text(px2 - 12, y + 5, nm.strip(), 13, "end", "bold", "#fff")
text(px1 + 12, py2 - 8, "comm (isolated)", 11, fill="#b0bec5")
text(px2 - 12, py2 - 8, "measure", 11, "end", fill="#b0bec5")

poly([(mx2, mr["B"]), (px1, pc["B"])], C["b"])
poly([(mx2, mr["A"]), (px1, pc["A"])], C["a"])
text(1165, 474, "B", 12, "middle", "bold", C["b"])
text(1165, 514, "A", 12, "middle", "bold", C["a"])

# ---------------- Power rails ----------------
RAIL5, RAILG = 800, 840
# buck converter
bx1, bx2, by1, by2 = 330, 490, 770, 860
a(f'<rect x="{bx1}" y="{by1}" width="{bx2 - bx1}" height="{by2 - by1}" rx="6" fill="#455a64" stroke="#263238" stroke-width="2"/>')
text(410, by1 + 32, "Buck 24V→5V", 14, "middle", "bold", "#fff")
text(410, by1 + 52, "MP1584 / LM2596", 11, "middle", fill="#cfd8dc")
text(410, by1 + 70, "set 5.0 V before use", 11, "middle", fill="#ffcc80")
for nm, y in [("IN−", RAIL5), ("IN+", 825)]:
    pin(bx1, y); text(bx1 - 8, y - 6, nm, 11, "end", fill="#555")
for nm, y in [("OUT+", RAIL5), ("OUT−", 825)]:
    pin(bx2, y); text(bx2 + 8, y - 6, nm, 11, fill="#555")

# 5V rail: buck OUT+ -> ESP VIN -> PZEM 5V
poly([(bx2, RAIL5), (1195, RAIL5), (1195, pc["5V"]), (px1, pc["5V"])], C["5v"], hops={(1195, mr["B"]), (1195, mr["A"])})
poly([(ex1, ely["VIN"]), (620, ely["VIN"]), (620, RAIL5)], C["5v"])
dot(620, RAIL5, C["5v"])
text(700, RAIL5 - 8, "5 V", 13, weight="bold", fill=C["5v"])
# GND rail
poly([(bx2, 825), (510, 825), (510, RAILG), (1205, RAILG), (1205, pc["GND"]), (px1, pc["GND"])], C["gnd"])
poly([(ex1, ely["GND"]), (610, ely["GND"]), (610, RAILG)], C["gnd"], hops={(610, RAIL5)})
dot(610, RAILG)
text(700, RAILG + 20, "GND (common)", 13, weight="bold", fill=C["gnd"])

# ---------------- Battery side ----------------
# batteries
for (y, lbl) in [(200, "Battery 1"), (320, "Battery 2")]:
    a(f'<rect x="1600" y="{y}" width="160" height="80" rx="6" fill="#37474f" stroke="#000" stroke-width="2"/>')
    text(1680, y + 35, lbl, 14, "middle", "bold", "#fff")
    text(1680, y + 55, "12 V 75 Ah", 12, "middle", fill="#ffeb3b")
text(1680, 192, "24 V bank (series)", 13, "middle", "bold", fill="#555")
# B1: + right (1760,220), − left (1600,260); B2: + left (1600,340), − left (1600,380)
pin(1760, 220); text(1768, 214, "+", 16, weight="bold", fill=C["red"])
pin(1600, 260); text(1592, 254, "−", 16, "end", "bold")
pin(1600, 340); text(1592, 334, "+", 16, "end", "bold", fill=C["red"])
pin(1600, 380); text(1592, 396, "−", 16, "end", "bold")
poly([(1600, 260), (1585, 260), (1585, 340), (1600, 340)], C["black"])  # series link

# load
a('<rect x="1600" y="520" width="160" height="80" rx="6" fill="#fff8e1" stroke="#f9a825" stroke-width="2"/>')
text(1680, 557, "Load", 15, "middle", "bold")
text(1680, 577, "inverter / DC loads", 11, "middle", fill="#777")
pin(1760, 540); pin(1600, 580)
text(1768, 534, "+", 14, weight="bold", fill=C["red"])
text(1592, 596, "−", 14, "end", "bold")

# shunt
a('<rect x="1490" y="410" width="20" height="240" rx="3" fill="#bdbdbd" stroke="#616161" stroke-width="2"/>')
text(1475, 660, "shunt", 12, "end", "bold", fill="#555")
dot(1500, 420, "#616161"); dot(1500, 640, "#616161")
a('<circle cx="1500" cy="450" r="4" fill="#fff" stroke="#616161" stroke-width="2"/>')
a('<circle cx="1500" cy="610" r="4" fill="#fff" stroke="#616161" stroke-width="2"/>')

# bank + -> PZEM V+, -> load +, -> buck (via fuse)
poly([(1760, 220), (1760, 160), (1440, 160), (1440, pm["V+"]), (px2, pm["V+"])], C["red"])
poly([(1760, 220), (1780, 220), (1780, 900), (300, 900), (300, 825), (bx1, 825)], C["red"])
poly([(1780, 540), (1760, 540)], C["red"])
dot(1780, 540, C["red"])
# fuse on + line
a('<rect x="1080" y="888" width="60" height="24" rx="4" fill="#fff" stroke="#d32f2f" stroke-width="2"/>')
text(1110, 905, "FUSE 1A", 11, "middle", "bold", fill=C["red"])
# bank − -> shunt battery side; PZEM V− to same point
poly([(1600, 380), (1500, 380), (1500, 420)], C["black"])
poly([(px2, pm["V−"]), (1460, pm["V−"]), (1460, 420), (1500, 420)], C["black"])
# shunt sense -> PZEM I
poly([(1500, 450), (1480, 450), (1480, pm["I"]), (px2, pm["I"])], C["green"])
poly([(1500, 610), (1490, 610), (1490, pm["I "]), (px2, pm["I "])], C["blue"])
# shunt load side -> load −
poly([(1500, 640), (1560, 640), (1560, 580), (1600, 580)], C["black"])
# bank − -> buck IN−
poly([(1540, 380), (1540, 930), (290, 930), (290, RAIL5), (bx1, RAIL5)], C["black"], hops={(1540, 640)})
dot(1540, 380)

# ---------------- legend / notes ----------------
nx, ny = 40, 1030
notes = [
    "Measurement side (right of PZEM) follows the Peacefair diagram — check the labels printed on your PZEM terminal.",
    "Tags with the same name are the same net: 5V = buck OUT+ / ESP32 VIN, GND = common ground.  Wires crossing with a hop are NOT connected.",
    "Auto-direction RS485 module: skip D4 and the DE/RE wires.  Set the buck to 5.0 V with a multimeter BEFORE connecting the ESP32.",
]
for i, n in enumerate(notes):
    text(nx, ny - 40 + i * 20, "• " + n, 13, fill="#444")

a('<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#555"/></marker></defs>')
a("</svg>")

open(sys.argv[1], "w", encoding="utf-8").write("\n".join(out))
print("ok")
