#!/usr/bin/env python3
"""인스타 게시물 → 유튜브 쇼츠 · 게시물(커뮤니티) 묶음. youtube/shorts/, youtube/posts/ 에 만들고 원드라이브에도 복사한다.
    python3 tools/yt_social.py
"""
import json, shutil, subprocess, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / "posts"; Y = ROOT / "youtube"
OD = pathlib.Path.home() / "OneDrive" / "LayerCue from Zero"

def srt(cues):
    def ts(t): return f"{int(t//3600):02d}:{int(t%3600//60):02d}:{t%60:06.3f}".replace(".", ",")
    return "".join(f"{i}\n{ts(a)} --> {ts(b)}\n{x}\n\n" for i, (a, b, x) in enumerate(cues, 1))

ASK_T = [(0.32, 2.9), (3.12, 6.2), (6.32, 9.1), (9.28, 11.0), (11.12, 12.4), (12.48, 13.1), (13.2, 14.6), (17.12, 18.1), (18.24, 21.3)]
ASK = {"en": ["What if you could just ask?", "Make a presentation that explains LayerCue's features.", "Your AI builds it, straight into LayerCue.",
              "Libraries for your slides.", "Cue sheets for the night.", "Click once.", "It's live.", "LayerCue.", "Free while it's in beta, on Mac and Windows."],
       "ko": ["그냥 말로 부탁할 수 있다면?", "LayerCue 기능을 설명하는 프레젠테이션을 만들어 줘.", "AI가 LayerCue 안에 바로 만들어요.",
              "슬라이드는 라이브러리에.", "그날 밤 순서는 큐시트에.", "한 번 클릭하면,", "바로 송출돼요.", "LayerCue.", "베타 기간 동안 무료, Mac과 Windows에서."],
       "ja": ["ただ頼むだけでいいとしたら?", "LayerCue の機能を説明するプレゼンを作って。", "AI が LayerCue の中に直接作ります。",
              "スライドはライブラリに。", "その夜の進行はキューシートに。", "ワンクリックで、", "すぐ本番に。", "LayerCue。", "ベータ期間中は無料。Mac と Windows で。"]}
INTRO_JA = ["7つのレイヤー。すべての画面へ。", "ループする背景、", "その上にスライド、", "いちばん上にロゴと名前。", "それぞれが独立したレイヤーです。",
            "すべての画面に送り、", "画面ごとに必要なレイヤーだけを。", "1つ変えても、ほかは動きません。", "これが LayerCue。", "ベータ期間中は無料。Mac と Windows で。"]

def intro_cues(lang):
    src = (P / "2026-10-31-intro-reel/subtitles/en.srt").read_text().strip().split("\n\n")
    out = []
    for i, b in enumerate(src):
        ln = b.splitlines(); a, z = ln[1].split(" --> ")
        f = lambda s: int(s[:2])*3600 + int(s[3:5])*60 + float(s[6:].replace(",", "."))
        text = INTRO_JA[i] if lang == "ja" else (P / f"2026-10-31-intro-reel/subtitles/{lang}.srt").read_text().strip().split("\n\n")[i].splitlines()[2]
        out.append((f(a), f(z), text))
    return out

SHORTS = [
 ("short01-seven-layers", "2026-10-31-intro-reel",
  dict(en="Seven layers. Every screen. #Shorts", ko="레이어 일곱 개, 모든 화면으로 #Shorts", ja="7つのレイヤー。すべての画面へ #Shorts"),
  dict(en="A background that loops underneath, your slides on top, a logo and a name over it all. In LayerCue each one is its own layer, and each one goes live with a single click.\n\nSend the show to every screen in the room, and give each screen only the layers it needs.\n\nFree while it's in beta, on Mac and Windows: https://layercue.com\nFull tutorial series: LayerCue from Zero\n\nThe narration and music were made with AI running on a Mac. The event in the demo is made up.\n\n#LayerCue #LiveProduction #EventProduction",
       ko="반복되는 배경 영상 위에 슬라이드, 그 위에 로고와 이름. LayerCue에서는 하나하나가 따로 된 레이어이고, 클릭 한 번으로 송출돼요.\n\n공연장의 모든 화면으로 보내고, 화면마다 필요한 레이어만 골라 보여 주세요.\n\n베타 기간 동안 무료, Mac과 Windows: https://layercue.com\n전체 튜토리얼: LayerCue 처음부터\n\n나레이션과 음악은 Mac에서 AI로 만들었어요. 데모의 행사는 가상이에요.",
       ja="ループする背景の上にスライド、さらにその上にロゴと名前。LayerCue ではそれぞれが独立したレイヤーで、ワンクリックで本番に出せます。\n\n会場のすべての画面に送り、画面ごとに必要なレイヤーだけを表示できます。\n\nベータ期間中は無料、Mac と Windows: https://layercue.com\nチュートリアル全編: ゼロから LayerCue\n\nナレーションと音楽は Mac 上の AI で作りました。デモのイベントは架空です。"),
  "intro"),
 ("short02-just-ask", "2026-10-30-ask-reel",
  dict(en="What if you could just ask? AI builds your slides in LayerCue #Shorts", ko="그냥 말로 부탁한다면? AI가 LayerCue에 슬라이드를 만들어요 #Shorts", ja="頼むだけでいいとしたら? AI が LayerCue にスライドを作る #Shorts"),
  dict(en="Connect your AI app to LayerCue over MCP (Claude, Cursor, LM Studio) and say \"make a presentation that explains LayerCue's features.\" It builds the slides straight into LayerCue, checks what LayerCue actually drew, and lines them up in a cue sheet.\n\nLibraries for your slides. Cue sheets for the night. Click once, and it's live on the big screen.\n\nFree while it's in beta, on Mac and Windows: https://layercue.com\n\nThe narration and music were made with AI running on a Mac.\n\n#LayerCue #MCP #LiveProduction",
       ko="AI 앱(Claude, Cursor, LM Studio)을 MCP로 LayerCue에 연결하고 \"LayerCue 기능을 설명하는 프레젠테이션을 만들어 줘\"라고 말해 보세요. 슬라이드를 LayerCue 안에 바로 만들고, LayerCue가 실제로 그린 결과를 확인한 뒤 큐시트에 차례로 넣어요.\n\n슬라이드는 라이브러리에, 그날 밤 순서는 큐시트에. 한 번 클릭하면 큰 화면에 나가요.\n\n베타 기간 동안 무료, Mac과 Windows: https://layercue.com\n\n나레이션과 음악은 Mac에서 AI로 만들었어요.",
       ja="AI アプリ(Claude、Cursor、LM Studio)を MCP で LayerCue につなぎ、「LayerCue の機能を説明するプレゼンを作って」と言うだけ。LayerCue の中に直接スライドを作り、実際に描かれた結果を確認して、キューシートに並べます。\n\nスライドはライブラリに、その夜の進行はキューシートに。ワンクリックで大きな画面に出ます。\n\nベータ期間中は無料、Mac と Windows: https://layercue.com\n\nナレーションと音楽は Mac 上の AI で作りました。"),
  "ask"),
]

POSTS = [
 ("post01-whats-new", "2026-10-29-whats-new",
  dict(ko="8월 이후 LayerCue의 새 기능, 0.9.4부터 0.9.12까지.\n\n이제 Windows에서도 돼요. Mac과 함께 Microsoft Store에서 무료로 받을 수 있어요.\n\n공연장의 모든 화면으로. 무대 하나를 모니터 여러 대에, NDI®·Syphon으로, Mac에서는 Blackmagic SDI로, 스위처에는 fill & key로 보내요. 0.9.12부터는 음악과 영상 소리도 NDI®와 SDI로 함께 나가요.\n\n가진 걸 그대로. PowerPoint는 편집할 수 있는 상태로 들어와요. PDF도 넣고 내보내요. 모든 곡의 가사를 열지 않고 검색해요.\n\n말로 슬라이드를. Settings › AI apps에서 Claude, LM Studio, Cursor를 연결하고 \"이 가사로 슬라이드 만들어 줘\"라고 해 보세요.\n\n베타 기간 동안 무료: https://layercue.com",
       ja="8月以降の LayerCue の新機能、0.9.4 から 0.9.12 まで。\n\nWindows に対応しました。Mac と同じく Microsoft Store で無料です。\n\n会場のすべての画面へ。1つのステージを何台ものモニターに、NDI®・Syphon で、Mac では Blackmagic SDI で、スイッチャーには fill & key で。0.9.12 からは音楽と動画の音も NDI® と SDI で送れます。\n\n手持ちのものをそのまま。PowerPoint は編集できる形で取り込めます。PDF の読み込みと書き出しも。歌詞を開かずに全曲を検索できます。\n\n言葉でスライドを。Settings › AI apps で Claude、LM Studio、Cursor をつないで「この歌詞でスライドを作って」と頼んでみてください。\n\nベータ期間中は無料: https://layercue.com")),
 ("post02-propresenter", "2026-10-30-propresenter",
  dict(ko="ProPresenter 라이선스가 부담되나요? 컴퓨터마다 라이선스가 필요하면 금방 늘어나요. 학교 강당, 작은 공연장, 회의실, 교회, 뒤에서 화면을 맡는 누구에게나요. 대부분은 그중 일부만 쓰는데도요.\n\n솔직하게 말할게요. ProPresenter를 전부 쓰신다면 계속 쓰세요. 좋은 프로그램이고, 저희보다 훨씬 많은 일을 해요.\n\n하지만 대부분 반복되는 배경, 가사, 자막과 로고, 유튜브 영상, 그리고 말 잘 듣는 두 번째 화면이 필요하다면, 그게 바로 LayerCue가 하는 일이에요. 베타 기간 동안 무료, Mac과 Windows. PowerPoint도 편집 가능한 슬라이드로 열려요.\n\n다음 공연에서 갱신하기 전에 한번 써 보세요: https://layercue.com\n\nProPresenter는 Renewed Vision의 상표예요. LayerCue는 Renewed Vision과 관계가 없어요.",
       ja="ProPresenter のライセンスが負担ですか? パソコンごとのライセンスはすぐにかさみます。学校のホール、小さな会場、会議室、教会、後ろで画面を担当する誰にとっても。たいていは一部しか使わないのに。\n\n正直に言います。ProPresenter をすべて使っているなら、そのままお使いください。良いソフトで、私たちよりずっと多くのことができます。\n\nでも、ループする背景、歌詞、テロップとロゴ、YouTube 動画、ちゃんと動く2台目の画面が主な用途なら、それこそ LayerCue の役目です。ベータ期間中は無料、Mac と Windows。PowerPoint も編集できるスライドとして開けます。\n\n更新の前に、次の本番で試してみてください: https://layercue.com\n\nProPresenter は Renewed Vision の商標です。LayerCue は Renewed Vision とは関係ありません。")),
]

def yt_en(caption):
    t = caption.replace("layercue.com — link in bio", "https://layercue.com")
    body, _, tags = t.rpartition("\n\n#")
    tags = ("#" + tags).split()[:3]
    return body.strip() + "\n\n" + " ".join(tags)

def main():
    sd = Y / "shorts"; pd = Y / "posts"
    for name, src, title, desc, kind in SHORTS:
        o = sd / name; (o / "subtitles").mkdir(parents=True, exist_ok=True)
        shutil.copy(P / src / "reel.mp4", o / f"{name}.mp4"); shutil.copy(P / src / "cover.jpg", o / f"{name}-cover.jpg")
        for lang in ("en", "ko", "ja"):
            cues = [(a, b, x) for (a, b), x in zip(ASK_T, ASK[lang])] if kind == "ask" else intro_cues(lang)
            (o / "subtitles" / f"{name}-{lang}.srt").write_text(srt(cues), encoding="utf-8")
        up = ["YOUTUBE SHORT — upload the vertical video; YouTube makes it a Short (under 3 min, 9:16).", "",
              f"TITLE\n{title['en']}\n", f"DESCRIPTION\n{desc['en']}\n", "TAGS\nLayerCue, LayerCue tutorial, presentation software, live production, event production, projection software, Mac, Windows\n",
              "PLAYLIST\nLayerCue Shorts (optional)\n", f"SUBTITLES\nsubtitles/{name}-en.srt, -ko.srt, -ja.srt as 'With timing'.\n",
              "COVER\nShorts use a frame from the video; the app's mobile upload can also pick a cover. The Instagram cover is included.\n"]
        for lang, head in (("ko", "한국어 (KOREAN)"), ("ja", "日本語 (JAPANESE)")):
            up += ["=" * 40, head, "=" * 40, "", f"TITLE\n{title[lang]}\n", f"DESCRIPTION\n{desc[lang]}\n"]
        (o / f"{name}-upload.txt").write_text("\n".join(up), encoding="utf-8")
    for name, src, tr in POSTS:
        o = pd / name; o.mkdir(parents=True, exist_ok=True)
        media = json.load(open(P / src / "post.json"))["media"]
        for i, m in enumerate(media, 1): shutil.copy(P / src / m, o / f"{name}-{i}.jpg")
        cap = (P / src / "caption.txt").read_text()
        txt = [f"YOUTUBE POST (Community) — Create › Post › Image, add the {len(media)} images in order ({name}-1.jpg …), paste the text.",
               "YouTube posts have one text box: post in English, or paste the Korean/Japanese version as a separate post.", "",
               "TEXT (ENGLISH)", yt_en(cap), "", "=" * 40, "한국어 (KOREAN)", "=" * 40, tr["ko"], "", "=" * 40, "日本語 (JAPANESE)", "=" * 40, tr["ja"]]
        (o / f"{name}-text.txt").write_text("\n".join(txt) + "\n", encoding="utf-8")
    if OD.parent.exists():
        for sub in ("shorts", "posts"):
            subprocess.run(["rsync", "-a", "--delete", "--exclude", ".DS_Store", str(Y / sub), str(OD) + "/"], check=True)
        print("copied →", OD / "shorts", OD / "posts")

if __name__ == "__main__":
    main()
