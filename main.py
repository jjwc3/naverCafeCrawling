"""
사용법
아무 글이나 들어가서 개발자도구 - Network 들어가서 페이지 새로고침 한 번 해주고(넾캍은 동적 페이지라 게시글 URL로 접속해야 함)
Filter: Fetch/XHR 선택하고 뜨는 것들 중 숫자로 시작하는 것 클릭
Headers에 Request URL이 게시글 정보 담은 링크
링크에서 cafes 뒤에 있는 숫자가 cafeId, articles 뒤에 있는 숫자가 articleId임.
이 방식대로 첫번째 글이랑 마지막 글 articleId 확인
Chrome Webstore에서 Export cookie JSON file for Puppeteer 설치 후 경로 입력
JSON 형식: [{name:"name1",value:"value1",...},{name:"name2",value:"value2",...},...]

엑셀에서 데이터 불러올 때 Data - Get Data - JSON으로 파일 불러오고, Parse - JSON 후 To Table - Close & load
"""
import requests
import matplotlib.pyplot as plt
import json
from datetime import datetime


cafeId = 29844827
articleId = 88600
with open(input("Cookies Path: "), 'r') as f:
    cookies_before = json.load(f)
cookies:dict = {}
for i in cookies_before:
    cookies[i["name"]] = i["value"]
print(cookies)
latestArticleId = int(input("Latest ArticleId: "))
# cookies = {
#     "BUC": "DJ3N~~~",
#     "NAC": "u7u~~~~",
#     "NACT": "1",
#     "NID_AUT": "Nnu~~~",
#     "NID_JKL": "oIo~~~",
#     "NID_SES": "AAABgI82G~~~",
#     "NNB": "LB~~~",
#     "SRT30": "17~~~",
#     "SRT5": "17~~~",
#     "_ga": "GA1.2.1~~~",
#     "_ga_6Z6DP60WFK": "GS1.2.17~~",
#     "nid_inf": "1~~~",
#     "perf_dv6Tr4n": "1"
# }



# ogq_origin = "ogq_627c80ea90e91-"

ogq_name=["우하잉하", "ㅇㄱㅇ", "따봉", "끄덕끄덕", "잉모노자나", "으아앙아아아", "점령", "커트", "공지", "ㅋ", "어라랍스타", "ㅊㅋㅊㅋ", "환영합니다", "?", "@우정잉", "초롱", "하트", "귀여워", "먹이금지", "오오오", "헤롱", "경멸", "우바잉바", "점점점"]

result = {char: 0 for char in ogq_name}

for currentArticleId in range(articleId, latestArticleId + 1):
    # 아래 url은 댓글 전체가 안 나옴, 대신 commentCount로 페이지 수 세기 위해 GET 요청
    try:
        base_url = f"https://apis.naver.com/cafe-web/cafe-articleapi/v3/cafes/{cafeId}/articles/{currentArticleId}"
        res1 = requests.get(base_url, cookies=cookies).json()
        page_count = res1["result"]["article"]["commentCount"] // 100 + 1
    except:
        print("Cookies Invalid or Article Not Exist : Pass")
        continue

    try:
        for page in range(1, page_count+1):
            # 이게 댓글 전체 다 나옴, 페이지별로 100개씩
            url = f"https://apis.naver.com/cafe-web/cafe-articleapi/v2/cafes/{cafeId}/articles/{currentArticleId}/comments/pages/{page}?requestFrom=A&orderBy=asc"
            res2 = str(requests.get(url, cookies=cookies).json())
            # print(response)
            for j, char in enumerate(ogq_name, start=1):
                pattern = f"ogq_627c80ea90e91-{j}-"
                result[char] += res2.count(pattern)
            # print(res2.count("ogq_627c80ea90e91-"))
    except:
        print("An Error Occured : Pass")
        pass

print(result)
result_json = json.dumps(result, ensure_ascii=False)
now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

with open(f'{now}_from_{articleId}_to_{latestArticleId}.json','w', encoding="UTF-8") as f:
    json.dump(result_json, f, ensure_ascii=False)

open_pyplot = input("Open Pyplot Graph? (Y/else): ")
if open_pyplot in ['Y', 'y']:
    # 키와 값 분리
    labels = list(result.keys())
    values = list(result.values())

    # 그래프 그리기
    plt.rc('font', family="AppleGothic")
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(12, 6))
    plt.bar(labels, values, color='skyblue', edgecolor='black')



    # 제목과 레이블 설정
    plt.title('데이터의 막대형 그래프', fontsize=16)
    plt.xlabel('항목', fontsize=12)
    plt.ylabel('값', fontsize=12)

    # X축 레이블 회전
    plt.xticks(rotation=45, ha='right', fontsize=10)

    # 그래프 표시
    plt.tight_layout()  # 레이아웃 자동 조정
    plt.show()