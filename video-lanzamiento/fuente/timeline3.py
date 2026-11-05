import json,sys,shutil
S=sys.argv[1]; B=json.load(open(f"{S}/el2/blocks.json"))
L={}
def place(bi,t0):
    for k,a,b in B[str(bi)]['lines']: L[k]=(t0+a,t0+b)
    return t0+B[str(bi)]['dur']
T={'vo':{}}
b0=0.12; T['vo']['b0']=b0; e0=place(0,b0)
T['hk']={k:L[k] for k in ['hA','hB','hC','hD']}
T['teaser']=[0.0,L['hB'][0]-0.05,L['hC'][0]-0.05,L['hD'][0]-0.05]; T['teaserEnd']=L['01b1'][0]-0.05
T['lights']=[T['teaserEnd']+x for x in (0.0,0.08,0.16,0.24)]
T['title']=T['teaserEnd']+0.12; T['subt']=T['title']+0.55; T['pill']=T['title']+0.9
T['pillw']=[T['pill']+0.3,T['pill']+0.55,T['pill']+0.8]; T['concept']=L['01b2'][0]
T['s2']=e0+0.2; b1=T['s2']+0.2; T['vo']['b1']=b1; e1=place(1,b1)
T['spk']=[round(L[k][0]-0.2,3) for k in ['02','03','04','05']]; T['spk'][0]=T['s2']
T['grp']=e1+0.2; b2=T['grp']+0.25; T['vo']['b2']=b2; e2=place(2,b2)
T['four1']=L['06a1'][0]; T['four2']=L['06a2'][0]
T['grp2']=L['06a2'][1]+0.1
T['big']=[L['06b1'][0],L['06b1'][0]+0.35,L['06b1'][0]+0.75]; T['rocket']=T['grp2']+0.4; T['nofuera']=L['06b2'][0]
T['s4']=e2+0.15; b3=T['s4']+0.25; T['vo']['b3']=b3; e3=place(3,b3)
fb={'title':T['s4']+0.1,'spk':T['s4']+0.4,'cards':T['s4']+0.8,'date':L['07a'][0]+0.5,'tag':L['07c'][0]+0.2,
    'loc':L['07b'][0]+0.3,'foot':L['07c'][0]+1.6,'cta':L['07d'][0],'top':L['07c'][0]}
T['fb']=fb; T['finalSweep']=L['07d'][1]+0.4; T['end']=round(L['07d'][1]+2.6,3)
T['flash']=[[0.0,.9]]+[[x,.35] for x in T['teaser'][1:]]+[[T['title'],.85],[T['s2'],.6]]+[[x,.35] for x in T['spk'][1:]]+[[T['grp'],.45],[T['grp2'],.9],[T['nofuera'],.35],[T['s4'],.7],[fb['cta'],.35],[T['finalSweep']+.4,.55]]
T['bflash']=[[x,.55] for x in T['lights']]+[[T['title'],.6],[T['grp2'],.6],[T['finalSweep']+.4,.5]]
T['shake']=[[0.02,14],[L['hD'][0],10],[T['title'],16],[T['grp2'],12],[T['nofuera'],8],[T['s4'],8],[fb['cta'],6]]
T['lines']=L
for bi in range(4): shutil.copy(f"{S}/el2/b{bi}.wav",f"{S}/vo/b{bi}.wav")
json.dump(T,open(f"{S}/timeline.json","w"),indent=1)
print('end',T['end'],'s2',round(T['s2'],2),'spk',T['spk'],'grp',round(T['grp'],2),'grp2',round(T['grp2'],2),'s4',round(T['s4'],2))
