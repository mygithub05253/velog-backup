import feedparser
import os
import re

# 본인 Velog RSS 피드 URL
rss_url = 'https://api.velog.io/rss/@kik328288'

# 'velog-posts' 라는 이름의 게시글 저장 폴더 경로
posts_dir = 'velog-posts'

# 'velog-posts' 폴더가 없다면 생성
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

# RSS 피드 파싱
print(f"Fetching RSS feed from {rss_url}")
feed = feedparser.parse(rss_url)

if feed.bozo:
    print(f"Error parsing RSS feed: {feed.bozo_exception}")
else:
    print(f"Found {len(feed.entries)} posts. Processing...")
    # 각 게시글을 .md 파일로 저장
    for entry in feed.entries:
        # 파일 이름으로 사용할 수 없는 문자들을 '_'로 변경
        file_name = re.sub(r'[\/:*?"<>|]', '_', entry.title) + '.md'
        file_path = os.path.join(posts_dir, file_name)

        # 파일이 이미 존재하지 않을 경우에만 새로 생성
        if not os.path.exists(file_path):
            print(f"Creating new post file: {file_name}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {entry.title}\n\n")
                f.write(f"**Published:** {entry.published}\n")
                f.write(f"**Link:** {entry.link}\n\n")
                f.write("---\n\n")
                f.write(entry.description)
        else:
            print(f"Skipping existing post: {file_name}")

print("Blog post update process finished.")