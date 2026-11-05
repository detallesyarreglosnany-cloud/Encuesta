import json, sys, numpy as np, soundfile as sf
from scipy import signal

S = sys.argv[1]
T = json.load(open(f"{S}/timeline.json"))
SR = 48000
END = T['end']
N = int((END + 0.5) * SR)
rng = np.random.default_rng(7)
tt = np.arange(N) / SR

def z(): return np.zeros(N)
def at(x): return int(x * SR)
def midi(m): return 440 * 2 ** ((m - 69) / 12)

def add(buf, sig, t0, gain=1.0):
    i = at(t0)
    if i >= N: return
    if i < 0: sig = sig[-i:]; i = 0
    n = min(len(sig), N - i)
    buf[i:i + n] += sig[:n] * gain

def lp(x, fc, order=2):
    b, a = signal.butter(order, min(fc, SR / 2 - 100) / (SR / 2), 'low'); return signal.lfilter(b, a, x)
def hp(x, fc, order=2):
    b, a = signal.butter(order, fc / (SR / 2), 'high'); return signal.lfilter(b, a, x)
def bp(x, lo, hi):
    b, a = signal.butter(2, [lo / (SR / 2), hi / (SR / 2)], 'band'); return signal.lfilter(b, a, x)

def saw(f, dur, detune=(0, -0.08, 0.08)):
    t = np.arange(int(dur * SR)) / SR
    out = 0
    for d in detune:
        ff = f * 2 ** (d / 12)
        ph = rng.random()
        out = out + 2 * ((t * ff + ph) % 1) - 1
    return out / len(detune)

def env_adsr(n, a, d, s, r):
    e = np.ones(n) * s
    A, D, R = int(a * SR), int(d * SR), int(r * SR)
    A = min(A, n); e[:A] = np.linspace(0, 1, A)
    D2 = min(D, n - A); e[A:A + D2] = np.linspace(1, s, D2)
    if R > 0 and R < n: e[-R:] *= np.linspace(1, 0, R)
    return e

def reverb(x, secs=2.8, wet=0.35):
    n = int(secs * SR)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * (6.9 / secs))
    ir = lp(ir, 6000); ir /= np.sqrt(np.sum(ir ** 2))
    y = signal.fftconvolve(x, ir)[:len(x)]
    return x * (1 - wet) + y * wet * 1.2

# ---------- grid ----------
G0 = T['s2']; BEAT = 0.5; BAR = 2.0
# chord progression (Dm Bb F C) — roots midi
CH = [[50, 53, 57], [46, 50, 53], [53, 57, 60], [48, 52, 55]]
def chord_at(t):
    k = int(np.floor((t - G0) / BAR)) % 4
    return CH[k]

pad = z(); bass = z(); arp = z(); drums = z(); fx = z(); hits = z()

# ---------- pads (whole piece) ----------
bar_t = G0 - BAR * 6
while bar_t < END:
    ch = chord_at(bar_t + 0.01)
    dur = BAR + 0.6
    sig = 0
    for m in ch + [ch[0] + 12]:
        sig = sig + saw(midi(m), dur)
    sig += 0.6 * saw(midi(ch[0] - 12), dur)
    bright = 900 if bar_t < G0 else (1800 if bar_t < T['grp'] else 3200)
    sig = lp(sig, bright, 2) * env_adsr(len(sig), 0.5, 0.2, 0.9, 0.6)
    lvl = 0.10 if bar_t < G0 else (0.12 if bar_t < T['grp'] else 0.16)
    add(pad, sig, bar_t, lvl)
    bar_t += BAR
# opening swell envelope: silent before lights
pad *= np.clip((tt - 0.3) / 2.5, 0, 1)

# low drone + shimmer for opening
dr = (np.sin(2 * np.pi * midi(38) * tt) + 0.5 * np.sin(2 * np.pi * midi(26) * tt)) * 0.12
dr *= np.clip((tt - 0.3) / 1.5, 0, 1) * np.clip((T['s2'] + 1 - tt) / 1.5, 0, 1)
pad += dr

# ---------- bass pulse (8ths) from s2 ----------
def pluck(f, dur, cutoff=1200, dec=6):
    s = saw(f, dur, (0, 0.05))
    e = np.exp(-np.arange(len(s)) / SR * dec)
    return lp(s, cutoff) * e

t = G0
while t < END - 1.2:
    ch = chord_at(t + 0.01)
    if not (T['grp2'] - 0.6 < t < T['grp2']):  # drop gap before big hit
        add(bass, pluck(midi(ch[0] - 12), 0.24, 500, 10), t, 0.55)
    t += BEAT / 2

# ---------- arp (16ths) ----------
t = G0 + BAR * 2
i = 0
while t < END - 1.2:
    ch = chord_at(t + 0.01)
    notes = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 24]
    if not (T['grp2'] - 0.6 < t < T['grp2']):
        cut = 2500 if t < T['grp'] else 4500
        add(arp, pluck(midi(notes[i % 4]), 0.18, cut, 14), t, 0.10)
    t += BEAT / 4; i += 1

# ---------- drums ----------
def kick(g=1.0):
    n = int(0.45 * SR); t_ = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t_ * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t_ * 7) * g + 0.15 * rng.standard_normal(n) * np.exp(-t_ * 120)
def snare():
    n = int(0.35 * SR); t_ = np.arange(n) / SR
    no = bp(rng.standard_normal(n), 1200, 9000) * np.exp(-t_ * 14)
    return no * 0.8 + 0.4 * np.sin(2 * np.pi * 190 * t_) * np.exp(-t_ * 25)
def hat():
    n = int(0.06 * SR); return hp(rng.standard_normal(n), 8000) * np.exp(-np.arange(n) / SR * 70)
def tom(f):
    n = int(0.5 * SR); t_ = np.arange(n) / SR
    ff = f * (1 + 0.5 * np.exp(-t_ * 20)); return np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-t_ * 6)

b = 0; t = G0
while t < END - 1.5:
    beat_in_bar = b % 4
    inGap = T['grp2'] - 0.6 < t < T['grp2']
    if not inGap:
        if t < T['grp']:
            if beat_in_bar in (0, 2): add(drums, kick(), t, 0.9)
            if t > T['spk'][2] and beat_in_bar in (1, 3): add(drums, snare(), t, 0.35)
            if t > T['spk'][1]: add(drums, hat(), t + BEAT / 2, 0.18)
        elif t < T['s4']:
            add(drums, kick(), t, 1.0)  # four on the floor
            if beat_in_bar in (1, 3): add(drums, snare(), t, 0.45)
            add(drums, hat(), t + BEAT / 2, 0.22); add(drums, hat(), t + BEAT / 4, 0.1)
        else:
            if beat_in_bar == 0: add(drums, kick(1.2), t, 1.0)
            if beat_in_bar == 2: add(drums, kick(), t + 0.25, 0.7)
            if beat_in_bar == 2: add(drums, snare(), t, 0.5)
            add(drums, hat(), t + BEAT / 2, 0.16)
    t += BEAT; b += 1
# tom fill before group (last bar of Daniela) and snare roll riser into big hit
for k in range(8):
    add(drums, tom(110 - k * 7), T['grp'] - 1.0 + k * 0.125, 0.5)
roll_s, roll_e = T['grp2'] - 2.4, T['grp2'] - 0.05
t = roll_s
while t < roll_e:
    p = (t - roll_s) / (roll_e - roll_s)
    add(drums, snare(), t, 0.08 + 0.35 * p)
    t += 0.125 if p < 0.5 else 0.0625

# ---------- FX ----------
def impact(g=1.0, dur=3.0):
    n = int(dur * SR); t_ = np.arange(n) / SR
    f = 30 + 70 * np.exp(-t_ * 8)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t_ * 1.6)
    no = lp(rng.standard_normal(n), 2500) * np.exp(-t_ * 5)
    return (sub * 0.9 + no * 0.5) * g
def whoosh(dur=0.6, g=1.0, up=True):
    n = int(dur * SR); t_ = np.arange(n) / SR; p = t_ / dur
    no = rng.standard_normal(n)
    # sweeping band via short-time filtering
    out = np.zeros(n); seg = 1024
    for s0 in range(0, n, seg):
        pp = p[s0] if up else 1 - p[s0]
        lo = 300 + 4000 * pp; hi = lo * 2.2
        out[s0:s0 + seg] = bp(no[s0:s0 + seg], lo, min(hi, 20000))
    e = np.sin(np.pi * p) ** 2
    return out * e * g
def riser(dur, g=1.0):
    n = int(dur * SR); t_ = np.arange(n) / SR; p = t_ / dur
    f = 200 * 2 ** (p * 3)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.3
    no = hp(rng.standard_normal(n), 2000) * 0.5
    return (tone + no) * p ** 2 * g
def click(g=1.0):
    n = int(0.5 * SR); t_ = np.arange(n) / SR
    return (np.sin(2 * np.pi * 60 * t_) * np.exp(-t_ * 9) + lp(rng.standard_normal(n), 3000) * np.exp(-t_ * 40) * 0.6) * g

for x in T['lights']: add(hits, click(), x, 0.6)
add(hits, impact(1.0, 4), T['title'], 1.0)
add(fx, whoosh(0.7, 0.5), T['title'] - 0.6)
add(fx, riser(1.8, 0.35), T['s2'] - 1.8)
add(hits, impact(0.8), T['s2'], 0.8)
for x in T['spk'][1:]:
    add(fx, whoosh(0.5, 0.55), x - 0.3); add(hits, impact(0.35, 1.5), x, 0.6)
add(fx, whoosh(0.6, 0.6), T['grp'] - 0.35); add(hits, impact(0.5, 2), T['grp'], 0.7)
add(fx, riser(2.4, 0.5), T['grp2'] - 2.4)
add(hits, impact(1.2, 4), T['grp2'], 1.0)
add(hits, impact(0.5, 2), T['nofuera'], 0.6)
add(fx, whoosh(0.6, 0.6), T['s4'] - 0.4); add(hits, impact(0.9, 3), T['s4'], 0.9)
add(hits, impact(0.4, 2), T['fb']['cta'], 0.6)
add(fx, riser(1.2, 0.3), T['finalSweep'] - 0.8)
add(hits, impact(1.2, 5), T['finalSweep'] + 0.4, 1.0)

# final: stop rhythmic parts at the final hit, let pad ring a sustained Dm chord
cut = at(T['finalSweep'] + 0.4)
fade = np.ones(N); fade[cut:] = np.exp(-np.arange(N - cut) / SR * 8)
for buf in (bass, arp, drums):
    buf *= fade
pad *= np.concatenate([np.ones(cut), np.exp(-np.arange(N - cut) / SR * 3)])
final = 0
for m in [38, 50, 53, 57, 62, 65]:
    final = final + saw(midi(m), 3.0)
final = lp(final, 2500) * env_adsr(len(final), 0.02, 0.5, 0.6, 2.0) * 0.08
add(pad, final, T['finalSweep'] + 0.4)

music = reverb(pad, 3.0, 0.45) + reverb(arp, 1.8, 0.3) + bass * 0.9 + reverb(drums, 1.2, 0.15) + reverb(hits, 3.5, 0.35) + reverb(fx, 2.0, 0.3)
music = hp(music, 28)

# ---------- voice ----------
vo = z()
for k, t0 in T['vo'].items():
    a, sr = sf.read(f"{S}/vo/{k}.wav")
    if a.ndim > 1: a = a.mean(1)
    a = signal.resample_poly(a, SR, sr)
    add(vo, a, t0, 1.0)
# voice EQ: slight presence + warmth, light compression
vo = hp(vo, 80)
pres = bp(vo, 2500, 6000); vo = vo + 0.25 * pres
pk = np.max(np.abs(vo)); vo = vo / pk
vo = np.tanh(vo * 1.8) / np.tanh(1.8)
vo = reverb(vo, 0.8, 0.08)

# ducking envelope
act = np.abs(vo)
win = int(0.08 * SR)
envv = signal.lfilter(np.ones(win) / win, 1, act)
envv = np.clip(envv / 0.05, 0, 1)
# smooth attack/release
sm = int(0.15 * SR)
envv = signal.lfilter(np.ones(sm) / sm, 1, envv)
duck = 1 - 0.55 * np.clip(envv, 0, 1)

music = music / np.max(np.abs(music))
mix = music * 0.55 * duck + vo * 0.78
mix = np.tanh(mix * 1.15) / np.tanh(1.15)
mix = mix / np.max(np.abs(mix)) * 0.95
# stereo widen music slightly
L = mix + 0.02 * np.roll(music, 300) * duck
R = mix - 0.02 * np.roll(music, 300) * duck
st = np.stack([L, R], 1)
st = st[:int(END * SR)]
st[-int(0.3 * SR):] *= np.linspace(1, 0, int(0.3 * SR))[:, None]
sf.write(f"{S}/mix.wav", st.astype(np.float32), SR)
sf.write(f"{S}/music_only.wav", (music * 0.8).astype(np.float32)[:int(END * SR)], SR)
print("ok", st.shape[0] / SR)
