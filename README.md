# LayerCue 인스타그램 · 페이스북

[@layercue](https://www.instagram.com/layercue/) 계정과 페이스북 [LayerCue](https://www.facebook.com/profile.php?id=61596265250122) 페이지에 업데이트 게시물을 만들고, Graph API 로 두 곳에 같이 자동 발행한다.

## 처음 한 번만 하는 설정

Facebook 로그인 방식(Instagram API with Facebook Login)을 쓴다. 이 Meta 앱에는 Instagram 로그인 방식이 열리지 않았다.

1. **프로페셔널 계정**: @layercue 는 크리에이터 계정(카테고리: 소프트웨어)으로 전환해 두었다.
2. **Meta 앱**: [LayerCue](https://developers.facebook.com/apps/1444173200564298/) (앱 ID 1444173200564298, 개발 모드). 이용 사례 "Instagram에서 메시지 및 콘텐츠 관리"에 콘텐츠 관리 권한(`instagram_basic`, `instagram_content_publish`, `pages_show_list`, `pages_read_engagement`, `business_management`)을 추가해 두었다. 페이지 게시용으로 이용 사례 "페이지의 모든 부분 관리"를 더해 `pages_manage_posts` 를 추가해 두었다.
   - 본인 계정만 쓰므로 앱 검수(App Review)는 필요 없다.
3. **페이스북 페이지**: [LayerCue](https://www.facebook.com/profile.php?id=61596265250122) 페이지를 만들고 @layercue 를 연결해 두었다(페이지 설정 > 연결된 계정 > Instagram).
4. **토큰 받기**: [그래프 API 탐색기](https://developers.facebook.com/tools/explorer/)에서 앱 LayerCue, "사용자 토큰"을 고르고 위 6개 권한을 넣어 *Generate Access Token* → LayerCue 페이지와 @layercue 를 허용한다.
5. **`.env` 채우기**: `IG_ACCESS_TOKEN` 에 그 토큰을, `FB_APP_SECRET` 에 앱 설정 > 기본 설정의 앱 시크릿 코드를 직접 붙여 넣는다.
6. **장기 토큰으로 바꾸고 확인**: `python3 publish.py refresh` (60일짜리로 교환) → `python3 publish.py whoami` (연결된 @layercue 를 찾아 `IG_USER_ID`, `FB_PAGE_ID` 기록).
7. **사진 공개 주소**: 인스타 API 는 파일을 직접 받지 않고 공개 URL 에서 가져간다. 이 저장소는 GitHub Pages(<https://kj1212.github.io/LayerCue-insta>)로 공개돼 있고, `.env.example` 의 `MEDIA_BASE_URL` 이 그 주소다. 게시물 폴더는 발행 전에 커밋·푸시해서 Pages 에 올라가 있어야 한다.

## 게시물 올리기

```
posts/2026-10-29-v0.9.12/
  post.json     {"media": ["1.jpg", "2.jpg"]}
  caption.txt   캡션과 해시태그
  1.jpg 2.jpg
```

- 사진은 JPEG 만 된다. 1장이면 사진, 2~10장이면 캐러셀, `.mp4` 1개면 릴스.
- `python3 publish.py post posts/<폴더> --dry-run` 으로 먼저 확인하고, `--dry-run` 을 빼면 발행한다.
- 인스타에 먼저 올리고, `FB_PAGE_ID` 가 있으면 같은 사진·캡션을 페이스북 페이지에도 올린다. 페이지 쪽 캐러셀은 사진만 묶인다.
- 올린 곳마다 `published.json` 에 기록된다. 한쪽만 실패했으면 다시 실행할 때 남은 쪽만 올라간다.
- 24시간에 API 발행은 100건까지.

## 토큰 연장

장기 토큰은 60일 뒤 만료된다. 만료 전에 `python3 publish.py refresh` 를 다시 실행하면 새 60일짜리로 바뀐다. 이미 만료됐으면 4단계부터 다시 한다.
