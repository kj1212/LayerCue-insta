# Over the Camera: NDI, Syphon and Fill & Key | LayerCue from Zero, Episode 17

## A screen without a monitor

- Welcome back! Today: sending the stage to other apps and machines, like OBS, a switcher, or a streaming computer.  
  다시 만나서 반가워요! 오늘은 무대를 다른 앱과 기계로 보내 봐요. OBS, 스위처, 스트리밍 컴퓨터 같은 곳으로요.
- Open Stage output, and press Add screen. Under Send to, Network and apps sends a video stream instead of opening a window.  
  Stage output을 열고 Add screen을 누르세요. Send to의 Network · apps는 창을 여는 대신 영상 스트림으로 보내요.
- NDI goes over the network, to OBS, vMix or a switcher. Syphon goes to another app on this Mac.  
  NDI는 네트워크로 OBS, vMix, 스위처에 가고, Syphon은 이 맥의 다른 앱으로 가요.

## NDI out

- Pick NDI, and give it a name. Receivers see this name in their list.  
  NDI를 고르고 이름을 붙이세요. 받는 쪽 목록에 이 이름이 보여요.
- Choose the resolution and frame rate yourself. There's no window to take them from.  
  해상도와 프레임레이트는 직접 골라요. 크기를 가져올 창이 없으니까요.
- Set Alpha to transparent, and turn off B. Only the words go out; the rest is see-through.  
  Alpha를 투명으로 하고 B를 끄세요. 가사만 나가고 나머지는 비쳐 보여요.
- Switch it on. The row counts its receivers: none yet.  
  켜 보세요. 줄에 받는 쪽 수가 나와요. 아직은 없어요.

## Into OBS

- In OBS, open an NDI source. LayerCue's stream is in the list, with this computer's name in front.  
  OBS에서 NDI 소스를 열면 목록에 LayerCue 스트림이 있어요. 앞에 이 컴퓨터 이름이 붙어요.
- Pick it, and send a line from LayerCue. The words sit over the camera.  
  고르고 LayerCue에서 한 줄을 보내면, 가사가 카메라 위에 올라가요.
- The next line follows at once.  
  다음 줄도 바로 따라와요.
- Back in LayerCue, the row now says one receiving.  
  LayerCue로 돌아오면, 줄에 1 receiving이라고 떠요.
- Two things to know. Renaming while it sends starts a new stream, so pick it again in each receiver. And allow the network permission the first time, or other computers can't find it.  
  알아 둘 것 두 가지. 보내는 중에 이름을 바꾸면 새 스트림이 돼서, 받는 쪽마다 다시 골라야 해요. 그리고 처음에 네트워크 권한을 허용하세요. 안 그러면 다른 컴퓨터가 찾지 못해요.
- Audio puts the stage sound into the stream, at its own level. It starts off.  
  Audio를 켜면 무대 소리가 따로 정한 크기로 스트림에 실려요. 처음엔 꺼져 있어요.

## Syphon on the same Mac

- On a Mac, Syphon hands the picture to an app on the same machine, straight from the graphics card.  
  맥에서는 Syphon이 같은 맥의 앱에 그림을 그래픽 카드에서 바로 넘겨 줘요.
- The row says when an app is connected. If letter edges look dark there, try Straight instead of Premultiplied.  
  앱이 연결되면 줄에 표시돼요. 그쪽에서 글자 가장자리가 어둡게 보이면 Premultiplied 대신 Straight를 써 보세요.

## Fill and key for a switcher

- A switcher like an ATEM needs two signals: the fill is the picture, and the key is a black-and-white matte that says where it shows.  
  ATEM 같은 스위처는 신호 두 개가 필요해요. fill은 그림 자체, key는 그림이 보일 자리를 알려 주는 흑백 매트예요.
- Press Add fill and key. A Blackmagic device that sends both, like this UltraStudio, is picked by itself: fill on SDI A, key on SDI B.  
  Add fill & key를 누르세요. 이 UltraStudio처럼 둘을 함께 보내는 Blackmagic 장치는 저절로 잡혀요. fill은 SDI A, key는 SDI B로 나가요.
- SDI format must match the switcher. Changing it while live drops the signal for a moment, so set it before the show.  
  SDI format은 스위처와 같아야 해요. 송출 중에 바꾸면 신호가 잠깐 끊기니, 쇼 전에 맞춰 두세요.
- Keying External is the usual setup: the switcher does the combining. Mix sets how strongly it keys.  
  Keying은 보통 External이에요. 합치는 건 스위처가 해요. Mix는 얼마나 세게 키잉할지 정해요.
- Alpha follows the switcher's pre-multiplied key setting.  
  Alpha는 스위처의 Pre-multiplied Key 설정에 맞추세요.
- And turn off B here too. With the background on, the key is white everywhere, and it covers the camera.  
  그리고 여기서도 B를 끄세요. 배경이 켜져 있으면 key가 온통 흰색이 돼서 카메라를 덮어요.

## What's next

- You can now put the words over a camera, in OBS or a switcher.  
  이제 OBS나 스위처에서 카메라 위에 가사를 올릴 수 있어요.
- Next time: show day, from the night before to the last cue.  
  다음 편: 쇼 당일. 전날 밤부터 마지막 큐까지.
