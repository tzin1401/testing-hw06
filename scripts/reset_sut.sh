#!/bin/bash
# Reset SUT: restart backend; database.js tự DROP + seed lại DB (xóa lockout, order, coupon usage). Cart nằm trong RAM nên cũng bị xóa.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
pkill -f "^node server.js" || true
sleep 1
cd "$ROOT/eshop-sut/backend"
[ -d node_modules ] || npm ci --silent
setsid node server.js > "$ROOT/results/server.log" 2>&1 &
for i in $(seq 60); do curl -s localhost:3000/api/products >/dev/null && break; sleep 0.5; done
curl -sf localhost:3000/api/products >/dev/null || { echo "SUT không lên, xem results/server.log"; exit 1; }
echo "SUT reset. Backend PID: $(pgrep -f '^node server.js')"
