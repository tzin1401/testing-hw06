#!/bin/bash
# Chạy Newman thật cho OUT/collection.json. Dùng: run.sh OUT
# Reset SUT bằng $RESET_CMD (mặc định scripts/reset_sut.sh). Case crashes_sut chạy riêng sau reset.
set -u
OUT=${1:?Usage: run.sh OUT}
RESET_CMD=${RESET_CMD:-scripts/reset_sut.sh}
mkdir -p "$OUT/newman"
base=$(jq -r '.values[]|select(.key=="baseUrl").value' "$OUT/env.json")
case "$base" in http://localhost:*|http://127.0.0.1:*) ;; *) echo "Dừng: baseUrl không phải localhost ($base)"; exit 2;; esac

folder_of() { jq -r --arg id "$1" '.item[].item[]|select(.name|startswith("["+$id+"]")).name' "$OUT/collection.json"; }
crash=$(jq -r '.cases[]|select(.crashes_sut==true and .label!="INVALID").id' "$OUT/cases.json")
normal=$(jq -r '.cases[]|select((.crashes_sut//false)==false and .label!="INVALID").id' "$OUT/cases.json")

for id in $crash; do
  $RESET_CMD
  newman run "$OUT/collection.json" -e "$OUT/env.json" --folder "$(folder_of "$id")" \
    --reporters cli,json,htmlextra --reporter-json-export "$OUT/newman/isolated-$id.json" \
    --reporter-htmlextra-export "$OUT/newman/isolated-$id.html" >/dev/null || true
  echo "isolated $id -> $OUT/newman/isolated-$id.json"
done

args=()
for id in $normal; do args+=(--folder "$(folder_of "$id")"); done
[ ${#args[@]} -eq 0 ] && { $RESET_CMD >/dev/null; exit 0; }   # không có --folder thì newman chạy cả collection
$RESET_CMD
newman run "$OUT/collection.json" -e "$OUT/env.json" "${args[@]}" \
  --reporters cli,json,htmlextra --reporter-json-export "$OUT/newman/main.json" \
  --reporter-htmlextra-export "$OUT/newman/main.html" | tail -25
$RESET_CMD >/dev/null
