# 오르빗 익스플로러 인터프리터
오르빗 익스플로러를 좀 더 보기 쉽게 변환해서 보여주는 파이썬 스크립트입니다.<br>
python orbit_interpreter.py 로 실행 후 TxID 를 입력하시면 사용자가 보기 편안한 Event Log로 변환되서 출력시킵니다.<br>
Selenium을 이용하므로 사전에 chrome webdriver가 c:\webdriver에 설치되어 있어야 합니다.<br>
https://chromedriver.chromium.org/downloads<br>
<br>
설치 상세방법<br>
- Python을 설치해주세요.<br>
PATH는 자동으로 설정되도록 옵션 선택해주세요.
https://www.python.org/downloads/
- 하기 chrome webdriver 다운로드 페이지에서 크롬에 맞는 버전을 다운로드 하세요.
https://chromedriver.chromium.org/downloads
위 압축파일을 받은 뒤 c:\webdriver 폴더를 생성 후에 webdriver.exe 파일을 추가해주세요.
- cmd (명령프롬프트) 실행, 필요한 추가 라이브러리를 설치합니다.<br>
pip install selenium<br>
pip install beautifulsoup4
- cmd에서 python orbit_interpreter.py로 실행
<br>혹은 python IDLE - orbit_interpreter.py 를 불러오기 해서 실행
