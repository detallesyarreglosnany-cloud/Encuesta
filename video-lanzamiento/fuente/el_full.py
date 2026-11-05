import json,sys,subprocess,numpy as np,soundfile as sf
sys.path.insert(0,sys.argv[1]); from el_tts import tts
S=sys.argv[1]; voice=sys.argv[2]; speed=float(sys.argv[3])
import el_tts
L=[("01a","¿Y si este fuera el impulso que tu negocio necesita para llegar al siguiente nivel?"),
 ("01b","Llega a Puerto Ayacucho una experiencia para empresarios que quieren crecer, innovar y transformar sus resultados."),
 ("02","Aprende a vender mejor, conectar con tus clientes y liderar con estrategia."),
 ("03","Descubre cómo piensa tu consumidor, y convierte tu emprendimiento en una empresa con visión."),
 ("04","Aprende a tomar decisiones financieras inteligentes, y a convertir tus números en resultados."),
 ("05","Descubre cómo la tecnología, la automatización y las herramientas digitales pueden llevar tu negocio más lejos."),
 ("06a","Cuatro especialistas. Cuatro perspectivas."),
 ("06b","Una experiencia diseñada para transformar tu manera de hacer negocios. ¡No te quedes fuera!"),
 ("07a","Este viernes cuatro de diciembre, tienes una cita con el futuro de tu negocio."),
 ("07b","Nos vemos en el Club Parapata, en Puerto Ayacucho."),
 ("07c","Prepárate para inspirarte, aprender y aplicar."),
 ("07d","¡Asegura tu entrada, y sé parte de esta transformación!")]
import urllib.request
orig=el_tts.tts
d={}
for i,(k,t) in enumerate(L):
    prev=L[i-1][1] if i else None; nxt=L[i+1][1] if i+1<len(L) else None
    body={"text":t,"model_id":"eleven_multilingual_v2","voice_settings":{"stability":0.45,"similarity_boost":0.8,"style":0.35,"use_speaker_boost":True,"speed":speed}}
    if prev: body["previous_text"]=prev
    if nxt: body["next_text"]=nxt
    req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128",data=json.dumps(body).encode(),headers={"xi-api-key":"proxy-injected","Content-Type":"application/json"})
    open(f"{S}/el/{k}.mp3","wb").write(urllib.request.urlopen(req,timeout=120).read())
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"{S}/el/{k}.mp3","-ac","1","-ar","44100",f"{S}/el/{k}.wav"],check=True)
    a,sr=sf.read(f"{S}/el/{k}.wav")
    idx=np.where(np.abs(a)>0.012)[0]; a=a[max(idx[0]-300,0):idx[-1]+int(.12*sr)]
    a[:200]*=np.linspace(0,1,200); a[-800:]*=np.linspace(1,0,800)
    # cap internal pauses at 0.32 s
    w=int(.02*sr); n=len(a)//w; e=np.array([np.sqrt(np.mean(a[i*w:(i+1)*w]**2)) for i in range(n)])
    keep=np.ones(len(a),bool); c=0
    for i in range(n+1):
        if i<n and e[i]<0.006: c+=1; continue
        if c*0.02>0.32:
            st=(i-c)*w+int(.16*sr); en=i*w-int(.16*sr); keep[st:en]=False
        c=0
    a=a[keep]
    sf.write(f"{S}/vo/{k}.wav",a,sr); d[k]=round(len(a)/sr,3)
json.dump(d,open(f"{S}/vo/durs.json","w")); print(d, sum(d.values()))
