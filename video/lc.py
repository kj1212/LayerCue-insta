#!/usr/bin/env python3
"""촬영용 LayerCue(모래상자) 를 MCP 다리로 부린다 — 사람이 쓰는 LayerCue 는 건드리지 않는다.

    python3 lc.py get_state
    python3 lc.py run_commands '{"commands":[{"op":"usePt","name":"Start here"},{"op":"present","n":1}]}'

다리는 개발 빌드의 layercue-mcp. LAYERCUE_MCP_DIR 를 sandbox/mcp 로 주면 그 자리의 만남 파일만 본다
(LayerCue/tools/mcp-smoke.py 와 같은 길).
"""
import json, os, subprocess, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
BRIDGE = pathlib.Path(os.environ.get("LC_BUILD", str(pathlib.Path.home() / "projects/LayerCue-film-0912/build"))) / "LayerCue.app/Contents/MacOS/layercue-mcp"
MCP = HERE / os.environ.get("LC_SANDBOX", "sandbox") / "mcp"     # LC_SANDBOX=sandbox-ep01 처럼 다른 모래상자를 고른다


def call(tool, args=None):
    """tool="tools/list" 면 도구 목록(설명 포함)을 돌려준다."""
    env = dict(os.environ, LAYERCUE_MCP_DIR=str(MCP), LAYERCUE_MCP_JSON=str(MCP / "mcp-layercue-dev.json"))
    p = subprocess.Popen([str(BRIDGE)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                         env=env, text=True, encoding="utf-8", bufsize=1)
    def send(o): p.stdin.write(json.dumps(o, ensure_ascii=False) + "\n"); p.stdin.flush()
    def wait(i):
        for line in p.stdout:
            o = json.loads(line)
            if o.get("id") == i: return o
    send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
          "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "film", "version": "1"}}})
    wait(1)
    send({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
    if tool == "tools/list":
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    else:
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": tool, "arguments": args or {}}})
    r = wait(2)
    p.stdin.close(); p.wait(5)
    return r


if __name__ == "__main__":
    r = call(sys.argv[1], json.loads(sys.argv[2]) if len(sys.argv) > 2 else {})
    for c in r.get("result", {}).get("content", []):
        if c.get("type") == "text": print(c["text"][:3000])
    if "error" in r: print("ERROR", r["error"])
