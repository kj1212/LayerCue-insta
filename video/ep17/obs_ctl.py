#!/usr/bin/env python3
"""17편 OBS 조종(obs-websocket, 127.0.0.1) — 녹화 앞뒤 정리용. 화면에 보이는 조작(NDI 소스 고르기)은 마우스로 한다.
    obs_ctl.py reset    NDI 소스 이름 비움 · Syphon 소스 지움
    obs_ctl.py syphon   Syphon 소스를 만들어 LayerCue 서버로(투명) · NDI 숨기고 Syphon 보이기
    obs_ctl.py front|place   OBS 창을 앞으로 / LG 오른쪽 자리에"""
import json, os, sys, time, subprocess
import obsws_python as obs
PW = json.load(open(os.path.expanduser("~/Library/Application Support/obs-studio/plugin_config/obs-websocket/config.json")))["server_password"]
def cl(): return obs.ReqClient(host="127.0.0.1", port=4455, password=PW, timeout=10)
def item(c, name): return c.get_scene_item_id("Stream", name).scene_item_id
def osa(s): subprocess.run(["osascript", "-e", s], capture_output=True)
cmd = sys.argv[1]
if cmd == "reset":
    c = cl()
    c.set_input_settings("LayerCue (NDI)", {"ndi_source_name": ""}, False)
    c.set_scene_item_enabled("Stream", item(c, "LayerCue (NDI)"), True)
    if "LayerCue (Syphon)" in [i["inputName"] for i in c.get_input_list().inputs]: c.remove_input("LayerCue (Syphon)")     # Syphon 장면에서 새로 만든다
elif cmd == "syphon":
    c = cl()
    if "LayerCue (Syphon)" not in [i["inputName"] for i in c.get_input_list().inputs]:
        c.create_input("Stream", "LayerCue (Syphon)", "syphon-input", {"allow_transparency": True}, False)
    for _ in range(20):
        it = [x for x in c.send("GetInputPropertiesListPropertyItems", {"inputName": "LayerCue (Syphon)", "propertyName": "uuid"}).property_items if x["itemValue"]]
        if it: break
        time.sleep(0.25)
    c.set_input_settings("LayerCue (Syphon)", {"uuid": it[0]["itemValue"], "allow_transparency": True}, True)
    c.set_scene_item_enabled("Stream", item(c, "LayerCue (NDI)"), False)
    c.set_scene_item_enabled("Stream", item(c, "LayerCue (Syphon)"), True)
elif cmd == "front":
    osa('tell application "System Events" to set frontmost of (first process whose name contains "OBS") to true')
elif cmd == "place":
    osa('tell application "System Events" to tell (first process whose name contains "OBS") to set position of window 1 to {2700, -1050}')
    osa('tell application "System Events" to tell (first process whose name contains "OBS") to set size of window 1 to {1020, 1020}')
