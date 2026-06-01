# -*- coding: utf-8 -*-
"""lotto_data.js 읽어서 widget-01.html 재생성"""
import os

# GitHub Actions는 레포 루트에서 실행, 로컬은 scripts/ 폴더에서 실행
DATA_JS = "lotto_data.js" if os.path.exists("lotto_data.js") else os.path.join(os.path.dirname(__file__), "..", "lotto_data.js")
WIDGET  = "widget-01.html" if os.path.exists("lotto_data.js") else os.path.join(os.path.dirname(__file__), "..", "widget-01.html")

with open(DATA_JS, encoding="utf-8") as f:
    data_js = f.read().strip()

html = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>로또 6/45 회차별 당첨번호 조회</title>
<style>*{{margin:0;padding:0;box-sizing:border-box;}}body{{background:#f5f5f7;display:flex;justify-content:center;padding:16px 16px 32px;}}</style>
</head>
<body>
<div id="lotto645-widget">
  <div class="lw-head"><span class="lw-badge">LOTTO 6/45</span><div class="lw-title">회차별 당첨번호 조회</div></div>
  <div class="lw-controls">
    <button class="lw-nav" data-act="prev">&#x2039;</button>
    <div class="lw-select-wrap"><select class="lw-select"></select><span class="lw-hoe">회</span></div>
    <button class="lw-nav" data-act="next">&#x203a;</button>
  </div>
  <div class="lw-card">
    <div class="lw-meta"><span class="lw-date"></span><span class="lw-carry"></span></div>
    <div class="lw-balls"></div>
    <table class="lw-table"><thead><tr><th>순위</th><th>당첨자 수</th><th>1인당 당첨금</th></tr></thead><tbody></tbody></table>
    <div class="lw-sell"></div>
  </div>
  <div id="lw-related" style="max-width:480px;margin:12px auto 0;display:grid;grid-template-columns:1fr 1fr;gap:8px;">
    <a href="https://archivebox.tistory.com/2" target="_blank" style="display:block;padding:11px;border:1px solid #e0e0e8;border-radius:10px;font-size:12px;font-weight:700;color:#444;text-decoration:none;text-align:center;background:#fafafa;">당첨금 실수령액 계산기</a>
    <a href="#" target="_blank" style="display:block;padding:11px;border:1px solid #e0e0e8;border-radius:10px;font-size:12px;font-weight:700;color:#444;text-decoration:none;text-align:center;background:#fafafa;">내 번호 당첨 확인</a>
  </div>
  <p class="lw-foot">자료 출처: 동행복권 · 당첨금은 세전 기준입니다.</p>
</div>
<style>
#lotto645-widget{{--y:#fbc400;--b:#69c8f2;--r:#ff7272;--g:#aaaaaa;--grn:#b0d840;--ink:#1a1a2e;--line:#ececf1;--soft:#6b6b7b;max-width:480px;width:100%;font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Pretendard","Malgun Gothic",sans-serif;color:var(--ink);line-height:1.5;}}
#lotto645-widget *{{box-sizing:border-box;}}
#lotto645-widget .lw-head{{background:linear-gradient(135deg,#1a1a2e 0%,#2d2d52 100%);border-radius:18px 18px 0 0;padding:20px 24px 18px;color:#fff;}}
#lotto645-widget .lw-badge{{display:inline-block;font-size:11px;font-weight:800;letter-spacing:2px;color:#ffd84d;border:1px solid rgba(255,216,77,.5);border-radius:20px;padding:3px 12px;margin-bottom:8px;}}
#lotto645-widget .lw-title{{margin:0;font-size:21px;font-weight:800;letter-spacing:-.4px;}}
#lotto645-widget .lw-controls{{display:flex;align-items:center;justify-content:center;gap:10px;background:#14142a;padding:14px;}}
#lotto645-widget .lw-nav{{width:38px;height:38px;border:none;border-radius:50%;background:rgba(255,255,255,.12);color:#fff;font-size:22px;line-height:1;cursor:pointer;transition:background .15s;flex:0 0 auto;}}
#lotto645-widget .lw-nav:hover{{background:rgba(255,255,255,.25);}}
#lotto645-widget .lw-nav:disabled{{opacity:.3;cursor:default;}}
#lotto645-widget .lw-select-wrap{{display:flex;align-items:center;gap:6px;}}
#lotto645-widget .lw-select{{appearance:none;-webkit-appearance:none;background:#fff;border:none;border-radius:10px;padding:9px 16px;font-size:17px;font-weight:800;color:var(--ink);text-align:center;cursor:pointer;min-width:96px;}}
#lotto645-widget .lw-hoe{{color:#fff;font-weight:700;font-size:15px;}}
#lotto645-widget .lw-card{{background:#fff;border:1px solid var(--line);border-top:none;border-radius:0 0 18px 18px;padding:24px;}}
#lotto645-widget .lw-meta{{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;font-size:13px;}}
#lotto645-widget .lw-date{{color:var(--soft);font-weight:600;}}
#lotto645-widget .lw-carry{{font-weight:800;font-size:12px;padding:4px 10px;border-radius:20px;}}
#lotto645-widget .lw-carry.on{{background:#fff3cd;color:#9a6b00;}}
#lotto645-widget .lw-carry.off{{background:#e9f7ef;color:#1a7a45;}}
#lotto645-widget .lw-balls{{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:9px;margin-bottom:22px;}}
#lotto645-widget .lw-ball{{width:46px;height:46px;border-radius:50%;color:#fff;display:flex;align-items:center;justify-content:center;font-size:19px;font-weight:800;flex:0 0 auto;box-shadow:0 3px 6px rgba(0,0,0,.18);text-shadow:0 1px 2px rgba(0,0,0,.2);}}
#lotto645-widget .lw-plus{{font-size:22px;font-weight:800;color:var(--soft);}}
#lotto645-widget .lw-bonus-label{{width:100%;text-align:center;font-size:11px;color:var(--soft);margin-top:-4px;font-weight:600;}}
#lotto645-widget .lw-table{{width:100%;border-collapse:collapse;font-size:13.5px;}}
#lotto645-widget .lw-table th{{background:#f6f6fa;color:var(--soft);font-weight:700;font-size:12px;padding:9px 8px;text-align:center;border-bottom:1px solid var(--line);}}
#lotto645-widget .lw-table td{{padding:11px 8px;text-align:center;border-bottom:1px solid var(--line);}}
#lotto645-widget .lw-table td:first-child{{font-weight:800;}}
#lotto645-widget .lw-table td:last-child{{font-weight:700;text-align:right;}}
#lotto645-widget .lw-table tr:last-child td{{border-bottom:none;}}
#lotto645-widget .lw-sell{{margin-top:16px;font-size:12.5px;color:var(--soft);}}
#lotto645-widget .lw-sell b{{color:var(--ink);font-weight:800;}}
#lotto645-widget .lw-foot{{text-align:center;font-size:11px;color:#a0a0ad;margin:12px 0 0;}}
@media(max-width:430px){{#lotto645-widget .lw-ball{{width:40px;height:40px;font-size:17px;}}#lotto645-widget .lw-card{{padding:18px;}}}}
</style>
<script>
{data_js}
(function(){{
  var root=document.getElementById('lotto645-widget');
  if(!root||!LOTTO_DATA||!LOTTO_DATA.length)return;
  LOTTO_DATA.sort(function(a,b){{return b.no-a.no;}});
  var byNo={{}};LOTTO_DATA.forEach(function(d){{byNo[d.no]=d;}});
  var sel=root.querySelector('.lw-select'),balls=root.querySelector('.lw-balls'),tbody=root.querySelector('.lw-table tbody');
  var dateEl=root.querySelector('.lw-date'),carryEl=root.querySelector('.lw-carry'),sellEl=root.querySelector('.lw-sell');
  var prevBtn=root.querySelector('[data-act="prev"]'),nextBtn=root.querySelector('[data-act="next"]');
  LOTTO_DATA.forEach(function(d){{var o=document.createElement('option');o.value=d.no;o.textContent=d.no;sel.appendChild(o);}});
  function ballColor(n){{if(n<=10)return'var(--y)';if(n<=20)return'var(--b)';if(n<=30)return'var(--r)';if(n<=40)return'var(--g)';return'var(--grn)';}}
  function won(v){{if(!v)return'-';if(v>=100000000){{var uk=Math.floor(v/100000000),man=Math.floor((v%100000000)/10000);return man>0?uk+'억 '+man.toLocaleString('ko-KR')+'만원':uk+'억원';}}if(v>=10000)return Math.round(v/10000).toLocaleString('ko-KR')+'만원';return v.toLocaleString('ko-KR')+'원';}}
  function makeBall(n){{var b=document.createElement('span');b.className='lw-ball';b.style.background=ballColor(n);b.textContent=n;return b;}}
  var RANK=['1등','2등','3등','4등','5등'];
  function render(no){{
    var d=byNo[no];if(!d)return;
    sel.value=no;dateEl.textContent=d.date+' 추첨';
    var carried=d.ranks[0].co===0;
    carryEl.textContent=carried?'⚠ 이월 (1등 없음)':'당첨 (이월 없음)';
    carryEl.className='lw-carry '+(carried?'on':'off');
    balls.innerHTML='';
    d.nums.forEach(function(n){{balls.appendChild(makeBall(n));}});
    var plus=document.createElement('span');plus.className='lw-plus';plus.textContent='+';
    balls.appendChild(plus);balls.appendChild(makeBall(d.bonus));
    var bl=document.createElement('span');bl.className='lw-bonus-label';bl.textContent='마지막 번호는 보너스';balls.appendChild(bl);
    tbody.innerHTML='';
    d.ranks.forEach(function(r,i){{var tr=document.createElement('tr');tr.innerHTML='<td>'+RANK[i]+'</td><td>'+(r.co?r.co.toLocaleString()+'명':'0명')+'</td><td>'+won(r.amt)+'</td>';tbody.appendChild(tr);}});
    var tp=d.ranks.reduce(function(s,r){{return s+r.co*r.amt;}},0);
    sellEl.innerHTML='<div style="display:flex;justify-content:space-between;align-items:center;font-size:12.5px;padding:4px 0;"><span style="color:var(--soft)">총 당첨금</span><b>'+won(tp)+'</b></div><div style="display:flex;justify-content:space-between;align-items:center;font-size:12.5px;padding:4px 0;border-top:1px solid var(--line);"><span style="color:var(--soft)">총 판매액</span><b>'+won(d.sell)+'</b></div>';
    var idx=LOTTO_DATA.indexOf(d);prevBtn.disabled=(idx===LOTTO_DATA.length-1);nextBtn.disabled=(idx===0);
  }}
  sel.addEventListener('change',function(){{render(+this.value);}});
  prevBtn.addEventListener('click',function(){{var i=LOTTO_DATA.indexOf(byNo[+sel.value]);if(i<LOTTO_DATA.length-1)render(LOTTO_DATA[i+1].no);}});
  nextBtn.addEventListener('click',function(){{var i=LOTTO_DATA.indexOf(byNo[+sel.value]);if(i>0)render(LOTTO_DATA[i-1].no);}});
  render(LOTTO_DATA[0].no);
}})();
</script>
</body>
</html>""".format(data_js=data_js)

with open(WIDGET, "w", encoding="utf-8") as f:
    f.write(html)

print("widget-01.html 재생성 완료")
