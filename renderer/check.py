#!/usr/bin/env python3
"""usage: check.py spec.json video.mp4 -> OK/NG (overflow, safe area, 30s, 1080x1920)"""
import sys,json,subprocess
from render import *
def main(spec,mp4):
    sp=json.load(open(spec));ng=[]
    mx=SAFE[2]-SAFE[0]
    texts=[('title',sp['title'],980,52),('problem',sp['problem'],0,0)]
    for l in sp['problem'].split('／'):
        if width(l,24)>860:ng.append('problem line too long: '+l)
    if abs(total(sp)-30)>1e-6:ng.append('spec seconds != 30')
    for i,s in enumerate(sp['steps']):
        ls=s['caption'].split('／')
        if len(ls)>2:ng.append('step%d caption >2 lines'%(i+1))
        sz=fit(ls,900,58)
        if sz<40:ng.append('step%d caption too small font %d'%(i+1,sz))
        h=len(ls)*sz*1.5+50
        if CAP_Y+h>SAFE[3]-60:ng.append('step%d caption outside safe area'%(i+1))
        if width(s['formula'],66)>940 and fit([s['formula']],940,66)<44:ng.append('step%d formula overflow'%(i+1))
        if width(s['heading'],40)>900:ng.append('step%d heading overflow'%(i+1))
    if 'check' in sp:ng.append('check segment present (類題は廃止)')
    if not (SAFE[0]<=FIG[0] and FIG[2]<=SAFE[2] and FIG[3]<=SAFE[3]):ng.append('figure outside safe area')
    r=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-show_entries','format=duration','-of','json',mp4],capture_output=True,text=True)
    j=json.loads(r.stdout);w,h=j['streams'][0]['width'],j['streams'][0]['height'];dur=float(j['format']['duration'])
    if (w,h)!=(1080,1920):ng.append('resolution %dx%d'%(w,h))
    if abs(dur-30)>0.1:ng.append('duration %.2f'%dur)
    print(('NG: '+'; '.join(ng)) if ng else 'OK  %dx%d %.2fs'%(w,h,dur));sys.exit(1 if ng else 0)
main(sys.argv[1],sys.argv[2])
