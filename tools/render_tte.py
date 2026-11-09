import re, sys, io, os, contextlib, importlib
import pyfiglet
from PIL import Image, ImageDraw, ImageFont
from terminaltexteffects.utils.graphics import Color

COLS, ROWS = 148, 15
CW, CH = 6, 12
BG = (13, 14, 20)
FONT = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 10, index=0)
FALLBACK = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 10)
NOTDEF = bytes(FONT.getmask('￿'))
SGR = re.compile(r'\x1b\[([0-9;]*)m')

def art_text(name="davin fortune", sub="> technonaut_"):
    art = pyfiglet.figlet_format(name, font="delta_corps_priest_1", width=300).rstrip("\n").split("\n")
    w = max(len(l) for l in art)
    lines = [l.ljust(w) for l in art]
    lines += ["", sub.center(w)]
    pad = (COLS - w) // 2
    return "\n".join(" " * pad + l for l in lines)

def parse(frame):
    cells = []
    fg = (255, 255, 255)
    for r, line in enumerate(frame.split("\n")[:ROWS]):
        c = 0
        pos = 0
        for m in SGR.finditer(line):
            for ch in line[pos:m.start()]:
                if ch != " " and c < COLS: cells.append((c, r, ch, fg))
                c += 1
            codes = m.group(1).split(";")
            if codes[:2] == ["38", "2"] and len(codes) >= 5: fg = tuple(int(x) for x in codes[2:5])
            elif codes in (["0"], [""]): fg = (255, 255, 255)
            pos = m.end()
        for ch in line[pos:]:
            if ch != " " and c < COLS: cells.append((c, r, ch, fg))
            c += 1
    return cells

def draw(cells):
    im = Image.new("RGB", (COLS * CW, ROWS * CH), BG)
    d = ImageDraw.Draw(im)
    for c, r, ch, fg in cells:
        x0, y0 = c * CW, r * CH
        blk = {'█': (0,0,CW,CH), '▄': (0,CH//2,CW,CH), '▀': (0,0,CW,CH//2), '▌': (0,0,CW//2+1,CH), '▐': (CW//2,0,CW,CH)}.get(ch)
        if blk:
            d.rectangle((x0+blk[0], y0+blk[1], x0+blk[2]-1, y0+blk[3]-1), fill=fg); continue
        if ch in '░▒▓':
            a = {'░':.25,'▒':.5,'▓':.75}[ch]
            d.rectangle((x0, y0, x0+CW-1, y0+CH-1), fill=tuple(int(BG[i]+(fg[i]-BG[i])*a) for i in range(3))); continue
        f = FONT if bytes(FONT.getmask(ch)) != NOTDEF else FALLBACK
        d.text((x0, y0), ch, font=f, fill=fg)
    return im

def effect_frames(mod, cls, text, stops):
    M = importlib.import_module(f"terminaltexteffects.effects.effect_{mod}")
    e = getattr(M, cls)(text)
    cfg = e.effect_config
    if hasattr(cfg, "final_gradient_stops"): cfg.final_gradient_stops = tuple(Color(s) for s in stops)
    e.terminal_config.canvas_width = COLS; e.terminal_config.canvas_height = ROWS
    e.terminal_config.frame_rate = 0
    if hasattr(cfg, 'text_gradient_stops'): cfg.text_gradient_stops = tuple(Color(x) for x in stops)
    if hasattr(cfg, 'grid_gradient_stops'): cfg.grid_gradient_stops = (Color('3b4261'), Color('565f89'))
    e.terminal_config.anchor_canvas = 'c'; e.terminal_config.anchor_text = 'c'
    e.terminal_config.ignore_terminal_dimensions = True
    e.terminal_config.wrap_text = False
    e.terminal_config.terminal_background_color = Color("0d0e14")
    out = []
    with contextlib.redirect_stdout(io.StringIO()):
        with e.terminal_output() as t:
            for f in e: out.append(f)
    return out

def pick(frames, n):
    if len(frames) <= n: return frames
    idx = [round(i * (len(frames) - 1) / (n - 1)) for i in range(n)]
    return [frames[i] for i in idx]

if __name__ == "__main__":
    mod, cls, n, outpng = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    fr = effect_frames(mod, cls, art_text(), ("7aa2f7", "bb9af7"))
    print(mod, "raw frames", len(fr))
    sel = pick(fr, n)
    ims = [draw(parse(f)) for f in sel]
    # montage of 4 evenly spaced frames
    ks = [int(len(ims) * x) for x in (0.2, 0.5, 0.8)] + [len(ims) - 1]
    W, H = ims[0].size
    sheet = Image.new("RGB", (W, H * 4))
    for i, k in enumerate(ks): sheet.paste(ims[k], (0, i * H))
    sheet.save(outpng)
