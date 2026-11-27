#!/bin/bash
# Dựng report/AI_AUDIT_REPORT.pdf = AI_AUDIT_REPORT.md + phụ lục toàn văn AI_LOG.md (+ AI_CRITIQUE.md nếu có).
# Log có payload XSS (<img onerror>, <script>): escape '<' để hiện dạng chữ, không chạy trong Chrome.
# Chạy lại sau mỗi lần sửa log / Human review.
set -e
cd "$(dirname "$0")/.."
tmp=$(mktemp -d)
{
  cat report/AI_AUDIT_REPORT.md
  [ -f report/AI_CRITIQUE.md ] && { echo; sed 's/^# /## /' report/AI_CRITIQUE.md; }
  echo
  echo '## Phụ lục – Toàn văn AI_LOG.md'; echo
  sed -e '1d' -e 's/^## #/### #/' -e 's/</\&lt;/g' report/AI_LOG.md
} > "$tmp/all.md"
cat > "$tmp/style.css" <<'CSS'
body{font-family:"Noto Sans","DejaVu Sans",Arial,sans-serif;font-size:10.5pt;line-height:1.45;max-width:none;margin:0}
table{border-collapse:collapse;width:100%;font-size:9pt;margin:8px 0}
th,td{border:1px solid #999;padding:3px 5px;vertical-align:top}th{background:#eee}
blockquote{margin:4px 0 4px 10px;padding-left:8px;border-left:3px solid #ccc;color:#333;font-size:9pt;white-space:pre-wrap}
code{font-size:9pt}h1{font-size:18pt}h2{font-size:14pt;border-bottom:1px solid #ccc}h3{font-size:11.5pt}
@page{size:A4;margin:16mm 14mm}
CSS
pandoc "$tmp/all.md" -f gfm-tex_math_dollars-tex_math_gfm -s --metadata pagetitle="AI Audit Report – HW06" --css "$tmp/style.css" --embed-resources -o "$tmp/all.html"
google-chrome --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=report/AI_AUDIT_REPORT.pdf "file://$tmp/all.html" 2>/dev/null
rm -rf "$tmp"
echo "-> report/AI_AUDIT_REPORT.pdf"
