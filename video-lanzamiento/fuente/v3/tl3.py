import json
W=json.load(open('words.json'))
def f(word,after=0,key='s'):
    for x in W:
        if x['w']==word and x['s']>=after: return x[key]
    raise Exception(word)
T={}
T['q']=[W[0]['s'],f('¿Inviertes,'),f('¿Trabajas')]
q3e=f('igual?',key='e')
T['c4']=q3e+0.12; T['shut']=[T['c4']+0.35,T['c4']+0.95]; T['sign']=T['c4']+1.0
T['c5']=T['c4']+1.5; T['flick']=T['c4']+2.05; T['dark']=T['c4']+2.35
T['entonces']=f('Entonces,'); T['esto']=f('¡esto')
T['llega']=f('Llega'); T['puerto']=f('Puerto'); T['empres']=f('empresarios')
T['chips']=[f('acelerar'),f('trabajar'),f('control')]
T['cumbre']=f('La',19); T['undia']=f('un',T['cumbre'])
cons=[x['s'] for x in W if x['w']=='Con']; T['spk']=cons+[f('Y',44)]
T['after']=[f('conocerás'),f('tecnología'),f('aliada')]
T['grp']=f('La',50)-0.15; T['darte']=f('darte')
T['s4']=f('Así'); T['date']=f('4',55); T['loc']=f('Club'); T['ven']=f('ven'); T['cierre']=f('cierre')
T['cta']=f('Compra'); T['end']=round(f('ya.',key='e')+2.0,2)
json.dump(T,open('../timeline.json','w'),indent=1); print(json.dumps(T))
