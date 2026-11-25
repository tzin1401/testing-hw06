#!/bin/bash
# Chạy bộ regression trong ci/regression_cases.txt bằng Newman (dùng cho GitHub Actions và chạy tay).
# Mỗi API: reset SUT rồi chạy các folder case theo thứ tự trong collection.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
mkdir -p results/ci
failed=0
for api in API1_Login API2_CancelOrder API3_ProductCRUD; do
  args=()
  while IFS='|' read -r a name; do
    [ "$a" = "$api" ] && args+=(--folder "$name")
  done < <(grep -v '^#' ci/regression_cases.txt)
  [ ${#args[@]} -eq 0 ] && continue
  scripts/reset_sut.sh
  newman run "collections/23120190_${api}.postman_collection.json" -e environments/local.postman_environment.json \
    "${args[@]}" --reporters cli,htmlextra,junit \
    --reporter-htmlextra-export "results/ci/23120190_${api}_ci.html" \
    --reporter-junit-export "results/ci/23120190_${api}_ci.xml" || failed=1
done
exit $failed
