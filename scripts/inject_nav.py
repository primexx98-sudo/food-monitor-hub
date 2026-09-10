"""docs/trend/(index.html + dashboard_*.html), docs/law/index.html에 공용 네비게이션 바를 삽입합니다."""

import glob
import os

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
NAV_PATH = os.path.join(REPO_ROOT, "docs", "nav_snippet.html")

TRENDS_DIR = os.path.join(REPO_ROOT, "docs", "trend")
TREND_TARGETS = [os.path.join(TRENDS_DIR, "index.html")] + glob.glob(
    os.path.join(TRENDS_DIR, "dashboard_*.html")
)
LAW_TARGETS = [os.path.join(REPO_ROOT, "docs", "law", "index.html")]
STATUTE_TARGETS = [os.path.join(REPO_ROOT, "docs", "statute", "index.html")]

TARGETS = TREND_TARGETS + LAW_TARGETS + STATUTE_TARGETS

NAV_ACTIVE_KEYS = {path: "trend" for path in TREND_TARGETS}
NAV_ACTIVE_KEYS.update({path: "law" for path in LAW_TARGETS})
NAV_ACTIVE_KEYS.update({path: "statute" for path in STATUTE_TARGETS})


def build_nav(active_key):
    with open(NAV_PATH, encoding="utf-8") as f:
        nav_html = f.read()
    marker = f'data-hub-key="{active_key}"'
    # 2026-09-10: padding/text-decoration은 nav_snippet.html의 공용 클래스(#hub-nav a)로
    # 이관됨(모바일 반응형 padding 적용을 위해) — 여기서는 활성 탭에서만 달라지는
    # 속성(색상/굵기/밑줄)만 인라인으로 덧붙인다.
    active_style = 'color:#fff;font-weight:700;border-bottom:2px solid #52b788;'
    return nav_html.replace(
        marker, f'{marker} style="{active_style}"'
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
