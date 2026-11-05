import sys, json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
S=sys.argv[1]
k=Kokoro(f"{S}/models/kokoro.onnx", f"{S}/models/voices.bin")
lines={
 "01a":"¿Y si este fuera el impulso que tu negocio necesita para llegar al siguiente nivel?",
 "01b":"Llega a Puerto Ayacucho una experiencia para empresarios que quieren crecer, innovar y transformar sus resultados.",
 "02":"Aprende a vender mejor, conectar con tus clientes y liderar con estrategia.",
 "03":"Descubre cómo piensa tu consumidor, y convierte tu emprendimiento en una empresa con visión.",
 "04":"Aprende a tomar decisiones financieras inteligentes, y a convertir tus números en resultados.",
 "05":"Descubre cómo la tecnología, la automatización y las herramientas digitales pueden llevar tu negocio más lejos.",
 "06a":"Cuatro especialistas. Cuatro perspectivas.",
 "06b":"Una experiencia diseñada para transformar tu manera de hacer negocios. ¡No te quedes fuera!",
 "07a":"Este viernes cuatro de diciembre, tienes una cita con el futuro de tu negocio.",
 "07b":"Nos vemos en el Club Parapata, en Puerto Ayacucho.",
 "07c":"Prepárate para inspirarte, aprender y aplicar.",
 "07d":"¡Asegura tu entrada, y sé parte de esta transformación!",
}
out={}
for key,t in lines.items():
    a,sr=k.create(t, voice=sys.argv[2], speed=float(sys.argv[3]), lang="es")
    # trim silence
    th=0.01; idx=np.where(np.abs(a)>th)[0]; a=a[max(idx[0]-200,0):idx[-1]+1200]
    sf.write(f"{S}/vo/{key}.wav",a,sr); out[key]=round(len(a)/sr,3)
print(json.dumps(out)); print(sum(out.values()))
json.dump(out,open(f"{S}/vo/durs.json","w"))
