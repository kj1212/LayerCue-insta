#!/usr/bin/env python3
"""17편 OBS 준비 — obs-websocket(이 맥 안, 127.0.0.1)으로 장면 모음 「LayerCue Show」 · 장면 「Stream」 을 만든다.
   Camera = 무대 사진(media/choir-camera.png, 로컬 이미지 생성 — 카메라 대신) · LayerCue (NDI) · LayerCue (Syphon)."""
import json, os, pathlib, sys, time
import obsws_python as obs
H = pathlib.Path(__file__).resolve().parent
PW = json.load(open(os.path.expanduser("~/Library/Application Support/obs-studio/plugin_config/obs-websocket/config.json")))["server_password"]
c = obs.ReqClient(host="127.0.0.1", port=4455, password=PW, timeout=10)
if "list" in sys.argv:
    print(c.get_scene_collection_list().scene_collections); print([s["sceneName"] for s in c.get_scene_list().scenes])
    print([(i["inputName"], i["inputKind"]) for i in c.get_input_list().inputs]); sys.exit()
if "LayerCue Show" not in c.get_scene_collection_list().scene_collections:
    c.create_scene_collection("LayerCue Show"); time.sleep(2)
else:
    c.set_current_scene_collection("LayerCue Show"); time.sleep(2)
scenes = [s["sceneName"] for s in c.get_scene_list().scenes]
if "Stream" not in scenes:
    c.create_scene("Stream")
for s in scenes:
    if s != "Stream": c.remove_scene(s)
c.set_current_program_scene("Stream")
have = [i["inputName"] for i in c.get_input_list().inputs]
for name in have:                                      # 기본 오디오 장치(이름이 한국어)는 뺀다
    if name not in ("Camera", "LayerCue (NDI)", "LayerCue (Syphon)"): c.remove_input(name)
if "Camera" not in have: c.create_input("Stream", "Camera", "image_source", {"file": str(H / "media" / "choir-camera.png")}, True)
if "LayerCue (NDI)" not in have: c.create_input("Stream", "LayerCue (NDI)", "ndi_source", {}, True)
print([(i["inputName"], i["inputKind"]) for i in c.get_input_list().inputs])
