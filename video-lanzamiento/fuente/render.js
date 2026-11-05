const {chromium}=require('playwright');const fs=require('fs');
const [,,S,mode,a,b,fps]=process.argv; // mode: stills "t1,t2" | frames start end
(async()=>{
 const TL=fs.readFileSync(S+'/timeline.json','utf8');
 const br=await chromium.launch();
 const pg=await br.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
 await pg.addInitScript(`window.TL=${TL}`);
 await pg.goto('file://'+S+'/build/'+(process.env.PAGE||'video.html'));
 await pg.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode&&i.decode()))});
 // preload bg images
 await pg.evaluate(async()=>{for(const s of ['flyer.png','jose.png','tania.png','juan.png','daniela.png','c1.png','c2.png','c3.png','c4.png','c5.png','c6.png','c7.png','c8.png']){const i=new Image();i.src=s;await i.decode()}});
 if(mode==='stills'){
   for(const t of a.split(',').map(Number)){await pg.evaluate(t=>render(t),t);await pg.waitForTimeout(30);
     await pg.screenshot({path:`${S}/stills/s_${t.toFixed(2)}.jpg`,type:'jpeg',quality:80});}
 } else {
   const F=+fps||30; fs.mkdirSync(S+'/frames',{recursive:true});
   for(let f=+a;f<+b;f++){await pg.evaluate(t=>render(t),f/F);
     await pg.screenshot({path:`${S}/frames/f_${String(f).padStart(5,'0')}.jpg`,type:'jpeg',quality:93});}
 }
 await br.close();
})();
