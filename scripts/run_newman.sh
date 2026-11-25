#!/bin/bash
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [ "$#" -gt 1 ]; then
  echo "Usage: $0 [API1_Login|API2_CancelOrder|API3_ProductCRUD]" >&2
  exit 2
fi
case "${1-}" in
  '') apis=(API1_Login API2_CancelOrder API3_ProductCRUD) ;;
  API1_Login|API2_CancelOrder|API3_ProductCRUD) apis=("$1") ;;
  *) echo "Usage: $0 [API1_Login|API2_CancelOrder|API3_ProductCRUD]" >&2; exit 2 ;;
esac

mkdir -p results/newman
results=()
failed=0
date_suffix="$(date +%Y%m%d)"
for api in "${apis[@]}"; do
  folders=(--folder G1 --folder G2 --folder G3 --folder G4 --folder G6 --folder EX)
  if [ "$api" = API3_ProductCRUD ]; then
    folders+=(--folder EX-last)
    for case_name in \
      "[PR-G6-09] H2: price null" \
      "[PR-G6-15] H8: thiếu riêng price" \
      "[PR-G6-31] H10: auth-first PUT body rỗng"; do
      case_id="${case_name%%]*}"
      case_id="${case_id#[}"
      scripts/reset_sut.sh
      if newman run "collections/23120190_${api}.postman_collection.json" -e environments/local.postman_environment.json \
        --folder "$case_name" \
        --reporters cli,htmlextra,json \
        --reporter-htmlextra-export "results/newman/23120190_${api}_isolated-${case_id}_${date_suffix}.html" \
        --reporter-htmlextra-title "23120190 – ${api} – ${case_id} – localhost" \
        --reporter-json-export "results/newman/23120190_${api}_isolated-${case_id}_${date_suffix}.json"; then
        results+=("$api-isolated-$case_id: PASS")
      else
        results+=("$api-isolated-$case_id: FAIL")
        failed=1
      fi
    done
  fi
  scripts/reset_sut.sh
  if newman run "collections/23120190_${api}.postman_collection.json" -e environments/local.postman_environment.json \
    "${folders[@]}" \
    --reporters cli,htmlextra,json \
    --reporter-htmlextra-export "results/newman/23120190_${api}_${date_suffix}.html" \
    --reporter-htmlextra-title "23120190 – ${api} – localhost" \
    --reporter-json-export "results/newman/23120190_${api}_${date_suffix}.json"; then
    results+=("$api: PASS")
  else
    results+=("$api: FAIL")
    failed=1
  fi
  if [ "$api" = API1_Login ]; then
    scripts/reset_sut.sh
    if newman run collections/23120190_API1_Login.postman_collection.json -e environments/local.postman_environment.json \
      --folder "DATA – LG-G1" -d data/lg_g1_partition.csv \
      --reporters cli,htmlextra --reporter-htmlextra-export "results/newman/23120190_API1_Login-data_${date_suffix}.html"; then
      results+=("API1_Login-data: PASS")
    else
      results+=("API1_Login-data: FAIL")
      failed=1
    fi
  fi
  if [ "$api" = API3_ProductCRUD ]; then scripts/reset_sut.sh; fi
done

printf '\nSummary:\n%s\n' "${results[@]}"
exit "$failed"
