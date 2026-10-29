#!/usr/bin/env python3
"""LayerCue 인스타그램 자동 발행 (Instagram API with Instagram Login).

사용법:
  python3 publish.py whoami                 # 토큰 확인, 계정 아이디·IG_USER_ID 출력
  python3 publish.py post posts/<폴더>      # 게시물 발행
  python3 publish.py post posts/<폴더> --dry-run   # 보내지 않고 보낼 내용만 출력
  python3 publish.py refresh                # 장기 토큰 연장(60일), .env 에 다시 씀

게시물 폴더:
  post.json   {"media": ["1.jpg", "2.jpg"], "share_to_feed": true}
  caption.txt 캡션(해시태그 포함)
  media 가 http 로 시작하면 그대로, 아니면 MEDIA_BASE_URL + 이 저장소 기준 경로로 씀.
  .jpg 1장 = 사진, 여러 장 = 캐러셀, .mp4 1개 = 릴스.
발행이 끝나면 published.json 이 생기고, 같은 폴더는 다시 올리지 않는다.

표준 라이브러리만 쓴다.
"""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV_PATH = ROOT / ".env"
IMAGE_EXT = {".jpg", ".jpeg"}
VIDEO_EXT = {".mp4", ".mov"}


def load_env():
    env = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def save_env_value(key, value):
    lines = ENV_PATH.read_text(encoding="utf-8").splitlines() if ENV_PATH.exists() else []
    for i, line in enumerate(lines):
        if line.split("=", 1)[0].strip() == key:
            lines[i] = f"{key}={value}"
            break
    else:
        lines.append(f"{key}={value}")
    ENV_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


class Api:
    def __init__(self, env):
        self.token = env.get("IG_ACCESS_TOKEN", "")
        if not self.token:
            sys.exit(".env 에 IG_ACCESS_TOKEN 이 없습니다. README 의 설정 순서를 보세요.")
        self.base = f"https://graph.instagram.com/{env.get('IG_API_VERSION', 'v23.0')}"

    def call(self, method, path, params=None):
        url = f"{self.base}/{path}"
        data = None
        if method == "GET" and params:
            url += "?" + urllib.parse.urlencode(params)
        elif params:
            data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"Bearer {self.token}")
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")
            sys.exit(f"API 오류 {e.code} ({method} {path}): {body}")


def whoami(env):
    me = Api(env).call("GET", "me", {"fields": "user_id,username,account_type"})
    print(json.dumps(me, ensure_ascii=False, indent=2))
    if me.get("user_id") and env.get("IG_USER_ID") != str(me["user_id"]):
        save_env_value("IG_USER_ID", me["user_id"])
        print(f"IG_USER_ID={me['user_id']} 를 .env 에 적었습니다.")


def refresh(env):
    # 장기 토큰은 발급 후 24시간이 지나야 연장할 수 있다.
    url = "https://graph.instagram.com/refresh_access_token?" + urllib.parse.urlencode(
        {"grant_type": "ig_refresh_token"})
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {env.get('IG_ACCESS_TOKEN', '')}")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            res = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"토큰 연장 실패 {e.code}: {e.read().decode(errors='replace')}")
    save_env_value("IG_ACCESS_TOKEN", res["access_token"])
    days = int(res.get("expires_in", 0)) // 86400
    print(f"토큰을 연장했습니다. 남은 기간 약 {days}일.")


def media_url(env, post_dir, item):
    if item.startswith(("http://", "https://")):
        return item
    local = post_dir / item
    if not local.exists():
        sys.exit(f"파일이 없습니다: {local}")
    base = env.get("MEDIA_BASE_URL", "").rstrip("/")
    if not base:
        sys.exit(".env 에 MEDIA_BASE_URL 이 없습니다. 인스타 서버가 받아갈 공개 주소가 필요합니다.")
    rel = local.resolve().relative_to(ROOT).as_posix()
    return f"{base}/{urllib.parse.quote(rel)}"


def plan_post(env, post_dir):
    meta = json.loads((post_dir / "post.json").read_text(encoding="utf-8"))
    caption = (post_dir / "caption.txt").read_text(encoding="utf-8").strip()
    if len(caption) > 2200:
        sys.exit(f"캡션이 너무 깁니다({len(caption)}자, 최대 2200자).")
    items = meta["media"]
    exts = [Path(urllib.parse.urlparse(i).path).suffix.lower() for i in items]
    for ext in exts:
        if ext not in IMAGE_EXT | VIDEO_EXT:
            sys.exit(f"지원하지 않는 형식 {ext}: 사진은 JPEG, 영상은 MP4/MOV 만 됩니다.")
    urls = [media_url(env, post_dir, i) for i in items]
    if len(items) == 1:
        kind = "REELS" if exts[0] in VIDEO_EXT else "IMAGE"
    elif 2 <= len(items) <= 10:
        kind = "CAROUSEL"
    else:
        sys.exit("캐러셀은 2~10장입니다.")
    return {"kind": kind, "caption": caption, "urls": urls, "exts": exts,
            "share_to_feed": meta.get("share_to_feed", True)}


def wait_ready(api, container_id):
    for _ in range(60):
        st = api.call("GET", container_id, {"fields": "status_code,status"})
        code = st.get("status_code")
        if code == "FINISHED":
            return
        if code in ("ERROR", "EXPIRED"):
            sys.exit(f"미디어 처리 실패: {st}")
        time.sleep(5)
    sys.exit("미디어 처리가 5분 안에 끝나지 않았습니다.")


def post(env, post_dir, dry_run):
    post_dir = Path(post_dir).resolve()
    done = post_dir / "published.json"
    if done.exists():
        sys.exit(f"이미 발행한 게시물입니다: {json.loads(done.read_text())['permalink']}")
    p = plan_post(env, post_dir)
    if dry_run:
        print(f"[dry-run] 종류: {p['kind']}")
        for u in p["urls"]:
            print(f"[dry-run] 미디어: {u}")
        print(f"[dry-run] 캡션 ({len(p['caption'])}자):\n{p['caption']}")
        return

    api = Api(env)
    uid = env.get("IG_USER_ID") or sys.exit("IG_USER_ID 가 없습니다. 먼저 whoami 를 실행하세요.")

    if p["kind"] == "IMAGE":
        c = api.call("POST", f"{uid}/media", {"image_url": p["urls"][0], "caption": p["caption"]})
    elif p["kind"] == "REELS":
        c = api.call("POST", f"{uid}/media", {
            "media_type": "REELS", "video_url": p["urls"][0], "caption": p["caption"],
            "share_to_feed": str(p["share_to_feed"]).lower()})
    else:
        children = []
        for url, ext in zip(p["urls"], p["exts"]):
            params = {"is_carousel_item": "true"}
            if ext in VIDEO_EXT:
                params.update(media_type="VIDEO", video_url=url)
            else:
                params["image_url"] = url
            child = api.call("POST", f"{uid}/media", params)
            wait_ready(api, child["id"])
            children.append(child["id"])
        c = api.call("POST", f"{uid}/media", {
            "media_type": "CAROUSEL", "children": ",".join(children), "caption": p["caption"]})

    wait_ready(api, c["id"])
    pub = api.call("POST", f"{uid}/media_publish", {"creation_id": c["id"]})
    info = api.call("GET", pub["id"], {"fields": "permalink,timestamp"})
    record = {"media_id": pub["id"], "permalink": info.get("permalink"),
              "timestamp": info.get("timestamp"), "kind": p["kind"]}
    done.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"발행했습니다: {record['permalink']}")


def main():
    args = sys.argv[1:]
    env = load_env()
    if args[:1] == ["whoami"]:
        whoami(env)
    elif args[:1] == ["refresh"]:
        refresh(env)
    elif args[:1] == ["post"] and len(args) >= 2:
        post(env, args[1], "--dry-run" in args)
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
