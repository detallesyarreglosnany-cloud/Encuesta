# Video de lanzamiento – Cumbre de Transformación Empresarial 2026

| Archivo | Uso |
|---|---|
| `cumbre-transformacion-empresarial-2026.mp4` | Máxima calidad · 1080×1920 · 30 fps · 53 s · Reels / TikTok / Historias |
| `cumbre-whatsapp.mp4` | Versión ligera (~12 MB) para estados y envíos por WhatsApp |

## Voz
Locución con la voz venezolana **Joseph Corona – Clear and Professional** de ElevenLabs (`eleven_multilingual_v2`, velocidad 1,15).
Muestras de otras voces en `muestras-voz/`. Para cambiar de voz:
`python3 fuente/el_full.py <dir> <voice_id> 1.15` → `timeline.py` → render → `music.py` → ffmpeg.

| Voz | voice_id |
|---|---|
| Miguel | STFMZniNPVEtF1Ug6b81 |
| Joseph Corona (usada) | SIpDYvpsUzCaJ0WmnSA8 |
| Andrea | O5hbneAmtjLMgfg5UFIm |
| Valeria | iyvXhCAqzDxKnq3FDjZl |

## Estructura
1. **0–11 s · Apertura:** se encienden 4 luces, el título entra con impacto, «INSPIRA • APRENDE • APLICA» y el concepto «El crecimiento de tu negocio NO PUEDE ESPERAR».
2. **11–34 s · Speakers:** José, Tania, Juan y Daniela entran uno por uno con un barrido de izquierda a derecha, acercamiento de cámara, nombre, especialidad y frase.
3. **34–41 s · Momento emocional:** «4 especialistas / 4 perspectivas», foto grupal con un destello de luz, «CIERRA EL AÑO CON LA MEJOR EXPERIENCIA» y «¡NO TE QUEDES FUERA!».
4. **41–56 s · Cierre:** el folleto se arma por piezas al ritmo de la locución (fecha → lugar → lema → botón COMPRA TU ENTRADA), con un destello final.

## Cómo regenerarlo (`fuente/`)
```
python3 tts.py <dir> ef_dora 1.12   # locución (Kokoro TTS, requiere modelo kokoro-v1.0.onnx + voices-v1.0.bin en <dir>/models)
python3 timeline.py <dir>           # tiempos calculados desde la duración de la voz
node render.js <dir> frames 0 1692 30   # cuadros (Playwright + build/video.html)
python3 music.py <dir>              # música sintetizada + mezcla con ducking
ffmpeg -framerate 30 -i frames/f_%05d.jpg -i mix.wav -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac out.mp4
```
Para cambiar la voz por una locutora venezolana real: graba cada línea con los nombres de `vo/` (01a…07d), reemplaza los `.wav` y vuelve a ejecutar desde `timeline.py`; el video se reajusta solo.

## Versión actual (guion persuasivo)
Guion problema → solución: «Abres temprano, cierras tarde… y las ventas siguen igual», cada speaker presentado como una herramienta
y cierre con FOMO. Voz Joseph (ElevenLabs) generada en 4 bloques continuos (`el_blocks.py`), tiempos en `timeline3.py`,
música compuesta con ElevenLabs Music por secciones (`music.mp3`) y mezcla en `music.py`.
