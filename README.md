# 농사 게임

마인크래프트의 농사를 2d로 만든게임입니다.

## 설치

```console
$ git clone https://github.com/newkincode/simple_farming_game.git
$ cd simple_farming_game
$ (pip) install -r requirements.txt

$ python main.py
```

## 빌드

pyinstaller라이브러리가 필요합니다.

```console
$ pyinstaller main.py
```
이후 lib 폴더를 dist/main 폴더에 넣습니다.

## 조작법

-   방향키: 이동
-   `Z`: 아무것도 선택안함
-   `F`: 낫 선택
-   `R`: 씨앗 선택
-   `Z`: 선택 해제
-   `D`: 선택 항목 사용
-   `S`: 삽 선택
-   `E`: 괭이 선택

## TODO

-   [ ] 뼛가루 추가 / 사용
-   [ ] 인벤토리 구현 (씨, 뼛가루 등 선택)

## 기여자

-   [newkincode](https://github.com/newkincode) - 메인테이너
-   [ky0422](https://github.com/ky0422) - `README.md` 작성, 그 외 버그 수정
