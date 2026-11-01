#!/private/tmp/claude-501/-Users-kj1212-projects-LayerCue-insta/40ec29a8-ed28-44bf-b3e5-52d2d8c01868/scratchpad/venv/bin/python
"""창 그림의 글자를 애플 Vision 으로 읽어 [글자, x, y, w, h](그림 픽셀, 왼쪽 위 기준) 목록을 낸다 — 영역(regions.json)을 눈대중 대신 실측으로.

    ep01/ocr.py <png> [찾을 글자 …]      → 전부(또는 그 글자가 든 것만) 출력, JSON 은 <png>.ocr.json
"""
import sys, json
import Vision, Quartz, Foundation

def ocr(path):
    src = Quartz.CGImageSourceCreateWithURL(Foundation.NSURL.fileURLWithPath_(path), None)
    img = Quartz.CGImageSourceCreateImageAtIndex(src, 0, None)
    W, H = Quartz.CGImageGetWidth(img), Quartz.CGImageGetHeight(img)
    req = Vision.VNRecognizeTextRequest.alloc().init()
    req.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    req.setUsesLanguageCorrection_(False)
    h = Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(img, None)
    h.performRequests_error_([req], None)
    out = []
    for o in req.results() or []:
        c = o.topCandidates_(1)[0]; text = str(c.string())
        # 줄 전체 상자 — 정규화 좌표(왼쪽 아래 기준) → 픽셀(왼쪽 위 기준)
        bb = o.boundingBox()
        x, y, w, hh = bb.origin.x * W, (1 - bb.origin.y - bb.size.height) * H, bb.size.width * W, bb.size.height * H
        out.append([text, round(x), round(y), round(w), round(hh)])
        # 낱말마다 상자도(여러 낱말 줄일 때)
        words = text.split(" ")
        if len(words) > 1:
            pos = 0
            for wd in words:
                i = text.find(wd, pos); pos = i + len(wd)
                r, err = c.boundingBoxForRange_error_(Foundation.NSMakeRange(i, len(wd)), None)
                if r is None: continue
                b = r.boundingBox()
                out.append(["·" + wd, round(b.origin.x * W), round((1 - b.origin.y - b.size.height) * H), round(b.size.width * W), round(b.size.height * H)])
    return out

if __name__ == "__main__":
    res = ocr(sys.argv[1]); json.dump(res, open(sys.argv[1] + ".ocr.json", "w"), ensure_ascii=False)
    keys = sys.argv[2:]
    for r in res:
        if not keys or any(k.lower() in r[0].lower() for k in keys): print(r)
