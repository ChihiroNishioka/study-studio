#!/usr/bin/env python3
"""StudyStudio template renderer: spec.json -> mp4 (no LLM). usage: render.py spec.json out.mp4"""
import json,sys,math,subprocess
from multiprocessing import Pool
from PIL import Image,ImageDraw,ImageFont
W,H,FPS,S=1080,1920,30,1
FB='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
_f={}
def F(z):
    k=max(1,int(z))
    if k not in _f:_f[k]=ImageFont.truetype(FB,k,index=0)
    return _f[k]
BG=(222,238,250);NAV=(18,32,70);INK=NAV;WHT=(255,255,255);GRY=(150,170,195)
COL={'r':(235,55,60),'b':(30,110,230),'g':(20,160,100),'o':(255,120,40),'a':(250,170,0)}
STEPC=[COL['r'],COL['b'],COL['g']];YEL=(255,214,0)
cl=lambda x:max(0,min(1,x))
def ease(x):x=cl(x);return x*x*(3-2*x)
def pr(t,a,d=.5):return ease((t-a)/d)
def parse(s,col):
    runs=[];i=0;cur=col
    while i<len(s):
        if s[i]=='<':
            j=s.index('>',i);tag=s[i+1:j];i=j+1;cur=col if tag=='' else COL[tag];continue
        if s[i]=='_':
            if s[i+1]=='{':j=s.index('}',i);txt=s[i+2:j];i=j+1
            else:txt=s[i+1];i+=2
            runs.append((txt,1,cur));continue
        runs.append((s[i],0,cur));i+=1
    return runs
def width(s,sz):return sum(F(sz*(.62 if sub else 1)).getlength(c) for c,sub,_ in parse(s,INK))
def rich(d,s,cx,cy,sz,col=INK,a=1):
    if a<=.02:return
    x=cx-width(s,sz)/2
    for c,sub,cc in parse(s,col):
        z=sz*(.62 if sub else 1);d.text((x,cy+(sz*.26 if sub else 0)),c,font=F(z),fill=tuple(cc)+(int(255*a),),anchor='lm');x+=F(z).getlength(c)
def card(d,b,a=1,fill=WHT,out=INK,r=30):
    d.rounded_rectangle(b,radius=r,fill=tuple(fill)+(int(255*a),),outline=tuple(out)+(int(255*a),),width=4)
def fit(lines,maxw=900,sz=62):
    while sz>24 and max(width(l,sz) for l in lines)>maxw:sz-=2
    return sz
# ---- geometry shared with checker
FIG=(60,420,1020,1000)   # figure area
FORM_Y=1180;CAP_Y=1440;SAFE=(40,40,1040,1880)
def timeline(sp):
    t=0;segs=[('intro',0,sp['intro_seconds'])];t=sp['intro_seconds']
    for i,s in enumerate(sp['steps']):segs.append(('step%d'%i,t,t+s['seconds']));t+=s['seconds']
    return segs
def total(sp):return sum(b-a for _,a,b in timeline(sp)[:1])+sum(s['seconds'] for s in sp['steps'])
# ---- components
def c_text(d,s,y,sz,t0,t,col=INK):
    rich(d,s,540,y,fit([s],940,sz),col,pr(t,t0,.4))
def c_figure(im,d,fig,t,t0,col):
    ty=fig['type'];x0,y0,x1,y1=FIG;a=pr(t,t0,.4)
    card(d,FIG,a,(235,246,255),NAV,24);lt=t-t0
    if ty=='wave':
        cy=(y0+y1)//2;sp=fig.get('speed',72);xs=600+sp*.4*lt;xo=170
        lay=Image.new('RGBA',(W,H),(0,0,0,0));ld=ImageDraw.Draw(lay)
        T=.45
        for n in range(int(lt/T)+1):
            age=lt-n*T
            if 0<=age<4.4:
                r=190*age;cx=820-sp*(n*T)*.4-0 ;cx=600+sp*.4*(n*T)
                al=(1-age/4.4)**.8
                if r>3:ld.ellipse([cx-r,cy-r,cx+r,cy+r],outline=COL['o']+(int(255*al*.9),),width=6)
        mask=Image.new('L',(W,H),0);ImageDraw.Draw(mask).rounded_rectangle(FIG,24,fill=255)
        im.paste(lay,(0,0),Image.composite(lay.split()[3],Image.new('L',(W,H),0),mask))
        d=ImageDraw.Draw(im,'RGBA')
        d.ellipse([xo-34,cy-110,xo+34,cy-42],fill=INK);d.rounded_rectangle([xo-46,cy-36,xo+46,cy+80],radius=30,fill=INK)
        d.pieslice([xs-36,cy-60,xs+36,cy+12],180,360,fill=COL['r']);d.rounded_rectangle([xs-52,cy+10,xs+52,cy+55],radius=10,fill=INK)
        card(d,(330,y0+20,750,y0+76),1,NAV,NAV,26);rich(d,fig.get('label',''),540,y0+48,38,WHT)
        d.text((xo,cy+110),'観測者',font=F(34),fill=INK+(255,),anchor='mm');d.text((xs,cy+85),'音源',font=F(34),fill=INK+(255,),anchor='mm')
        arrow(d,(xs+60,cy-100),(xs+160,cy-100),COL['b']) if False else None
    elif ty=='point':
        mn,mx=fig['min'],fig['max'];lx0,lx1=140,940;cy=(y0+y1)//2
        px=lambda v:lx0+(v-mn)/(mx-mn)*(lx1-lx0)
        d.line([lx0,cy,lx1,cy],fill=INK+(255,),width=8)
        n=8
        for i in range(n+1):
            v=mn+(mx-mn)*i/n;x=px(v);d.line([x,cy-14,x,cy+14],fill=INK+(255,),width=4)
            d.text((x,cy+44),('%g'%v),font=F(32),fill=INK+(255,),anchor='mm')
        v=fig['from']+(fig['to']-fig['from'])*ease(lt/2.5);x=px(v)
        d.ellipse([x-24,cy-24,x+24,cy+24],fill=col+(255,),outline=WHT+(255,),width=4)
        rich(d,'%s ＝ %g'%(fig.get('label',''),round(v,1)),x,cy-80,44,col)
    elif ty=='graph':
        gx0,gy0,gx1,gy1=140,y0+50,980,y1-70
        X=lambda v:gx0+(v-fig['xmin'])/(fig['xmax']-fig['xmin'])*(gx1-gx0)
        Y=lambda v:gy1-(v-fig['ymin'])/(fig['ymax']-fig['ymin'])*(gy1-gy0)
        d.line([gx0,gy1,gx1,gy1],fill=INK+(255,),width=5);d.line([gx0,gy0,gx0,gy1],fill=INK+(255,),width=5)
        for v in range(int(fig['xmin']),int(fig['xmax'])+1):
            d.text((X(v),gy1+30),str(v),font=F(30),fill=INK+(255,),anchor='mm')
        for v in range(int(fig['ymin']),int(fig['ymax'])+1,2):
            d.text((gx0-30,Y(v)),str(v),font=F(30),fill=INK+(255,),anchor='mm')
        p=ease(lt/2.0)
        for ln in fig['lines']:
            c=COL[ln.get('color','b')];xa=fig['xmin'];xb=xa+(fig['xmax']-xa)*p
            pts=[(X(xa+(xb-xa)*i/40),Y(ln['a']*(xa+(xb-xa)*i/40)+ln['b'])) for i in range(41)]
            d.line(pts,fill=c+(255,),width=8)
            if p>.9:rich(d,ln.get('label',''),X(fig['xmax'])-130,Y(ln['a']*fig['xmax']+ln['b'])+(-40 if ln['a']>0 else -40),34,c)
        if 'mark' in fig and lt>2.2:
            mx_,my_=fig['mark'];r=18+4*math.sin(lt*8)
            d.ellipse([X(mx_)-r,Y(my_)-r,X(mx_)+r,Y(my_)+r],fill=YEL+(255,),outline=INK+(255,),width=4)
def station(d,cur,t,t0):
    names=['①','②','③']
    for i in range(3):
        x=240+i*300;on=(i==cur);c=STEPC[i]
        if on:
            d.rounded_rectangle([x-125,265,x+125,395],radius=22,outline=YEL+(255,),width=8)
            d.text((x,252),'▶ いまここ',font=F(30),fill=INK+(255,),anchor='mm') if False else None
        d.ellipse([x-38,282,x+38,358],fill=c+(255,));d.text((x,320),names[i],font=F(46),fill=WHT+(255,),anchor='mm')
        if i<2:d.line([x+45,320,x+255,320],fill=GRY+(255,),width=6)
    return
def frame(args):
    sp,n=args;t=n/FPS;segs=timeline(sp)
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im,'RGBA')
    for x in range(0,W,60):d.line([x,260,x,H],fill=(210,228,243),width=1)
    for y in range(260,H,60):d.line([0,y,W,y],fill=(210,228,243),width=1)
    d.rectangle([0,0,W,250],fill=NAV)
    rich(d,sp['title'],540,95,fit([sp['title']],980,52),WHT);rich(d,sp.get('subtitle',''),540,160,40,WHT[:3] and (190,215,245))
    for k,(name,a,b) in enumerate(segs):
        if not a<=t<b+(1e-9 if k==len(segs)-1 else 0):continue
        if name=='intro':
            card(d,(60,420,1020,1000),pr(t,a,.4),WHT,NAV,30)
            for j,l in enumerate(sp['problem'].split('／')):rich(d,l,540,540+j*110,fit([l],860,60),INK,pr(t,a+.2+.2*j,.4))
            cap=None;acc=COL['o'];idx=0
        elif name.startswith('step'):
            i=int(name[4]);s=sp['steps'][i];acc=STEPC[i];station(d,i,t,a)
            if 'figure' in s:c_figure(im,d,s['figure'],t,a,acc);d=ImageDraw.Draw(im,'RGBA')
            card(d,(60,1090,1020,1280),pr(t,a+.3,.4),WHT,acc,30)
            rich(d,s['heading'],540,1125,40,acc,pr(t,a+.3,.4))
            c_text(d,s['formula'],1210,66,a+.5,t,INK)
            cap=s['caption']
        if cap:
            ls=cap.split('／');sz=fit(ls,900,58);h=int(len(ls)*sz*1.5+50);al=pr(t,a+.1,.3)*(1-pr(t,b-.2,.2))
            y0=CAP_Y+int((1-pr(t,a+.1,.3))*25);card(d,(60,y0,1020,y0+h),al,NAV,NAV,34)
            d.rounded_rectangle([60,y0+h-14,60+960*pr(t,a,.8),y0+h],radius=7,fill=acc+(int(255*al),))
            for j,l in enumerate(ls):rich(d,l,540,y0+25+sz*.75+j*sz*1.5,sz,WHT,al)
    for k in range(len(segs)):
        on=segs[k][1]<=t<segs[k][2];x=540+(k-(len(segs)-1)/2)*46;r=11 if on else 7
        d.ellipse([x-r,1850-r,x+r,1850+r],fill=(COL['a'] if on else GRY)+(255,))
    return im.tobytes()
def render(spec,out):
    sp=json.load(open(spec));tot=total(sp);assert abs(tot-30)<1e-6,'total seconds must be 30 (got %s)'%tot
    N=int(tot*FPS)
    ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','%dx%d'%(W,H),'-r',str(FPS),'-i','-','-f','lavfi','-i','anullsrc=r=44100:cl=mono','-shortest','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-t',str(tot),out],stdin=subprocess.PIPE)
    with Pool() as p:
        for b in p.imap(frame,[(sp,n) for n in range(N)],chunksize=8):ff.stdin.write(b)
    ff.stdin.close();ff.wait()
if __name__=='__main__':render(sys.argv[1],sys.argv[2])
