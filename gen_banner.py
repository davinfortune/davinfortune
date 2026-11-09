import random, sys
out = sys.argv[1]
F = {
'D':["11110","10001","10001","10001","10001","10001","11110"],
'A':["01110","10001","10001","11111","10001","10001","10001"],
'V':["10001","10001","10001","10001","10001","01010","00100"],
'I':["11111","00100","00100","00100","00100","00100","11111"],
'N':["10001","11001","10101","10011","10001","10001","10001"],
'F':["11111","10000","10000","11110","10000","10000","10000"],
'O':["01110","10001","10001","10001","10001","10001","01110"],
'R':["11110","10001","10001","11110","10100","10010","10001"],
'T':["11111","00100","00100","00100","00100","00100","00100"],
'U':["10001","10001","10001","10001","10001","10001","01110"],
'C':["01111","10000","10000","10000","10000","10000","01111"],
'H':["10001","10001","10001","11111","10001","10001","10001"],
'E':["11111","10000","10000","11110","10000","10000","11111"],
'L':["10000","10000","10000","10000","10000","10000","11111"],
'P':["11110","10001","10001","11110","10000","10000","10000"],
'>':["10000","01000","00100","00010","00100","01000","10000"],
'_':["00000","00000","00000","00000","00000","00000","11111"],
' ':["000"]*7,
}
W,H = 1200,330
BG,CHROME,BORDER = "#1a1b26","#16161e","#3b4261"
FG,SH,ACC,GRN = "#c0caf5","#bb9af7","#7aa2f7","#9ece6a"
parts=[]
def rect(x,y,w,h,c,extra=""): parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {extra}/>')
def text(s,x,y,px,c):
    cx=x
    for ch in s:
        g=F[ch]; gw=len(g[0])
        for r,row in enumerate(g):
            for k,b in enumerate(row):
                if b=="1": rect(cx+k*px,y+r*px,px,px,c)
        cx+=(gw+1)*px
    return cx
def width(s,px): return sum((len(F[c][0])+1) for c in s)*px-px
# frame
rect(0,0,W,H,BG)
rect(0,0,W,40,CHROME)
for i,c in enumerate(["#f7768e","#e0af68","#9ece6a"]): rect(20+i*28,14,12,12,c)
text_title="~/davinfortune"  # drawn as small pixel text below with limited glyphs
# skyline
random.seed(7)
x=0; base=H-0
while x<W:
    bw=random.choice([40,50,60,70,80]); bh=random.choice([24,40,55,68])
    rect(x,base-bh,bw,bh,"#24283b")
    for wy in range(base-bh+10,base-6,20):
        for wx in range(x+8,x+bw-10,16):
            if random.random()<0.22: rect(wx,wy,8,8,random.choice([GRN,"#e0af68",ACC]))
    x+=bw+random.choice([0,0,10])
# stars
for _ in range(38):
    sx=random.randrange(10,W-10,10); sy=random.randrange(50,150,10)
    rect(sx,sy,random.choice([4,6]),random.choice([4,6]),random.choice(["#565f89","#414868","#7aa2f7"]))
# title with pixel shadow
px=14; t="DAVIN FORTUNE"; tw=width(t,px); tx=(W-tw)//2; ty=75
pass
text(t,tx,ty,px,FG)
# subtitle prompt + blinking cursor
px2=7; s="> TECHNONAUT"; sw=width(s,px2)+px2*2+5*px2
sx0=(W-sw)//2; sy=ty+7*px+34
end=text(s,sx0,sy,px2,GRN)
parts.append(f'<rect x="{end+px2}" y="{sy}" width="{5*px2}" height="{7*px2}" fill="{GRN}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect>')
# border
rect(0,0,W,3,BORDER); rect(0,H-3,W,3,BORDER); rect(0,0,3,H,BORDER); rect(W-3,0,3,H,BORDER); rect(0,40,W,3,BORDER)
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" shape-rendering="crispEdges" role="img" aria-label="Davin Fortune - Technonaut">'+"".join(parts)+'</svg>'
open(out,"w").write(svg); print(len(svg)//1024,"KB")
