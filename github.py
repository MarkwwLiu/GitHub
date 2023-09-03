import requests
from datetime import datetime, timedelta
import os

def get_merged_pr_branches_and_titles(owner, repo, since_timestamp):
    # 使用 GitHub API 查詢已合併的 PR 資訊
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&since={since_timestamp}"
    response = requests.get(url)
    prs = response.json()

    merged_pr_info = []
    for pr in prs:
        if pr.get("merged_at"):
            pr_info = {
                "branch": pr["head"]["ref"],  # 取得分支名稱
                "title": pr["title"],  # 取得 PR 標題
                "pr_link": pr["html_url"]  # 取得 PR 的連結
            }
            merged_pr_info.append(pr_info)

    return merged_pr_info

def save_pr_info_to_file(file_path, pr_info):
    # 將 PR 資訊寫入檔案
    with open(file_path, "w") as file:
        for info in pr_info:
            file.write(f"{info['branch']}|{info['title']}|{info['pr_link']}\n")

def read_previous_pr_info(file_path):
    # 從檔案中讀取之前的 PR 資訊
    previous_info = []
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip('\n').split('|')
                if len(parts) == 3:
                    info = {"branch": parts[0], "title": parts[1], "pr_link": parts[2]}
                    previous_info.append(info)
    return previous_info

def main():
    owner = "XXX"
    repo = "test"

    # 設定上次 git pull 的時間點（90 天前）
    since_timestamp = (datetime.now() - timedelta(days=90)).isoformat()

    merged_pr_info = get_merged_pr_branches_and_titles(owner, repo, since_timestamp)

    previous_info_path = "previous_merged_pr_info.txt"
    previous_info = read_previous_pr_info(previous_info_path)

    new_info = []
    for pr_info in merged_pr_info:
        info = {"branch": pr_info["branch"], "title": pr_info["title"], "pr_link": pr_info["pr_link"]}
        new_info.append(info)

    # 儲存新資訊到檔案中
    save_pr_info_to_file(previous_info_path, new_info)

    # 找出新增的分支
    added_info = [info for info in new_info if info not in previous_info]

    print("新增的分支:")
    for info in added_info:
        print(f"branch:{info['branch']}\nPR 標題: {info['title']}\nPR Link: {info['pr_link']}\n")

if __name__ == "__main__":
    main()
