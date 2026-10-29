#!/usr/bin/env python3
"""LayerCue 인스타그램 자동 발행 (Instagram API with Facebook Login).

@layercue 는 페이스북 'LayerCue' 페이지에 연결돼 있고, 그 페이지를 관리하는
페이스북 사용자 토큰으로 graph.facebook.com 을 부른다. FB_PAGE_ID 가 있으면
같은 게시물을 페이스북 페이지에도 올린다.

사용법:
  python3 publish.py whoami                 # 토큰 확인, 연결된 인스타 계정 찾아 IG_USER_ID 기록
  python3 publish.py post posts/<폴더>      # 게시물 발행
  python3 publish.py post posts/<폴더> --dry-run   # 보내지 않고 보낼 내용만 출력
  python3 publish.py refresh                # 단기 토큰을 장기 토큰(60일)으로 바꿔 .env 에 다시 씀

게시물 폴더:
  post.json   {"media": ["1.jpg", "2.jpg"], "share_to_feed": true}
  caption.txt 캡션(해시태그 포함)
  media 가 http 로 시작하면 그대로, 아니면 MEDIA_BASE_URL + 이 저장소 기준 경로로 씀.
  .jpg 1장 = 사진, 여러 장 = 캐러셀, .mp4 1개 = 릴스.
발행이 끝나면 published.json 에 올린 곳마다 기록되고, 이미 올린 곳에는 다시 올리지 않는다.

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
    def __init__(self, env, token=None):
        self.token = token or env.get("IG_ACCESS_TOKEN", "")
        if not self.token:
            sys.exit(".env 에 IG_ACCESS_TOKEN 이 없습니다. README 의 설정 순서를 보세요.")
        self.base = f"https://graph.facebook.com/{env.get('IG_API_VERSION', 'v26.0')}"

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
    api = Api(env)
    me = api.call("GET", "me", {"fields": "id,name"})
    print(f"페이스북 사용자: {me.get('name')} ({me.get('id')})")
    pages = api.call("GET", "me/accounts", {
        "fields": "id,name,instagram_business_account{id,username}"}).get("data", [])
    want = env.get("IG_USERNAME", "layercue")
    found = None
    for p in pages:
        ig = p.get("instagram_business_account")
        print(f"  페이지 {p['name']}: 인스타 {('@' + ig['username']) if ig else '연결 안 됨'}")
        if ig and ig.get("username") == want:
            found = ig
            page_id = p["id"]
    if not found:
        sys.exit(f"@{want} 가 연결된 페이지를 찾지 못했습니다. 페이지-인스타 연결과 토큰 권한(pages_show_list)을 확인하세요.")
    for key, value in (("IG_USER_ID", found["id"]), ("FB_PAGE_ID", page_id)):
        if env.get(key) != value:
            save_env_value(key, value)
            print(f"{key}={value} 를 .env 에 적었습니다.")


def refresh(env):
    # 그래프 API 탐색기에서 받은 단기 토큰(1~2시간)을 장기 토큰(60일)으로 바꾼다.
    # 만료 전에 다시 실행하면 새 60일짜리로 바뀐다.
    for k in ("FB_APP_ID", "FB_APP_SECRET"):
        if not env.get(k):
            sys.exit(f".env 에 {k} 가 없습니다. 앱 대시보드 > 앱 설정 > 기본 설정에서 확인하세요.")
    data = urllib.parse.urlencode({
        "grant_type": "fb_exchange_token", "client_id": env["FB_APP_ID"],
        "client_secret": env["FB_APP_SECRET"],
        "fb_exchange_token": env.get("IG_ACCESS_TOKEN", "")}).encode()
    url = f"https://graph.facebook.com/{env.get('IG_API_VERSION', 'v26.0')}/oauth/access_token"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=60) as r:
            res = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"토큰 교환 실패 {e.code}: {e.read().decode(errors='replace')}")
    save_env_value("IG_ACCESS_TOKEN", res["access_token"])
    days = int(res.get("expires_in", 0)) // 86400
    print(f"장기 토큰으로 바꿨습니다. 남은 기간 약 {days}일." if days else "장기 토큰으로 바꿨습니다.")


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
    done_path = post_dir / "published.json"
    done = json.loads(done_path.read_text(encoding="utf-8")) if done_path.exists() else {}
    targets = ["instagram"] + (["facebook"] if env.get("FB_PAGE_ID") else [])
    todo = [t for t in targets if t not in done]
    if not todo:
        sys.exit("이미 발행한 게시물입니다: " + ", ".join(d["permalink"] for d in done.values()))
    p = plan_post(env, post_dir)
    if dry_run:
        print(f"[dry-run] 올릴 곳: {', '.join(todo)}")
        print(f"[dry-run] 종류: {p['kind']}")
        for u in p["urls"]:
            print(f"[dry-run] 미디어: {u}")
        print(f"[dry-run] 캡션 ({len(p['caption'])}자):\n{p['caption']}")
        return

    # 한쪽이 실패해도 성공한 쪽은 기록해 두고, 다시 실행하면 남은 쪽만 올린다.
    for target in todo:
        record = (post_instagram if target == "instagram" else post_facebook)(env, p)
        done[target] = record
        done_path.write_text(json.dumps(done, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{target} 에 발행했습니다: {record['permalink']}")


def post_facebook(env, p):
    user_api = Api(env)
    page_id = env["FB_PAGE_ID"]
    page_token = user_api.call("GET", page_id, {"fields": "access_token"})["access_token"]
    api = Api(env, token=page_token)
    if p["kind"] == "REELS":
        res = api.call("POST", f"{page_id}/videos", {
            "file_url": p["urls"][0], "description": p["caption"]})
        post_id = res["id"]
    elif p["kind"] == "IMAGE":
        res = api.call("POST", f"{page_id}/photos", {"url": p["urls"][0], "message": p["caption"]})
        post_id = res.get("post_id", res["id"])
    else:
        # 여러 장은 사진을 비공개로 올려 두고 피드 글 하나에 묶는다. 페이스북 피드는 영상 섞기를 안 받아 사진만 쓴다.
        params = {"message": p["caption"]}
        photos = [u for u, e in zip(p["urls"], p["exts"]) if e in IMAGE_EXT]
        for i, url in enumerate(photos):
            ph = api.call("POST", f"{page_id}/photos", {"url": url, "published": "false"})
            params[f"attached_media[{i}]"] = json.dumps({"media_fbid": ph["id"]})
        post_id = api.call("POST", f"{page_id}/feed", params)["id"]
    info = api.call("GET", post_id, {"fields": "permalink_url,created_time"})
    link = info.get("permalink_url") or ""
    if link.startswith("/"):            # 동영상(릴스)은 「/reel/…」처럼 앞부분 없이 온다
        link = "https://www.facebook.com" + link
    return {"post_id": post_id, "permalink": link,
            "timestamp": info.get("created_time"), "kind": p["kind"]}


def post_instagram(env, p):
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
    return {"media_id": pub["id"], "permalink": info.get("permalink"),
            "timestamp": info.get("timestamp"), "kind": p["kind"]}


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
