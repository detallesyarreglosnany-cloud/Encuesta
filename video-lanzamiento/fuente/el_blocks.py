import json,sys,base64,subprocess,urllib.request,numpy as np,soundfile as sf
S=sys.argv[1]; voice=sys.argv[2]; speed=float(sys.argv[3]); stab=float(sys.argv[4]); style=float(sys.argv[5])
BLOCKS=[
 [("hA","Abres temprano, cierras tarde…"),("hB","y las ventas siguen igual."),
  ("hC","¿Y si el problema no eres tú…"),("hD","sino las herramientas que estás usando?"),
  ("01b1","Por eso llega a Puerto Ayacucho la Cumbre de Transformación Empresarial:"),
  ("01b2","un día para darle a tu negocio lo que le falta.")],
 [("02","Con José Rodríguez, aprendes a convertir cada conversación en una venta."),
  ("03","Con Tania Alzuru, descubres qué pasa en la mente de tu cliente… y por qué te elige a ti."),
  ("04","Con Juan Sierra, por fin sabrás a dónde se va tu dinero… y cómo hacer que se quede."),
  ("05","Y con Daniela Silva, tu negocio vende las veinticuatro horas… aunque tú estés durmiendo.")],
 [("06a1","Ventas, clientes, dinero y tecnología:"),("06a2","todo en un solo lugar."),
  ("06b1","La pregunta no es si puedes ir…"),("06b2","es si puedes darte el lujo de no ir.")],
 [("07a","Este viernes cuatro de diciembre,"),("07b","en el Club Parapata, en el corazón de nuestra capital."),
  ("07c","Cierra este año aprendiendo… y empieza el próximo vendiendo más."),("07d","¡Asegura tu entrada!")]]
only=sys.argv[6].split(',') if len(sys.argv)>6 else None
out={}
for bi,blk in enumerate(BLOCKS):
    if only and str(bi) not in only: continue
    text=" ".join(t for _,t in blk)
    body={"text":text,"model_id":"eleven_multilingual_v2","voice_settings":{"stability":stab,"similarity_boost":0.8,"style":style,"use_speaker_boost":True,"speed":speed}}
    if bi>0: body["previous_text"]=" ".join(t for _,t in BLOCKS[bi-1])
    if bi<len(BLOCKS)-1: body["next_text"]=" ".join(t for _,t in BLOCKS[bi+1])
    req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps(body).encode(),headers={"xi-api-key":"proxy-injected","Content-Type":"application/json"})
    r=json.loads(urllib.request.urlopen(req,timeout=180).read())
    mp3=f"{S}/el2/b{bi}.mp3"; open(mp3,"wb").write(base64.b64decode(r["audio_base64"]))
    subprocess.run(["ffmpeg","-v","error","-y","-i",mp3,"-ac","1","-ar","44100",f"{S}/el2/b{bi}.wav"],check=True)
    al=r["alignment"]; st=al["character_start_times_seconds"]; en=al["character_end_times_seconds"]
    pos=0; lines=[]
    for k,t in blk:
        i0=text.index(t,pos); i1=i0+len(t)-1; pos=i1+1
        lines.append((k,st[i0],en[i1]))
    out[bi]={"text":text,"lines":lines,"dur":len(sf.read(f"{S}/el2/b{bi}.wav")[0])/44100}
    print(bi,round(out[bi]['dur'],2),[(k,round(a,2),round(b,2)) for k,a,b in lines])
prev=json.load(open(f"{S}/el2/blocks.json")) if only else {}
prev.update({str(k):v for k,v in out.items()})
json.dump(prev,open(f"{S}/el2/blocks.json","w"),indent=1)
