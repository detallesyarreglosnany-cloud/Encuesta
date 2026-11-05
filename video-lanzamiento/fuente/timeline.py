import json,sys
S=sys.argv[1]; d=json.load(open(f"{S}/vo/durs.json"))
vo={}
def place(k,t): vo[k]=round(t,3); return t+d[k]
T={}
T['lights']=[0.35,0.6,0.85,1.1]; T['title']=1.5; T['subt']=2.3; T['pill']=2.9; T['pillw']=[3.3,3.65,4.0]
e=place('01a',0.7); e=place('01b',e+0.35); T['concept']=vo['01b']+1.0
T['s2']=e+0.15; T['spk']=[]
t=T['s2']
for k in ['02','03','04','05']:
    T['spk'].append(round(t,3)); e=place(k,t+0.25); t=e+0.25
T['grp']=round(t,3); e=place('06a',t+0.3); T['four1']=vo['06a']; T['four2']=vo['06a']+d['06a']*0.52
T['grp2']=e+0.15; e=place('06b',T['grp2']+0.1)
T['big']=[T['grp2']+0.15,T['grp2']+0.4,T['grp2']+0.65]; T['rocket']=T['grp2']+1.6; T['nofuera']=e-1.35
T['s4']=e+0.2; fb={}; fb['title']=T['s4']+0.1; fb['spk']=T['s4']+0.5; fb['cards']=T['s4']+1.1
e=place('07a',T['s4']+0.3); fb['date']=vo['07a']+1.3; fb['tag']=vo['07a']+2.4
e=place('07b',e+0.25); fb['loc']=vo['07b']+0.5
e=place('07c',e+0.2); fb['foot']=vo['07c']+0.3
e=place('07d',e+0.2); fb['cta']=vo['07d']
T['fb']=fb; T['finalSweep']=e-0.3; T['end']=round(e+1.7,3)
T['flash']=[[T['title'],.85],[T['s2'],.6]]+[[x,.35] for x in T['spk'][1:]]+[[T['grp'],.45],[T['grp2'],.9],[T['nofuera'],.35],[T['s4'],.7],[fb['cta'],.35],[T['finalSweep']+.4,.55]]
T['bflash']=[[x,.55] for x in T['lights']]+[[T['title'],.6],[T['grp2'],.6],[T['finalSweep']+.4,.5]]
T['shake']=[[T['title'],16],[T['grp2'],12],[T['nofuera'],8],[T['s4'],8],[fb['cta'],6]]
T['vo']=vo
json.dump(T,open(f"{S}/timeline.json","w"),indent=1)
print(json.dumps(T))
