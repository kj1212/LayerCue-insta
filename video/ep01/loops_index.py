#!/usr/bin/env python3
"""GarageBand 의 Apple Loops(.caf) 에서 템포·키·박자 수·분류를 읽어 ep01/audio/loops.json 으로 — 같은 「곡 묶음」(이름 앞부분)끼리 모은다.
CAF 의 'info' 덩어리(문자열 키-값)와 'uuid' 덩어리의 속성을 읽는다. 받은 음원 없이 이 맥의 루프만 쓴다(사용권: GarageBand 사용권 — 자기 영상의 배경음으로 로열티 없이 사용 가능).
"""
import struct, json, pathlib, re, plistlib, sys
ROOT = pathlib.Path("/Library/Audio/Apple Loops/Apple")

def chunks(b):
    i = 8
    while i + 12 <= len(b):
        t = b[i:i+4].decode("latin1"); n = struct.unpack(">q", b[i+4:i+12])[0]
        if n < 0: n = len(b) - i - 12
        yield t, b[i+12:i+12+n]; i += 12 + n

def meta(path):
    b = path.read_bytes(); out = {}
    for t, d in chunks(b):
        if t == "info":
            k = d[4:].split(b"\x00")
            for a, v in zip(k[0::2], k[1::2]):
                try: out[a.decode()] = v.decode()
                except Exception: pass
        elif t == "uuid":
            body = d[16:]
            j = body.find(b"<?xml")
            if j >= 0:
                try: out.update({("u_" + k): v for k, v in plistlib.loads(body[j:]).items() if isinstance(v, (str, int, float))})
                except Exception: pass
            else:
                for m in re.finditer(rb"([a-zA-Z ]{3,24})\x00([^\x00]{1,40})\x00", body):
                    try: out["u_" + m.group(1).decode()] = m.group(2).decode()
                    except Exception: pass
    return out

rows = []
for p in sorted(ROOT.rglob("*.caf")):
    try: m = meta(p)
    except Exception as e: m = {"err": str(e)}
    rows.append({"pack": p.parent.name, "name": p.stem, "path": str(p), **m})
out = pathlib.Path("ep01/audio/loops.json"); out.parent.mkdir(parents=True, exist_ok=True)
json.dump(rows, open(out, "w"), indent=1, ensure_ascii=False)
keys = {}
for r in rows:
    for k in r: keys[k] = keys.get(k, 0) + 1
print(len(rows), "loops; keys:", {k: v for k, v in keys.items() if k not in ("pack", "name", "path")})
print(json.dumps(rows[0], ensure_ascii=False)[:600])
