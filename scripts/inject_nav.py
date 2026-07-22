"""docs/trend/index.html, docs/law/index.html에 공용 네비게이션 바를 삽입합니다."""

import os

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
NAV_PATH = os.path.join(REPO_ROOT, "docs", "nav_snippet.html")
TARGETS = [
    os.path.join(REPO_ROOT, "docs", "trend", "index.html"),
    os.path.join(REPO_ROOT, "docs", "law", "index.html"),
]

NAV_ACTIVE_KEYS = {
    os.path.join(REPO_ROOT, "docs", "trend", "index.html"): "trend",
    os.path.join(REPO_ROOT, "docs", "law", "index.html"): "law",
}


def build_nav(active_key):
    with open(NAV_PATH, encoding="utf-8") as f:
        nav_html = f.read()
    marker = f'data-hub-key="{active_key}"'
    active_style = 'color:#fff;font-weight:700;border-bottom:2px solid #52b788;'
    return nav_html.replace(
        marker, f'{marker} style="padding:10px 18px;text-decoration:none;{active_style}"'
    )


def inject(path):
    if not os.path.exists(path):
        print(f"건너뜀 (파일 없음): {path}")
        return
    with open(path, encoding="utf-8") as f:
        html = f.read()

    if 'id="hub-nav"' in html:
        print(f"이미 삽입됨, 건너뜀: {path}")
        return

    if "<body>" not in html:
        print(f"<body> 태그를 찾을 수 없음: {path}")
        return

    nav_html = build_nav(NAV_ACTIVE_KEYS[path])
    html = html.replace("<body>", f"<body>\n{nav_html}", 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"네비게이션 삽입 완료: {path}")


if __name__ == "__main__":
    for target in TARGETS:
        inject(target)
