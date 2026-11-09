import sys
from PIL import Image
import render_tte as R
EFFECTS = [("synthgrid","SynthGrid"),("decrypt","Decrypt"),("beams","Beams"),("burn","Burn"),("rain","Rain"),("blackhole","Blackhole")]
N = int(sys.argv[2]); out = sys.argv[1]
only = sys.argv[3].split(",") if len(sys.argv) > 3 else None
text = R.art_text(); frames=[]; durs=[]
for mod, cls in EFFECTS:
    if only and mod not in only: continue
    raw = R.effect_frames(mod, cls, text, ("7aa2f7","bb9af7"))
    sel = R.pick(raw, N)
    ims = [R.draw(R.parse(f)) for f in sel]
    print(mod, len(raw), "->", len(ims), flush=True)
    frames += ims; durs += [50]*len(ims)
    durs[-1] = 2200
# shared palette
step = max(1, len(frames)//12)
sample = frames[::step][:12]
mosaic = Image.new("RGB",(frames[0].width, frames[0].height*len(sample)))
for i,s in enumerate(sample): mosaic.paste(s,(0,i*frames[0].height))
pal = mosaic.quantize(colors=96, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
q[0].save(out, save_all=True, append_images=q[1:], duration=durs, loop=0, optimize=False, disposal=1)
import os; print(out, os.path.getsize(out)//1024, "KB", len(q), "frames", sum(durs)/1000, "s")
