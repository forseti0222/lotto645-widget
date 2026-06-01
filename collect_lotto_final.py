# -*- coding: utf-8 -*-
"""
로또 6/45 전체 회차 수집기 (최종판)
==================================================
개편된 동행복권의 새 JSON API(selectPstLt645InfoNew.do)를 사용.
당첨번호·보너스·1~5등 인원/당첨금·이월·판매액을 모두 수집한다.

[설치]  (이미 했다면 생략)
    pip install playwright
    python -m playwright install chromium

[실행]
    python collect_lotto_final.py

[결과]
    lotto_data.json  /  lotto_data.js   (위젯 LOTTO_DATA 에 붙여넣기)
    이미 받은 회차는 건너뛰므로, 매주 토요일 다시 실행하면 새 회차만 추가됨.
"""

import json, os, time
from playwright.sync_api import sync_playwright

API    = "https://www.dhlottery.co.kr/lt645/selectPstLt645InfoNew.do?srchDir=center&srchLtEpsd={}"
RESULT = "https://www.dhlottery.co.kr/lt645/result"
OUT_JSON, OUT_JS = "lotto_data.json", "lotto_data.js"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def fmt_date(ymd):
    s = str(ymd)
    return "{}-{}-{}".format(s[:4], s[4:6], s[6:8]) if len(s) == 8 else s


def parse_item(it):
    """API 항목 1개 → 위젯이 쓰는 형식으로 변환"""
    return {
        "no":   it["ltEpsd"],
        "date": fmt_date(it["ltRflYmd"]),
        "nums": [it["tm1WnNo"], it["tm2WnNo"], it["tm3WnNo"],
                 it["tm4WnNo"], it["tm5WnNo"], it["tm6WnNo"]],
        "bonus": it["bnsWnNo"],
        "sell":  it["wholEpsdSumNtslAmt"],
        "ranks": [
            {"co": it["rnk1WnNope"], "amt": it["rnk1WnAmt"]},
            {"co": it["rnk2WnNope"], "amt": it["rnk2WnAmt"]},
            {"co": it["rnk3WnNope"], "amt": it["rnk3WnAmt"]},
            {"co": it["rnk4WnNope"], "amt": it["rnk4WnAmt"]},
            {"co": it["rnk5WnNope"], "amt": it["rnk5WnAmt"]},
        ],
    }


def call_api(page, epsd):
    """지정 회차 기준 묶음 데이터(list)를 받아온다."""
    page.goto(API.format(epsd), wait_until="domcontentloaded", timeout=40000)
    body = page.inner_text("body").strip()
    if not body.startswith("{"):
        raise RuntimeError("JSON 아님(차단/오류). 앞부분: " + body[:120])
    return json.loads(body)["data"]["list"]


def find_latest(page):
    """최신 회차 자동 탐지: 아주 큰 회차를 요청해 list에서 최대값을 취함."""
    for guess in (9999, 2000, 1300):
        try:
            lst = call_api(page, guess)
            if lst:
                return max(it["ltEpsd"] for it in lst)
        except Exception:
            continue
    return 1226  # 탐지 실패 시 안전 기본값(필요시 수동 조정)


def load_existing():
    if os.path.exists(OUT_JSON):
        with open(OUT_JSON, encoding="utf-8") as f:
            return {d["no"]: d for d in json.load(f)}
    return {}


def save(records):
    data = sorted(records.values(), key=lambda x: x["no"], reverse=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    lines = ["  var LOTTO_DATA = ["]
    for d in data:
        rk = ",".join("{{co:{},amt:{}}}".format(r["co"], r["amt"]) for r in d["ranks"])
        lines.append("    {{no:{no}, date:\"{date}\", nums:{nums}, bonus:{bonus}, "
                     "sell:{sell}, ranks:[{rk}]}},".format(
                         no=d["no"], date=d["date"], nums=d["nums"],
                         bonus=d["bonus"], sell=d["sell"], rk=rk))
    lines.append("  ];")
    with open(OUT_JS, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    records = load_existing()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(locale="ko-KR", user_agent=UA)
        page = ctx.new_page()

        print("세션 준비 중...")
        page.goto(RESULT, wait_until="networkidle", timeout=40000)
        time.sleep(1.2)

        latest = find_latest(page)
        print("최신 회차: {}회. 수집 시작...".format(latest))

        # 1차 패스: 최신부터 내려가며, 미수집 회차만 요청(응답 묶음 전부 병합)
        no = latest
        while no >= 1:
            if no in records:
                no -= 1; continue
            try:
                lst = call_api(page, no)
            except Exception as e:
                print("  [{}회] 오류: {} (2초 후 재시도)".format(no, e))
                time.sleep(2); page.goto(RESULT); time.sleep(1); continue
            for it in lst:
                records[it["ltEpsd"]] = parse_item(it)
            got = parse_item(lst[0]) if lst else None
            print("  ~{}회 묶음 수신 ({}건 누적)".format(no, len(records)))
            if no % 60 == 0:
                save(records)
            no -= 1
            time.sleep(0.4)

        # 2차 패스: 혹시 빠진 회차 보정
        missing = [e for e in range(1, latest + 1) if e not in records]
        if missing:
            print("누락 {}건 보정 중: {}...".format(len(missing), missing[:10]))
            for m in missing:
                for off in (0, 3, 6, 9):
                    try:
                        lst = call_api(page, m + off)
                        for it in lst:
                            records[it["ltEpsd"]] = parse_item(it)
                        if m in records:
                            break
                    except Exception:
                        pass
                    time.sleep(0.4)

        browser.close()

    save(records)
    miss2 = [e for e in range(1, latest + 1) if e not in records]
    print("\n완료! 총 {}개 회차 → {}, {}".format(len(records), OUT_JSON, OUT_JS))
    if miss2:
        print("아직 누락된 회차: {} (알려주시면 개별 처리)".format(miss2))
    else:
        print("1~{}회 전부 수집 완료. lotto_data.js 를 위젯에 붙여넣으세요.".format(latest))


if __name__ == "__main__":
    main()
