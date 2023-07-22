# 농사 게임
![](https://capsule-render.vercel.app/api?type=waving&color=0:feac5e,50:c779d0,100:4bc0c8&height=300&section=header&text=Simple%20Farming%20Game&desc=Let%27s%20farm%20everything!&fontColor=fff)
모든걸 농사짓자!

## 설치

```console
$ pip install pipenv
$ git clone https://github.com/newkincode/simple_farming_game.git
$ cd simple_farming_game
$ pipenv shell
$ pipenv sync

$ python main.py
```

## 빌드

```console
> ./build.bat
```
```console
$ sh ./build.sh
```
이후 lib폴더와 assets 폴더와 data폴더를 build폴더 안 main폴더에 넣어줍니다(복사 붙여넣기)

## 이모지 사용법
> <이모지 이름><br>
> 이렇게 사용합니다<br>
> 현재 이모지 리스트<br>

> -   `smile`<br>
> -   `angry`<br>

>보더 텍스트라면 어디서든 사용가능하며<br>
> 한 매시지 안에 여러 이모지는 사용이 불가능 합니다<br>
> 예시: <br>
> `hello <smile> asdfsd` 가능<br>
> `hello <smile><smile>` 불가능<br>
> `hello <smile><angry>` 불가능<br>

## 조작법

-   `방향키`: 이동
-   `SPACE`: 달리기
-   `Z`: 선택 해제
-   `D`: 선택 항목 사용
-   `G`: 아이템 정보
-   `A`: 판매
-   `B`: 구매
-   `H`: 도움말
-   `K`: 저장
-   `L`: 불러오기
-   `M`: 블록 선택
-   `N`: 채팅
-   `숫자`: 아이템 선택 <br>
맥북의 경우 영어로 선택된 상태에서 게임을 플래이 해주세요
## TODO

-   [ ] 얼마나 자랐는지 표시
-   [ ] 얼마후에 썩는지 표시
-   [ ] 아이템 선택시 플래이어가 들고있는 이미지로 변경
-   [ ] 스크롤로 아이템 바꾸기
-   [ ] 클릭 인벤토리
-   [ ] 상자에 아이템 넣어서 판매
-   [ ] 도전과제 만들기
-   [ ] 상자 제작

## 기여자

-   [newkincode](https://github.com/newkincode) - 메인테이너
-   [ky0422](https://github.com/ky0422) - `README.md` 작성, 그 외 버그 수정
-   [kdh8219](https://github.com/kdh8219) - 코드 리팩터링, 첫번째 관심자
-   [copilot](https://github.com/features/copilot) - 코드 작성 도우미