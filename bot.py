import sys # 콘솔 출력에 사용 `sys.stdout.write()`
import datetime # 현재 날짜 가져오기에 사용
import requests as req # html 리스폰스 가져오기에 사용
from random import randint # 다양한 response를 위해 random 값 사용
from bs4 import BeautifulSoup # BeautifulSoup
blank = ' ' # define blank as ' '

def mealparse(date, weekday):
    '''
    지역별 교육청 웹사이트 링크
    서울특별시교육청 : stu.sen.go.kr
    부산광역시교육청 : stu.pen.go.kr
    대구광역시교육청 : stu.dge.go.kr
    인천광역시교육청 : stu.
    광주광역시교육청 : stu.
    대전광역시교육청 : stu.
    울산광역시교육청 : stu.
    세종특별자치시교육청 : stu.
    경기도교육청 : stu.goe.go.kr
    강원도교육청 : stu.
    충청북도교육청 : stu.
    충청남도교육청 : stu.
    전라북도교육청 : stu.
    전라남도교육청 : stu.
    경상북도교육청 : stu.
    경상남도교육청 : stu.
    제주특별자치도교육청 : stu.
    '''
    eduOfficeURL='stu.goe.go.kr' # 지역에 맞는 교육청 웹사이트 링크 값으로 수정하세요
    schulCode='J100006779' # 학교에 맞는 학교 코드 값으로 수정하세요
    '''
    01 : 유치원
    02 : 초등학교
    03 : 중학교
    04 : 고등학교
    '''
    schulKndScCode='03' # 학교 분류에 맞는 값으로 수정하세요
    URL = ( #URL = 교육청링크 + 급식페이지
            'http://' + eduOfficeURL + '/sts_sci_md01_001.do?' # 교육청 웹사이트
            'schulCode=' + schulCode + # 학교 코드
            '&schulCrseScCode=' + str(int(schulKndScCode)) + # 학교 분류 값을 1자리로 변환한 값
            '&schulKndScCode=' + schulKndScCode + # 학교 분류
            '&schMmealScCode=2' # 중식을 파싱해올꺼니까 값이 2
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

today_list = ['today', '오늘', '투데이'] # 오늘 급식 키워드가 저장된 배열입니다.
tommorow_list = ['내일', '다음날', 'tommorow'] #내일 급식 키워드가 저장된 배열입니다.
dayAfterTommorow_list = ['모레', '이틀', 'day after tommorow'] # 내일 모레 급식 키워드가 저장된 배열입니다.
yesterday_list = ['어제', '하루 전', 'yesterday'] # 어제 급식 키워드가 저장된 배열입니다.
dayBeforeYesterday_list = ['그제', '그저께', '이틀 전', 'day before yesterday'] # 그저께 급식 키워드가 저장된 배열입니다.
# 확인 우선순위는 '오늘 -> 모레 -> 내일'이므로 해당 순서에 맞게 검사문을 위치시킵니다.
exit_list = [
            '잘가', '뱌뱌', '빠이', 'ㅂㅂ', 'ㅂㅇ' , 'ㅃㅃ',
            'ㅃㅇ', '나가기', '종료', 'exit', 'quit'
] # 종료 키워드가 저장된 배열입니다.
while(1): #사용자가 exit_list에 있는 문자열을 포함하는 값을 입력하기 전까지는 무한 loop가 돌아갑니다.
    sys.stdout.write('\n') # 개행
    command = input('> ') # user input을 받음
    sys.stdout.write('\n') # 개행
    '''<종료> 키워드 체크'''
    # exit_list = ['잘가', '뱌뱌', '빠이', 'ㅂㅂ', 'ㅂㅇ' , 'ㅃㅃ', 'ㅃㅇ', '나가기', '종료', 'exit', 'quit']
    for exit_data in exit_list: # exit_list의 문자열이
        if command.lower().find(exit_data) > -1: # command에 포함될 경우
            sys.stdout.write('빠이빠이~\n')
            sys.exit() # 빠이빠이를 출력하고 종료합니다.
    days=False # 파싱할 데이터는 오늘로부터 days일 후의 데이터
    got_it=False # 며칠 후의 데이터를 파싱할 것인지의 여부가 결정되었는지를 나타냅니다.
    '''<오늘> 키워드 체크'''
    # today_list = ['today', '오늘', '투데이']
    for today_data in today_list: # today_list의 문자열이
        if command.lower().find(today_data) > -1: # command에 포함될 경우
            days = 0 # 현재 날짜의 급식 데이터를 파싱해오기 때문에 0일 후의 식단표를 가져오는 것이 됩니다.
            got_it = True # 며칠 후의 데이터를 파싱할 것인지 정했기 때문에 True로 설정합니다.
    '''<내일 모레> 키워드 체크'''
    # dayAfterTommorow_list = ['모레', '이틀', 'day after tommorow']
    if got_it is False: # 위에서 이미 며칠 후의 데이터를 파싱할 것인지 정해지지 않았다면(우선순위 체크)
        for dayAfterTommorow_data in dayAfterTommorow_list: # dayAfterTommorow_list의 문자열이
            if command.lower().find(dayAfterTommorow_data) > -1: # command에 포함될 경우
                days = 2 # 이틀 뒤의 식단표를 파싱해옵니다.
                got_it = True # 며칠 후의 데이터를 파싱할 것인지 정했기 때문에 True로 설정합니다.
    '''<내일> 키워드 체크'''
    # tommorow_list = ['내일', '다음날', 'tommorow']
    if got_it is False: # 위에서 이미 며칠 후의 데이터를 파싱할 것인지 정해지지 않았다면(우선순위 체크)
        for tommorow_data in tommorow_list: # today_list의 문자열이
            if command.lower().find(tommorow_data) > -1: # tommorow_list에 포함될 경우
                days = 1 # 1일 뒤의 식단표를 파싱해옵니다.
                got_it = True # 며칠 후의 데이터를 파싱할 것인지 정했기 때문에 True로 설정합니다.
    '''<어제> 키워드 체크'''
    # yesterday_list = ['어제', '하루 전', 'yesterday'] # 어제 급식 키워드가 저장된 배열입니다.
    if got_it is False: # 위에서 이미 며칠 후의 데이터를 파싱할 것인지 정해지지 않았다면(우선순위 체크)
        for yesterday_data in yesterday_list: # yesterday_list의 문자열이
            if command.lower().find(yesterday_data) > -1: # command에 포함될 경우
                days = -1 # 1일 전(-1일 후)의 식단표를 파싱해옵니다.
                got_it = True # 며칠 후의 데이터를 파싱할 것인지 정했기 때문에 True로 설정합니다.
    '''<그저께> 키워드 체크'''
    # dayBeforeYesterday_list = ['그제', '그저께', '이틀 전', 'day before yesterday'] # 그저께 급식 키워드가 저장된 배열입니다.
    if got_it is False: # 위에서 이미 며칠 후의 데이터를 파싱할 것인지 정해지지 않았다면(우선순위 체크)
        for dayBeforeYesterday_data in dayBeforeYesterday_list: # dayBeforeYesterday_list의 문자열이
            if command.lower().find(dayBeforeYesterday_data) > -1: # command에 포함될 경우
                days = -2 # 2일 전(-2일 후)의 식단표를 파싱해옵니다.
                got_it = True # 며칠 후의 데이터를 파싱할 것인지 정했기 때문에 True로 설정합니다.
    '''키워드 이외의 input을 받았을 경우'''
    if got_it is False: # 위에서 이미 며칠 후의 데이터를 파싱할 것인지 정해지지 않았다면(우선순위 체크)
        try:
            days=int(command)
            # 사용자가 입력한 데이터 전체가 정수값이 아닌지 확인합니다(그 정수가 그대로 days값이 됩니다).
        except ValueError: # 데이터 전체가 정수가 아니라면,
            try:
                days=int(command[0])
                # 사용자가 입력한 데이터의 맨 앞 문자가 정수가 아닌지 확인합니다(그 정수가 그대로 days값이 됩니다).
            except: # 사용자가 입력한 command의 첫 문자가 숫자가 아니라면
                days=0 # 그냥 오늘의 데이터를 가져옵니다.
        except IndexError: # 사용자가 공백을 입력
            days=0 # 그냥 오늘의 데이터를 가져옵니다.
    dt = datetime.datetime.today() + datetime.timedelta(days=days) # 현재 날짜에 days 이후의 값 -> 우리가 원하는 시간
    date = dt.strftime('%Y.%m.%d') # date(yyyy.mm.dd)
    day = dt.weekday()+1 # day는 날짜의 요일(월요일~일요일, 각각 0~6에 대응)
    lunch = mealparse(date, day) # 파싱 고고
    if days is not 0:
        if days < 0: # days가 음수이면
            sys.stdout.write("오늘로부터 %d일 전인,\n" % -days) # -n일 전
        else: #days가 양수이면
            sys.stdout.write("오늘로부터 %d일 후인,\n" % days) # n일 후
    sys.stdout.write(date[:4] + '년 ' + date[5:7] + '월 ' + date[8:10] + '일(')
    weekday = ['월', '화', '수', '목', '금', '토', '일']
    sys.stdout.write(weekday[day-1])
    sys.stdout.write('), 은여울중학교 급식 정보라구!\n') # 형식에 맞춰 출력
    sys.stdout.write('===============\n') # 구분선
    if lunch == blank or lunch == 'error': # 급식이 없거나(blank) 식단표 데이터가 없는 경우(error)
        sys.stdout.write('해당 날짜에는 급식이 없습니다.\n') # 급식이 없습니다 출력(히익)
        sys.stdout.write('===============\n') # 구분선
        rand = randint(1, 3) # 1~3 사이의 값을 가지는 난수(랜덤) 값 생성
        if rand == 1: # 생성한 난수값이 1
            sys.stdout.write('안돼... 급식이 없어!..부들,,부들\n') # 1번째 경우
        elif rand == 2: # 생성한 난수값이 2
            sys.stdout.write('씌익,,씌이익, 급식이 왜 없는 건데에\n') # 2번째 경우
        else: # 생성한 난수값이 3(not 1 nor 2)
            sys.stdout.write('ㄱ...그,급식이 없다고요...??\n') # 3번째 경우
    else:
        sys.stdout.write(lunch) # 식단 출력
        sys.stdout.write('===============\n') # 구분선
        sys.stdout.write('빠알리 급식 주세요. 현기증 난단 말이예요.\n') # 현기증 출력
