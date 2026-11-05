import json,sys,urllib.request
def tts(voice,text,out,prev=None,nxt=None,model="eleven_multilingual_v2",stab=0.45,style=0.35):
    body={"text":text,"model_id":model,"voice_settings":{"stability":stab,"similarity_boost":0.8,"style":style,"use_speaker_boost":True}}
    if prev: body["previous_text"]=prev
    if nxt: body["next_text"]=nxt
    req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128",data=json.dumps(body).encode(),
        headers={"xi-api-key":"proxy-injected","Content-Type":"application/json"})
    try:
        open(out,"wb").write(urllib.request.urlopen(req,timeout=120).read()); return True
    except urllib.error.HTTPError as e:
        print("ERR",voice,e.code,e.read()[:300]); return False
if __name__=="__main__":
    voices={"miguel":"STFMZniNPVEtF1Ug6b81","andrea":"O5hbneAmtjLMgfg5UFIm","valeria":"iyvXhCAqzDxKnq3FDjZl","joseph":"SIpDYvpsUzCaJ0WmnSA8"}
    t="¿Y si este fuera el impulso que tu negocio necesita para llegar al siguiente nivel? Llega a Puerto Ayacucho una experiencia para empresarios que quieren crecer, innovar y transformar sus resultados."
    for k,v in voices.items():
        if tts(v,t,f"muestra_{k}.mp3"): print("ok",k)
