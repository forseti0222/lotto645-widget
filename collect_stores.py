# -*- coding: utf-8 -*-
"""
당첨 판매점 수집기
최신 회차부터 최근 N개 회차의 당첨 판매점 데이터를 수집한다.
결과: stores.json
"""

import json, os, time
from playwright.sync_api import sync_playwright

API_STORE = "https://www.dhlottery.co.kr/wnprchsplcsrch/selectLtWnShp.do?srchWnShpRnk=all&srchLtEpsd={}&srchShpLctn="
RESULT    = "https://www.dhlottery.co.kr/lt645/result"
OUT_JSON  = "stores.json"
KEEP_ROUNDS = 10  # 최근 N회차 보관
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def find_latest_round():
    if os.path.exists("lotto_data.json"):
        with open("lotto_data.json", encoding="utf-8") as f:
            data = json.load(f)
        if data:
            return max(d["no"] for d in data)
    return 1226


def load_existing():
    if os.path.exists(OUT_JSON):
        with open(OUT_JSON, encoding="utf-8") as f:
            return json.load(f)
    return {}


def fetch_stores(page, round_no):
    url = API_STORE.format(round_no)
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    body = page.inner_text("body").strip()
    if not body.startswith("{"):
        raise RuntimeError("JSON 아님: " + body[:80])
    result = json.loads(body)
    return result.get("data", {}).get("list", [])


def main():
    latest = find_latest_round()
    existing = load_existing()
    target_rounds = list(range(latest, max(0, latest - KEEP_ROUNDS), -1))

    print(f"최신 회차: {latest}회. 최근 {KEEP_ROUNDS}회차 수집...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(locale="ko-KR", user_agent=UA)
        page = ctx.new_page()

        print("세션 준비 중...")
        page.goto(RESULT, wait_until="networkidle", timeout=40000)
        time.sleep(1.0)

        for rno in target_rounds:
            key = str(rno)
            if key in existing:
                print(f"  {rno}회 — 캐시 사용")
                continue
            try:
                stores = fetch_stores(page, rno)
                existing[key] = stores
                print(f"  {rno}회 — {len(stores)}개 판매점 수집")
                time.sleep(0.5)
            except Exception as e:
                print(f"  {rno}회 오류: {e}")

        browser.close()

    # 최근 KEEP_ROUNDS개만 유지
    keep_keys = {str(r) for r in target_rounds}
    pruned = {k: v for k, v in existing.items() if k in keep_keys}

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(pruned, f, ensure_ascii=False, separators=(',', ':'))

    print(f"\n완료! {len(pruned)}개 회차 → {OUT_JSON}")


if __name__ == "__main__":
    main()
