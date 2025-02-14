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

# '따봉' 관련 데이터를 저장할 딕셔너리
dabong_data = {}


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
    """게시글의 댓글을 확인하여 '따봉' 개수를 체크하는 함수"""
    comment_count = await fetch_article_comment_count(session, article_id)
    page_count = (comment_count // 100) + 1

    tasks = [fetch_comments(session, article_id, page) for page in range(1, page_count + 1)]
    responses = await asyncio.gather(*tasks)

    # '따봉' 관련 패턴
    pattern = "ogq_627c80ea90e91-3-"  # 따봉은 리스트에서 3번째
    dabong_count = sum(res.count(pattern) for res in responses)

    if dabong_count > 0:
        dabong_data[article_id] = dabong_count


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [process_article(session, article_id) for article_id in range(articleId, latestArticleId + 1)]
        await tqdm.gather(*tasks)

asyncio.run(main())

# 'articleId' 내림차순 정렬
sorted_dabong_data = dict(sorted(dabong_data.items(), key=lambda x: x[0], reverse=True))

# JSON 파일로 저장
now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
filename = f"{now}_dabong_data.json"

with open(filename, 'w', encoding="UTF-8") as f:
    json.dump(sorted_dabong_data, f, ensure_ascii=False, indent=4)

print(f"\n===== 따봉 댓글이 있는 게시글 목록 (내림차순) =====")
for article_id, count in sorted_dabong_data.items():
    print(f"게시글 ID: {article_id}, 따봉 개수: {count}")

print(f"\n데이터가 {filename} 파일로 저장되었습니다.")
