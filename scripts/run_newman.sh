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
for api in "${apis[@]}"; do
  scripts/reset_sut.sh
  date_suffix="$(date +%Y%m%d)"
  if newman run "collections/23120190_${api}.postman_collection.json" -e environments/local.postman_environment.json \
    --reporters cli,htmlextra,json \
    --reporter-htmlextra-export "results/newman/23120190_${api}_${date_suffix}.html" \
    --reporter-htmlextra-title "23120190 – ${api} – localhost" \
    --reporter-json-export "results/newman/23120190_${api}_${date_suffix}.json"; then
    results+=("$api: PASS")
  else
    results+=("$api: FAIL")
    failed=1
  fi
done

# X-DATA: data-driven runs will be added here.
printf '\nSummary:\n%s\n' "${results[@]}"
exit "$failed"
