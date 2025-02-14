import aiohttp
import asyncio
import json
from datetime import datetime
from tqdm.asyncio import tqdm

# 카페 및 게시글 정보 입력
cafeId = 29844827
articleId = 88600
latestArticleId = int(input("Latest ArticleId: "))

# 쿠키 불러오기
with open(input("Cookies Path: "), 'r') as f:
    cookies_before = json.load(f)

cookies = {i["name"]: i["value"] for i in cookies_before}

# ogq 데이터
ogq_name = ["우하잉하", "ㅇㄱㅇ", "따봉", "끄덕끄덕", "잉모노자나", "으아앙아아아", "점령", "커트", "공지", "ㅋ", "어라랍스타", "ㅊㅋㅊㅋ", "환영합니다", "?", "@우정잉", "초롱", "하트", "귀여워", "먹이금지", "오오오", "헤롱", "경멸", "우바잉바", "점점점"]
result = {char: 0 for char in ogq_name}


async def fetch_article_comment_count(session, article_id):
    """게시글의 댓글 개수를 가져오는 함수"""
    url = f"https://apis.naver.com/cafe-web/cafe-articleapi/v3/cafes/{cafeId}/articles/{article_id}"
    try:
        async with session.get(url, cookies=cookies) as response:
            data = await response.json()
            return data["result"]["article"]["commentCount"]
    except Exception:
        return 0  # 오류 시 0 반환


async def fetch_comments(session, article_id, page):
    """댓글 데이터를 가져오는 함수"""
    url = f"https://apis.naver.com/cafe-web/cafe-articleapi/v2/cafes/{cafeId}/articles/{article_id}/comments/pages/{page}?requestFrom=A&orderBy=asc"
    try:
        async with session.get(url, cookies=cookies) as response:
            return await response.text()
    except Exception:
        return ""  # 오류 발생 시 빈 문자열 반환


async def process_article(session, article_id):
    """게시글의 댓글을 처리하는 함수"""
    comment_count = await fetch_article_comment_count(session, article_id)
    if comment_count % 100 == 0:
        page_count = (comment_count // 100)
    else:
        page_count = (comment_count // 100) + 1
    

    tasks = [fetch_comments(session, article_id, page) for page in range(1, page_count + 1)]
    responses = await asyncio.gather(*tasks)

    for res in responses:
        for j, char in enumerate(ogq_name, start=1):
            pattern = f"ogq_627c80ea90e91-{j}-"
            result[char] += res.count(pattern)


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [process_article(session, article_id) for article_id in range(articleId, latestArticleId + 1)]
        await tqdm.gather(*tasks)


asyncio.run(main())

# 결과 저장
result_json = json.dumps(result, ensure_ascii=False)
now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
with open(f'{now}_from_{articleId}_to_{latestArticleId}.json', 'w', encoding="UTF-8") as f:
    json.dump(result_json, f, ensure_ascii=False)

print(result)
