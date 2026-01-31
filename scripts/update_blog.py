import requests
import os
import re

# 설정
USERNAME = 'kik328288'  # 본인 Velog 아이디
BASE_DIR = 'velog-posts' # 저장할 최상위 폴더

# 폴더가 없으면 생성
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

# 파일명에 사용할 수 없는 문자 제거 함수
def clean_filename(title):
    return re.sub(r'[\/:*?"<>|]', '_', title)

# Velog GraphQL API 호출 함수
def fetch_velog_posts(username):
    url = 'https://v2cdn.velog.io/graphql'
    query = """
    query Posts($username: String!, $cursor: ID) {
      posts(username: $username, cursor: $cursor, limit: 50) {
        id
        title
        body
        released_at
        url_slug
        series {
          name
        }
      }
    }
    """
    
    posts = []
    cursor = None

    print("Fetching posts from Velog...")
    while True:
        variables = {'username': username, 'cursor': cursor}
        response = requests.post(url, json={'query': query, 'variables': variables})
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        data = response.json().get('data', {}).get('posts', [])
        
        if not data:
            break
            
        posts.extend(data)
        cursor = data[-1]['id'] # 다음 페이지를 위한 커서 설정
        
    print(f"Total posts fetched: {len(posts)}")
    return posts

def main():
    posts = fetch_velog_posts(USERNAME)
    
    # 현재 존재하는 파일 목록 수집 (삭제 처리를 위함)
    existing_files = set()
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith('.md'):
                # 전체 경로를 저장
                full_path = os.path.join(root, file)
                existing_files.add(full_path)

    # 이번에 생성/업데이트된 파일 목록
    processed_files = set()

    for post in posts:
        # 시리즈 확인
        series_name = post['series']['name'] if post['series'] else 'Etc' # 시리즈 없으면 Etc 폴더로
        
        # 시리즈명으로 폴더 생성
        series_dir = os.path.join(BASE_DIR, clean_filename(series_name))
        if not os.path.exists(series_dir):
            os.makedirs(series_dir)

        # 파일명 및 경로 설정
        file_name = f"{clean_filename(post['title'])}.md"
        file_path = os.path.join(series_dir, file_name)
        
        # 파일 내용 작성
        content = f"""# {post['title']}

**Published:** {post['released_at']}
**Link:** https://velog.io/@{USERNAME}/{post['url_slug']}

---

{post['body']}
"""
        
        # 파일 쓰기 (기존 파일이 있어도 덮어쓰기 -> 수정 내용 반영됨)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        processed_files.add(file_path)

    # 삭제 처리: 기존 파일 중 이번에 처리되지 않은 파일 삭제 (Velog에서 삭제된 글)
    for old_file in existing_files:
        if old_file not in processed_files:
            print(f"Deleting removed post: {old_file}")
            os.remove(old_file)
            
            # 빈 폴더 정리
            folder = os.path.dirname(old_file)
            if not os.listdir(folder): # 폴더가 비었으면 삭제
                os.rmdir(folder)

    print("Blog update complete.")

if __name__ == '__main__':
    main()
