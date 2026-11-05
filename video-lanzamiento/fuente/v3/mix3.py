import json,subprocess,numpy as np,soundfile as sf
from scipy import signal
S='/tmp/claude-0/-home-user-Encuesta/c170e499-24d9-54ff-b669-69ea4d3e1cd2/scratchpad'; V=S+'/v3'
T=json.load(open(f'{S}/timeline.json')); SR=48000; N=int(T['end']*SR); rng=np.random.default_rng(3)
def z(): return np.zeros(N)
def add(b,s,t0,g=1.0):
    i=int(t0*SR); n=min(len(s),N-i)
    if n>0: b[i:i+n]+=s[:n]*g
def bp(x,lo,hi): b,a=signal.butter(2,[lo/(SR/2),hi/(SR/2)],'band'); return signal.lfilter(b,a,x)
def lp(x,f): b,a=signal.butter(2,f/(SR/2),'low'); return signal.lfilter(b,a,x)
def hp(x,f): b,a=signal.butter(2,f/(SR/2),'high'); return signal.lfilter(b,a,x)
def rev(x,secs=1.5,wet=.25):
    n=int(secs*SR); ir=rng.standard_normal(n)*np.exp(-np.arange(n)/SR*(6.9/secs)); ir=lp(ir,5000); ir/=np.sqrt((ir**2).sum())
    return x*(1-wet)+signal.fftconvolve(x,ir)[:len(x)]*wet
tt=lambda d:np.arange(int(d*SR))/SR
# --- music
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{V}/music.mp3','-ac','1','-ar',str(SR),f'{V}/music.wav'],check=True)
m,_=sf.read(f'{V}/music.wav'); mus=z(); n=min(len(m),N); mus[:n]=m[:n]; mus/=np.max(np.abs(mus))
# dramatic drop at lights-off, swell back on "esto es para ti"/"Llega"
g=np.ones(N); t=np.arange(N)/SR
dip=(t>T['flick']-.1)&(t<T['llega'])
g[dip]=np.clip(1-(t[dip]-(T['flick']-.1))/0.35,0.06,1)
sw=(t>=T['esto'])&(t<T['llega']+.3); g[sw]=np.maximum(g[sw],0.06+0.94*((t[sw]-T['esto'])/(T['llega']+.3-T['esto']))**2)
mus*=g
# --- sfx
sfx=z()
d=T['shut'][1]-T['shut'][0]; tr=tt(d+.05)
rat=bp(rng.standard_normal(len(tr)),300,4000)*(0.5+0.5*np.sign(np.sin(2*np.pi*38*tr)))*np.linspace(.5,1,len(tr))
add(sfx,rat,T['shut'][0],.5)
slam=tt(.6); add(sfx,(np.sin(2*np.pi*70*slam)*np.exp(-slam*12)+lp(rng.standard_normal(len(slam)),2500)*np.exp(-slam*25)*.8),T['shut'][1],.9)
th=tt(.3); add(sfx,lp(rng.standard_normal(len(th)),1200)*np.exp(-th*30),T['sign'],.5)
for k,dt in enumerate([0,.05,.1,.15,.2,.25]):
    c=tt(.03); add(sfx,hp(rng.standard_normal(len(c)),2000)*np.exp(-c*150),T['flick']+dt,.25)
c=tt(.25); add(sfx,(hp(rng.standard_normal(len(c)),1500)*np.exp(-c*80)+np.sin(2*np.pi*90*c)*np.exp(-c*30)),T['dark'],.6)
r=tt(1.2); f=300*2**(r/1.2*2.5); add(sfx,(hp(rng.standard_normal(len(r)),3000)*.4+np.sin(2*np.pi*np.cumsum(f)/SR)*.15)*(r/1.2)**2,T['llega']-1.2,.35)
def whoosh(dur=.5):
    r=tt(dur); x=rng.standard_normal(len(r)); out=np.zeros(len(r)); seg=1024
    for s0 in range(0,len(r),seg): p=r[s0]/dur; lo=400+3500*p; out[s0:s0+seg]=bp(x[s0:s0+seg],lo,min(lo*2,20000))
    return out*np.sin(np.pi*r/dur)**2
for x in [T['q'][1],T['q'][2]]+T['spk']+T['after'][1:]+[T['grp'],T['s4']]: add(sfx,whoosh(.45),x-.2,.18)
im=tt(2.5); add(sfx,np.sin(2*np.pi*np.cumsum(32+50*np.exp(-im*7))/SR)*np.exp(-im*2),T['cumbre'],.35)
sfx=rev(sfx,1.4,.25)
# --- voice (keep natural)
v,sr=sf.read(f'{V}/voz_edit.wav'); 
if v.ndim>1: v=v.mean(1)
vo=z(); add(vo,v,0.0); vo=hp(vo,70); vo=vo/np.max(np.abs(vo))
env=signal.lfilter(np.ones(int(.1*SR))/int(.1*SR),1,np.abs(vo)); env=np.clip(env/0.05,0,1); env=signal.lfilter(np.ones(int(.3*SR))/int(.3*SR),1,env)
duck=1-0.35*env
import os
MG=0.0 if os.environ.get("NOMUSIC") else 0.42
mix=mus*MG*duck+sfx*0.5+vo*0.95
mix=np.tanh(mix*1.05)/np.tanh(1.05); mix=mix/np.max(np.abs(mix))*.95
mix[-int(.4*SR):]*=np.linspace(1,0,int(.4*SR))
sf.write(f'{S}/mix.wav',np.stack([mix,mix],1).astype(np.float32),SR); print('ok',N/SR)
