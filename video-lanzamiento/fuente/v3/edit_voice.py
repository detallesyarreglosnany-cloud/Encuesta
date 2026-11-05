import json,numpy as np,soundfile as sf
d=json.load(open('stt.json')); W=[x for x in d['words'] if x['type']=='word']
a,sr=sf.read('voz.wav')
BEAT_BEFORE='Entonces,'; BEAT=2.6; HEAD=0.15
segs=[]; out=[]; t_new=HEAD; cur=max(0,W[0]['start']-0.05)
newW=[]
# build list of cut points at gaps
starts=[cur]; 
pieces=[]  # (src_a, src_b)
i0=0
for i in range(1,len(W)+1):
    if i==len(W) or (W[i]['start']-W[i-1]['end'])>0.3:
        a0=W[i0]['start']-0.08 if i0>0 else cur
        b0=W[i-1]['end']+0.10 if i<len(W) else min(len(a)/sr,W[-1]['end']+0.35)
        pieces.append((a0,b0,i0,i))
        i0=i
buf=[np.zeros(int(HEAD*sr))]; t=HEAD
for k,(a0,b0,i0,i1) in enumerate(pieces):
    if k>0:
        gap = BEAT if W[i0]['text']==BEAT_BEFORE else 0.06
        buf.append(np.zeros(int(gap*sr))); t+=gap
    seg=a[int(a0*sr):int(b0*sr)].copy(); f=int(.01*sr); seg[:f]*=np.linspace(0,1,f); seg[-f:]*=np.linspace(1,0,f)
    for j in range(i0,i1): newW.append({'w':W[j]['text'],'s':round(t+W[j]['start']-a0,3),'e':round(t+W[j]['end']-a0,3)})
    buf.append(seg); t+=len(seg)/sr
v=np.concatenate(buf); sf.write('voz_edit.wav',v,sr)
json.dump(newW,open('words.json','w'),ensure_ascii=False,indent=0)
print('dur',round(len(v)/sr,2),'pieces',len(pieces))
for x in newW:
    if x['w'] in ('¿Inviertes,','¿Trabajas','igual?','Entonces,','Llega','La','Con','Y','pregunta','Así','Compra','ya.','acelerar','trabajar','control','tecnología','aliada','veinticuatro','conocerás','ven','Club','4'): print(x)
