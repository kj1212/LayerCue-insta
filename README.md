# LayerCue 인스타그램

[@layercue](https://www.instagram.com/layercue/) 계정의 업데이트 게시물을 만들고, Instagram API 로 자동 발행한다.

## 처음 한 번만 하는 설정

1. **프로페셔널 계정으로 전환**: 인스타 앱 > 설정 > 계정 유형 및 도구 > 프로페셔널 계정으로 전환 (크리에이터 또는 비즈니스). 페이스북 페이지 연결은 필요 없다.
2. **Meta 앱 만들기**: [developers.facebook.com](https://developers.facebook.com/apps) > 앱 만들기 > 사용 사례에서 "Instagram에서 메시지 및 콘텐츠 관리"를 고른다.
3. **토큰 받기**: 앱 대시보드 > Instagram API > *API setup with Instagram login* > *Generate access tokens* 에서 @layercue 를 추가하고 토큰을 만든다. 권한은 `instagram_business_basic`, `instagram_business_content_publish`.
   - 본인 계정만 쓰므로 앱 검수(App Review)는 필요 없다. 앱은 개발 모드로 둔다.
4. **`.env` 채우기**: `.env.example` 을 `.env` 로 복사하고 `IG_ACCESS_TOKEN` 에 토큰을 붙여 넣는다. 토큰은 직접 넣는다.
5. **확인**: `python3 publish.py whoami` 를 실행하면 계정 정보가 나오고 `IG_USER_ID` 가 채워진다.
6. **사진 공개 주소**: 인스타 API 는 파일을 직접 받지 않고 공개 URL 에서 가져간다. 이 저장소를 GitHub Pages 로 공개하는 식으로 `MEDIA_BASE_URL` 을 정한다.

## 게시물 올리기

```
posts/2026-10-29-v0.9.12/
  post.json     {"media": ["1.jpg", "2.jpg"]}
  caption.txt   캡션과 해시태그
  1.jpg 2.jpg
```

- 사진은 JPEG 만 된다. 1장이면 사진, 2~10장이면 캐러셀, `.mp4` 1개면 릴스.
- `python3 publish.py post posts/<폴더> --dry-run` 으로 먼저 확인하고, `--dry-run` 을 빼면 발행한다.
- 발행하면 `published.json` 이 생기고, 같은 폴더는 다시 올라가지 않는다.
- 24시간에 API 발행은 100건까지.

## 토큰 연장

장기 토큰은 60일 뒤 만료된다. 만료 전에 `python3 publish.py refresh` 를 실행하면 60일이 다시 늘어난다(발급 후 24시간이 지나야 된다).
