import sys # 콘솔 출력에 사용 `sys.stdout.write()`
import datetime # 현재 날짜 가져오기에 사용
import requests as req # html 리스폰스 가져오기에 사용
from random import randint # 다양한 response를 위해 random 값 사용
from bs4 import BeautifulSoup # BeautifulSoup
blank = ' ' # define blank as ' '

def mealparse(date, weekday, eduOfficeURL, schulCode, schulKndScCode, schMmealScCode): # 학교 급식 파싱 함수
    # 인수 : 급식 파싱할 날짜 (yyyy .mm.dd), 해당 학교가 위치한 지역의 교육청 링크, 해당 학교 코드, 해당 학교 구분 코드, 파싱할 급식 종류(조식/중식/석식)
    '''
    <지역별 교육청 웹사이트 링크 (eduOfficeURL)>
    서울특별시교육청 : stu.sen.go.kr
    부산광역시교육청 : stu.pen.go.kr
    대구광역시교육청 : stu.dge.go.kr
    인천광역시교육청 : stu.ice.go.kr
    광주광역시교육청 : stu.gen.go.kr
    대전광역시교육청 : stu.dje.go.kr
    울산광역시교육청 : stu.use.go.kr
    세종특별자치시교육청 : stu.sje.go.kr
    경기도교육청 : stu.goe.go.kr
    강원도교육청 : stu.kwe.go.kr
    충청북도교육청 : stu.cbe.go.kr
    충청남도교육청 : stu.cne.go.kr
    전라북도교육청 : stu.jbe.co.kr
    전라남도교육청 : stu.jne.go.kr
    경상북도교육청 : stu.kbe.go.kr
    경상남도교육청 : stu.gne.go.kr
    제주특별자치도교육청 : stu.jje.go.kr

    <학교 종류 코드 (schulKndScCode)>
    01 : 유치원
    02 : 초등학교
    03 : 중학교
    04 : 고등학교

    <급식 종류 코드 (schMmealScCode)>
    조식(아침) : 1
    중식(점심) : 2
    석식(저녁) : 3
    '''
    URL = ( #URL = 교육청링크 + 급식페이지
            'http://' + eduOfficeURL + '/sts_sci_md01_001.do?' # 교육청 웹사이트
            'schulCode=' + schulCode + # 학교 코드
            '&schulCrseScCode=' + str(int(schulKndScCode)) + # 학교 분류 값을 1자리로 변환한 값
            '&schulKndScCode=' + schulKndScCode + # 학교 분류
            '&schMmealScCode=' + str(schMmealScCode) + # 급식 종류
            '&schYmd=' + date # date는 'yyyy.mm.dd' 형식의 string-type data
    )
    #print(URL) # 디버깅에 사용
    html = req.get(URL).text # 생성한 URL의 html 저장
    soup = BeautifulSoup(html, 'html.parser') # BeautifulSoup 객체 생성
    data = soup.find_all('tr')[2].find_all('td') # 식단표 부분 데이터만 찾아서 저장
    #print(data) # 디버깅에 사용
    try: # 급식이 없는 경우 공백(blank)을 리턴
        data = data[day] # 요청받은 요일의 데이터만 가져옴
        data = str(data) # <class 'bs4.data.Tag'>에서 <class 'str'>로 type 바꿈
        filter_list = ['[', ']', '<td class="textC">', '<td class="textC last">', '</td>', '.'] # 필터 리스트
        # 읽은 html에서 필요없는 부분 삭제
        for filter_data in filter_list:
            data = data.replace(filter_data, '') # 필터에 걸리는 내용 삭제
        data = data.replace('<br/>', '\n') # 줄바꿈
        data = ''.join(i for i in data if not i.isdigit()) # 숫자(알레르기 표시) 삭제
    except: # 식단표 데이터가 없는 등 에러가 발생하게 되면 요일의 데이터에서 IndexError가 발생
        data = 'error' # 함수가 error를 리턴하도록 함
    return data # 식단 데이터를 리턴(반환)합니다.
