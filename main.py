"""
사용법
아무 글이나 들어가서 개발자도구 - Network 들어가서 페이지 새로고침 한 번 해주고(넾캍은 동적 페이지라 게시글 URL로 접속해야 함)
Filter: Fetch/XHR 선택하고 뜨는 것들 중 숫자로 시작하는 것 클릭
Headers에 Request URL이 게시글 정보 담은 링크
링크에서 cafes 뒤에 있는 숫자가 cafeId, articles 뒤에 있는 숫자가 articleId임.
이 방식대로 첫번째 글이랑 마지막 글 articleId 확인
그 링크에 접속해서 다시 network에서 articleId랑 일치하는거 들어가서 Cookies 들어가면 쿠키 나옴.
걔네들 하나하나 복붙해서 JSON 파일로 저장해서 불러오거나(코드 구현 안함) 아래처럼 텍스트로 붙여넣기(value 숫자 허용 안됨. 숫자값도 쌍따옴표 씌워서)
"""
import requests
import matplotlib.pyplot as plt


cafeId = 29844827
articleId = 88600
latestArticleId = int(input("Latest ArticleId: "))
cookies = {
    "BUC": "DJ3NcOd3TzDkV00M2WI0qLqJdyVuZp2ZVvzVJzSvlFs=",
    "NAC": "u7udBcAVmehsA",
    "NACT": "1",
    "NID_AUT": "NnuoweclFZ7H3YuYtXmwiLJcKLqvYahTemSQvvrEhcx04lzOf+GvokDVGFXDo8YS",
    "NID_JKL": "oIoUYgjhy9BMrlOdeZ3m2nFQE9YB3nIESDDdMq6/K0U=",
    "NID_SES": "AAABgI82GSMAcSQCytfaRLc97MQDtWB7ijsxsnScrZl8q+Gre6Hj9iwinHs31tGlq4OAbA1mxSHjmKhtL+OZVSAgXnJ62tNrR/tU/r9IsL/yHRlkVjM0HZLu81Bf45cQXgk4Uk3a6Mf+Cf1ddduExy5JgAkGTcWuJJxUjVyElcRjmK6NYf38kUkmYh198pgTEiD/W5RJBnwMyuEpPZrEJQT/Jqj9ScYbWRHZly7Qq6YpkE/c06i/n4s5zF0F/H9j/GsrV5qqyWIttWwHeS43xzGOJDRyQH7idKJVHbZjsTtIx/hsiTrRVxla3kIZVK1B8DTZW2wEqXTaR5E5KMjiPRM6UKJ3CfemhWErQ7Ecvn3mUCvU4UxTL1dJr2BjKf9hjLvNp8c04PvZAp8AIh4/0FzdkCTaGIlGa+fFqOm9JBwyLs5K5Ic+h/f6kPi6RXoeKT0+pnorgGczG4F5Wi4KlDDBkrNzAPPIjSMaVETWAMd3olch4hrWvFLrP21kQypzanZPKQ==",
    "NNB": "LBM7FMANTW6GK",
    "SRT30": "1735566894",
    "SRT5": "1735568238",
    "_ga": "GA1.2.1790064785.1707654851",
    "_ga_6Z6DP60WFK": "GS1.2.1707654851.1.0.1707654851.60.0.0",
    "nid_inf": "101025269",
    "perf_dv6Tr4n": "1"
}

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
        print("Article Not Exist : Pass")
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
        print("An Error Occured")
        pass

print(result)



# 키와 값 분리
labels = list(result.keys())
values = list(result.values())

# 그래프 그리기
# plt.rcParams['font.family'] = "AppleGothic"
plt.rc('font', family="AppleGothic")
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