#!/bin/bash
# Dựng report/MAIN_REPORT.pdf = MAIN_REPORT.md + phụ lục (bug report, Postman features, CI/CD, AI critique).
# Ảnh dùng đường dẫn tương đối từ report/ nên pandoc chạy với --resource-path=report.
set -e
cd "$(dirname "$0")/.."
tmp=$(mktemp -d)
{
  cat report/MAIN_REPORT.md
  for f in bug_report postman_features cicd_report AI_CRITIQUE; do
    echo; echo "## Phụ lục – $f.md"; echo
    sed -e '1d' -e 's/^## /### /' -e 's/</\&lt;/g' "report/$f.md"
  done
} > "$tmp/all.md"
sed -n '/^cat > "$tmp\/style.css"/,/^CSS$/p' scripts/build_audit_pdf.sh | sed '1d;$d' > "$tmp/style.css"
echo 'img{max-width:100%;max-height:250mm;object-fit:contain;break-inside:avoid}' >> "$tmp/style.css"
pandoc "$tmp/all.md" -f gfm-tex_math_dollars-tex_math_gfm -s --resource-path=report --metadata pagetitle="HW06 – Báo cáo chính" --css "$tmp/style.css" --embed-resources -o "$tmp/all.html"
google-chrome --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=report/MAIN_REPORT.pdf "file://$tmp/all.html" 2>/dev/null
rm -rf "$tmp"
echo "-> report/MAIN_REPORT.pdf"
