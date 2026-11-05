"""Generate docs/wiring-usb-cable.svg: PZEM-017 -> network cable -> USB-RS485 -> HA server.

Usage: python docs/gen_wiring_usb.py docs/wiring-usb-cable.svg
"""
import math
import sys

W, H = 1640, 820
out = []
a = out.append

ORANGE, BROWN = "#ef6c00", "#6d4c41"


def text(x, y, s, size=14, anchor="start", weight="normal", fill="#222"):
    a(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}">{s}</text>')


def line(x1, y1, x2, y2, color, width=4, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{d}/>')


def wire(x1, y1, x2, y2, color, striped=False, width=5):
    """Solid wire, or white wire with colored stripe (e.g. orange/white)."""
    if striped:
        line(x1, y1, x2, y2, "#999", width + 2)
        line(x1, y1, x2, y2, "#fff", width)
        line(x1, y1, x2, y2, color, width, "10 8")
    else:
        line(x1, y1, x2, y2, "#333", width + 2)
        line(x1, y1, x2, y2, color, width)


def wave(x1, x2, y, amp, phase, color, striped):
    pts = []
    for i in range(0, int(x2 - x1) + 1, 4):
        pts.append(f"{x1 + i},{y + amp * math.sin(i / 14 + phase):.1f}")
    p = " ".join(pts)
    if striped:
        a(f'<polyline points="{p}" fill="none" stroke="#999" stroke-width="7"/>')
        a(f'<polyline points="{p}" fill="none" stroke="#fff" stroke-width="5"/>')
        a(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="5" stroke-dasharray="10 8"/>')
    else:
        a(f'<polyline points="{p}" fill="none" stroke="#333" stroke-width="7"/>')
        a(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="5"/>')


def screw(x, y):
    a(f'<circle cx="{x}" cy="{y}" r="11" fill="#cfd8dc" stroke="#455a64" stroke-width="2"/>')
    a(f'<line x1="{x - 7}" y1="{y + 7}" x2="{x + 7}" y2="{y - 7}" stroke="#455a64" stroke-width="2"/>')


a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Segoe UI, Arial, sans-serif">')
a(f'<rect width="{W}" height="{H}" fill="#fff"/>')
text(40, 50, "PZEM-017 → cabo de rede → cabo USB-RS485 → Home Assistant", 26, weight="bold")
text(40, 80, "Sem ESP32: o conversor USB fica no servidor do HA e um cabo de rede (usado só como fio) leva o sinal até o PZEM.", 15, fill="#555")

# rows for the 4 signals (top -> bottom, same order on both ends)
rows = [("5V", 300, BROWN, False, "marrom"),
        ("B", 350, ORANGE, True, "laranja/branco"),
        ("A", 400, ORANGE, False, "laranja"),
        ("GND", 450, BROWN, True, "marrom/branco")]

# ---------- measurement side (already wired) ----------
a('<rect x="40" y="230" width="190" height="300" rx="10" fill="#eceff1" stroke="#90a4ae" stroke-width="2" stroke-dasharray="6 5"/>')
text(135, 270, "Baterias 24 V", 15, "middle", "bold")
text(135, 292, "+ shunt + carga", 13, "middle", fill="#555")
text(135, 500, "já ligado", 13, "middle", "bold", "#2e7d32")
text(135, 518, "(não mexer)", 12, "middle", fill="#2e7d32")
for i, (lbl, col) in enumerate([("V+", "#d32f2f"), ("V−", "#222"), ("I", "#2e7d32"), ("I", "#1565c0")]):
    y = 330 + i * 40
    line(230, y, 290, y, col, 4)
    text(250, y - 8, lbl, 12, fill=col, weight="bold")

# ---------- PZEM ----------
px1, px2 = 290, 520
a(f'<rect x="{px1}" y="210" width="{px2 - px1}" height="340" rx="16" fill="#263238" stroke="#000" stroke-width="2"/>')
for i in range(9):
    a(f'<line x1="{px1 + 50 + i * 18}" y1="240" x2="{px1 + 25 + i * 18}" y2="520" stroke="#37474f" stroke-width="7"/>')
text(405, 195, "PZEM-017", 18, "middle", "bold")
a(f'<rect x="{px2 - 40}" y="275" width="40" height="200" rx="4" fill="#43a047" stroke="#1b5e20" stroke-width="2"/>')
for lbl, y, *_ in rows:
    screw(px2 - 20, y)
    text(px2 - 50, y + 5, lbl, 15, "end", "bold", "#fff")
text(405, 540, "borne RS485", 12, "middle", fill="#b0bec5")

# ---------- cable ----------
cx1, cx2 = 640, 1060
# short leads PZEM -> cable
for lbl, y, col, st, _ in rows:
    wire(px2, y, cx1, y, col, st)
# sheath
a(f'<rect x="{cx1}" y="265" width="{cx2 - cx1}" height="220" rx="30" fill="#e3f2fd" stroke="#64b5f6" stroke-width="3"/>')
# twisted pairs inside the sheath
wave(cx1 + 10, cx2 - 10, 375, 25, 0, ORANGE, True)       # B (orange/white)
wave(cx1 + 10, cx2 - 10, 375, 25, math.pi, ORANGE, False)  # A (orange)
# brown pair on top/bottom for readability
wire(cx1 + 10, 300, cx2 - 10, 300, BROWN, False)
wire(cx1 + 10, 450, cx2 - 10, 450, BROWN, True)
# ends of the pair inside sheath
wire(cx1, 350, cx1 + 10, 375, ORANGE, True)
wire(cx1, 400, cx1 + 10, 375, ORANGE, False)
wire(cx2 - 10, 375, cx2, 350, ORANGE, True)
wire(cx2 - 10, 375, cx2, 400, ORANGE, False)
# break marks (cable is long)
for x in (835, 865):
    a(f'<path d="M {x - 12} 250 L {x + 12} 500" stroke="#fff" stroke-width="14"/>')
    a(f'<path d="M {x - 12} 250 L {x + 12} 500" stroke="#64b5f6" stroke-width="3"/>')
text(850, 240, "Cabo de rede CAT5 / CAT6 — atravessa o quarto (vários metros OK)", 15, "middle", "bold", "#1565c0")
text(850, 520, "par laranja trançado = A e B   ·   par marrom = 5V e GND", 13, "middle", fill="#555")
text(850, 540, "pares azul e verde: não usados (isolar as pontas)", 13, "middle", fill="#888")

# ---------- USB-RS485 adapter ----------
ax1 = 1180
for lbl, y, col, st, _ in rows:
    wire(cx2, y, ax1, y, col, st)
a(f'<rect x="{ax1 - 4}" y="262" width="48" height="213" rx="4" fill="#43a047" stroke="#1b5e20" stroke-width="2"/>')
adapter_lbl = {"5V": "+5V", "B": "B−", "A": "A+", "GND": "GND"}
for lbl, y, *_ in rows:
    screw(ax1 + 20, y)
    text(ax1 + 20, y - 15, adapter_lbl[lbl], 11, "middle", "bold", "#fff")
a(f'<rect x="{ax1 + 40}" y="330" width="120" height="90" rx="10" fill="#212121"/>')
text(ax1 + 100, 370, "USB-RS485", 13, "middle", "bold", "#fff")
text(ax1 + 100, 390, "(veio com o PZEM)", 11, "middle", fill="#bdbdbd")
a(f'<rect x="{ax1 + 160}" y="355" width="40" height="40" rx="3" fill="#9e9e9e" stroke="#616161" stroke-width="2"/>')
text(ax1 + 100, 445, "na USB do servidor", 12, "middle", fill="#555")

# ---------- HA server ----------
sx1 = 1420
a(f'<path d="M {ax1 + 200} 375 L {sx1} 375" stroke="#424242" stroke-width="6"/>')
a(f'<rect x="{sx1}" y="290" width="190" height="170" rx="12" fill="#03a9f4" stroke="#0277bd" stroke-width="2"/>')
text(sx1 + 95, 345, "Servidor", 16, "middle", "bold", "#fff")
text(sx1 + 95, 367, "Home Assistant", 16, "middle", "bold", "#fff")
text(sx1 + 95, 392, "(HA OS)", 13, "middle", fill="#e1f5fe")
text(sx1 + 95, 430, "integração modbus", 12, "middle", fill="#e1f5fe")

# ---------- legend ----------
ly = 610
text(40, ly, "Ligação (mesma ordem nas duas pontas)", 16, weight="bold")
for i, (lbl, y, col, st, name) in enumerate(rows):
    yy = ly + 30 + i * 30
    wire(40, yy - 5, 110, yy - 5, col, st)
    text(125, yy, f"{name}", 14, weight="bold")
    text(280, yy, f"PZEM {lbl}  →  conversor {adapter_lbl[lbl]}", 14)

nx = 760
notes = [
    "A e B no MESMO par trançado (laranja e laranja/branco): protege do ruído do inversor.",
    "Sem leitura nenhuma? Inverta A e B.",
    "Siga as letras impressas no conversor (A+ = A, B− = B), não a posição dos bornes.",
    "NÃO ligue o cabo de rede em roteador/switch: ele está sendo usado só como fio.",
    "Passe o cabo longe dos cabos grossos de bateria/inversor quando possível.",
    "Não mexa nos bornes do lado das baterias (V+, V−, I): estão ligados direto em 24 V.",
]
text(nx, ly, "Dicas", 16, weight="bold")
for i, n in enumerate(notes):
    text(nx, ly + 30 + i * 26, "• " + n, 14, fill="#333")

a("</svg>")
open(sys.argv[1], "w", encoding="utf-8").write("\n".join(out))
print("ok")
