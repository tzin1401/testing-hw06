#!/bin/bash
# Tái hiện các bug trong report/issues/ bằng request thật tới SUT, lưu transcript vào evidence/issues/BUG-xx_curl.txt.
# Dùng: ./scripts/repro_bugs.sh [BUG-01 BUG-02 ...]   (không tham số = chạy tất cả)
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
B=http://localhost:3000
OUTDIR=evidence/issues
mask() { sed -E 's/eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/eyJ***(JWT đã che)/g'; }
reset() { scripts/reset_sut.sh >/dev/null && echo "$ scripts/reset_sut.sh   # SUT seed lại"; }

# req METHOD PATH [TOKEN_NAME] [BODY] [CONTENT_TYPE] [AUTH_SCHEME]
# In lệnh (token hiện bằng tên biến) rồi in status + body thật. Body response lưu vào $R.
req() {
  local m=$1 p=$2 tn=${3:-} body=${4:-} ct=${5:-application/json} sch=${6:-Bearer}
  local args=(-s -o /tmp/repro_body.$$ -w '%{http_code}' -X "$m" "$B$p" -H "X-Student-Id: 23120190")
  local show="curl -X $m '$B$p' -H 'X-Student-Id: 23120190'"
  if [ -n "$tn" ]; then args+=(-H "Authorization: $sch ${!tn}"); show+=" -H 'Authorization: $sch \$$tn'"; fi
  if [ -n "$body" ]; then args+=(-H "Content-Type: $ct" --data-raw "$body"); show+=" -H 'Content-Type: $ct' -d '$body'"; fi
  echo; echo "\$ $show"
  CODE=$(curl "${args[@]}"); R=$(cat /tmp/repro_body.$$ 2>/dev/null); rm -f /tmp/repro_body.$$
  echo "HTTP $CODE"; printf '%s\n' "$R" | head -c 1500 | mask; echo
}
j() { printf '%s' "$R" | jq -r "$1"; }
note() { echo; echo "# $*"; }
new_user() { # new_user VAR_TOKEN VAR_EMAIL
  local e="bug-$(date +%s%N)@test.com"; printf -v "$2" '%s' "$e"
  req POST /api/register "" "{\"name\":\"Bug User\",\"email\":\"$e\",\"password\":\"Test1234!\"}"
  req POST /api/login "" "{\"email\":\"$e\",\"password\":\"Test1234!\"}"; printf -v "$1" '%s' "$(j .token)"
}
admin_login() { req POST /api/login "" '{"email":"admin@eshop.com","password":"Admin123!"}'; ADMIN=$(j .token); }
new_order() { req POST /api/checkout "$1" '{"total_amount":100000,"shipping_address":"HCM"}'; printf -v "$2" '%s' "$(j .orderId)"; }

bug01() { note "FR-02: mỗi lần sai phải tăng bộ đếm đúng 1"; reset; new_user TOKEN_A EMAIL_A
  req POST /api/login "" "{\"email\":\"$EMAIL_A\",\"password\":\"Sai12345!\"}"
  note "Đọc bộ đếm sau MỘT lần sai"; req GET /api/users/me TOKEN_A
  echo "=> login_attempts = $(j .login_attempts) (expected 1)"; }

bug02() { note "FR-02: khóa 30 giây"; reset; new_user TOKEN_A EMAIL_A
  for i in 1 2 3; do req POST /api/login "" "{\"email\":\"$EMAIL_A\",\"password\":\"Sai12345!\"}"; done
  req GET /api/users/me TOKEN_A; echo "=> now=$(date -u +%FT%TZ) locked_until=$(j .locked_until)"
  note "Chờ 31 giây rồi login đúng"; sleep 31
  req POST /api/login "" "{\"email\":\"$EMAIL_A\",\"password\":\"Test1234!\"}"; }

bug03() { note "SEC-01 / không lộ dữ liệu nhạy cảm"; reset
  req POST /api/login "" '{"email":"test@eshop.com","password":"Test1234!"}'
  echo "=> user.password trong response = $(j .user.password)"; }

bug04() { note "Content-Type không phải JSON"; reset
  req POST /api/login "" '{"email":"test@eshop.com","password":"Test1234!"}' text/plain; }

bug05() { note "FR-02: không để lộ chi tiết nguyên nhân"; reset; new_user TOKEN_A EMAIL_A
  for i in 1 2; do req POST /api/login "" "{\"email\":\"$EMAIL_A\",\"password\":\"Sai12345!\"}"; done
  note "Email đã đăng ký (đang bị khóa) vs email không tồn tại, cùng password sai"
  req POST /api/login "" "{\"email\":\"$EMAIL_A\",\"password\":\"Sai12345!\"}"
  req POST /api/login "" '{"email":"khong-ton-tai-123@test.com","password":"Sai12345!"}'; }

bug06() { note "SEC-02: token phải hợp lệ; secret hardcode trong eshop-sut/backend/server.js:9"; reset; new_user TOKEN_A EMAIL_A; new_order TOKEN_A ORDER_A
  FORGED=$(cd eshop-sut/backend && node -e 'console.log(require("jsonwebtoken").sign({id:1,role:"admin"},"super_secret_key_that_should_not_be_here"))')
  note "Token tự ký bằng secret lấy từ source, payload {id:1, role:admin}"
  req GET /api/users/me FORGED
  note "Token tự ký với id của user A hủy được đơn của A"
  FORGED_A=$(cd eshop-sut/backend && node -e "console.log(require('jsonwebtoken').sign({id:$(printf '%s' "$(curl -s $B/api/users/me -H "Authorization: Bearer $TOKEN_A" | jq .id)"),role:'user'},'super_secret_key_that_should_not_be_here'))")
  req PUT /api/orders/$ORDER_A/cancel FORGED_A; }

bug07() { note "Token không có exp, không bị thu hồi khi đổi mật khẩu hoặc xóa user"; reset; new_user TOKEN_A EMAIL_A
  echo "=> payload JWT: $(printf '%s' "$TOKEN_A" | cut -d. -f2 | tr '_-' '/+' | base64 -d 2>/dev/null)"
  new_order TOKEN_A ORDER_A
  req POST /api/forgot-password "" "{\"email\":\"$EMAIL_A\"}"; OTP=$(j .resetToken)
  req POST /api/reset-password "" "{\"email\":\"$EMAIL_A\",\"resetToken\":\"$OTP\",\"newPassword\":\"NewPass123!\"}"
  note "Token cũ (cấp trước khi đổi mật khẩu) vẫn dùng được"
  req PUT /api/orders/$ORDER_A/cancel TOKEN_A
  note "Xóa user B, token của B vẫn hủy được đơn"; new_user TOKEN_B EMAIL_B; new_order TOKEN_B ORDER_B
  admin_login; ID_B=$(curl -s $B/api/users/me -H "Authorization: Bearer $TOKEN_B" | jq .id)
  req DELETE /api/admin/users/$ID_B ADMIN
  req PUT /api/orders/$ORDER_B/cancel TOKEN_B; }

bug08() { note "Header Authorization dùng scheme Basic vẫn được chấp nhận"; reset; new_user TOKEN_A EMAIL_A; new_order TOKEN_A ORDER_A
  req PUT /api/orders/$ORDER_A/cancel TOKEN_A "" application/json Basic
  req GET /api/orders/$ORDER_A; echo "=> status = $(j .status)"; }

to_status() { req PUT /api/admin/orders/$1/status ADMIN "{\"status\":\"$2\"}"; }
bug09() { note "FR-10: đơn shipping user không được tự hủy"; reset; new_user TOKEN_A EMAIL_A; new_order TOKEN_A ORDER_A; admin_login
  to_status $ORDER_A confirmed; to_status $ORDER_A shipping
  req PUT /api/orders/$ORDER_A/cancel TOKEN_A
  req GET /api/orders/$ORDER_A; echo "=> status = $(j .status) (expected shipping)"; }

bug10() { note "FR-10: canceled là trạng thái kết thúc"; reset; new_user TOKEN_A EMAIL_A; new_order TOKEN_A ORDER_A; admin_login
  req PUT /api/orders/$ORDER_A/cancel TOKEN_A
  to_status $ORDER_A delivered
  req GET /api/orders/$ORDER_A; echo "=> status = $(j .status) (expected canceled)"; }

bug11() { note "Path id không phải số nguyên chuẩn vẫn khớp bản ghi"; reset; new_user TOKEN_A EMAIL_A
  for f in '%2B' '' '0'; do new_order TOKEN_A O
    case $f in '') P="$O.0";; *) P="$f$O";; esac
    req PUT "/api/orders/$P/cancel" TOKEN_A; req GET /api/orders/$O; echo "=> order $O status = $(j .status)"; done
  note "Product: DELETE /api/products/2.0 xóa product id 2"
  req GET /api/products/2; req DELETE /api/products/2.0; req GET /api/products/2; }

bug12() { note "FR-12/SEC-02/SEC-03: POST/PUT/DELETE /api/products phải cần JWT admin"; reset
  note "Không có token"; req POST /api/products "" '{"name":"No Auth","price":100,"category_id":1}'; PID=$(j .id)
  req PUT /api/products/$PID "" '{"name":"No Auth edited","price":200,"category_id":1}'
  req DELETE /api/products/$PID
  note "Token user thường"; new_user TOKEN_A EMAIL_A
  req POST /api/products TOKEN_A '{"name":"User Created","price":100,"category_id":1}'; req GET /api/products/$(j .id); }

bug13() { note "FR-15: name bắt buộc, price > 0, category từ danh sách"; reset
  req POST /api/products "" '{"price":100,"category_id":1}';                  req GET /api/products/$(j .id)
  req POST /api/products "" '{"name":"Gia am","price":-5,"category_id":1}';   req GET /api/products/$(j .id)
  req POST /api/products "" '{"name":"Gia 0","price":0,"category_id":1}'
  req POST /api/products "" '{"name":"Gia -0","price":-0,"category_id":1}'
  req POST /api/products "" '{"name":"Gia vo cuc","price":1e309,"category_id":1}'
  req POST /api/products "" '{"name":"Category ao","price":100,"category_id":9999}'
  note "PUT thiếu field -> các field khác bị ghi NULL"
  req GET /api/products/3; req PUT /api/products/3 "" '{"name":"Chi doi ten"}'; req GET /api/products/3; }

bug14() { note "GET detail làm sập server khi price null"; reset
  req PUT /api/products/2 "" '{"name":"Price null","price":null,"category_id":1}'
  req GET /api/products/2
  req GET /api/products
  note "Log server"; tail -n 8 results/server.log; }

bug15() { note "SEC-06: API cập nhật hồ sơ không được đổi role"; reset; new_user TOKEN_A EMAIL_A
  req PUT /api/users/me TOKEN_A '{"name":"Bug User","role":"admin"}'
  req GET /api/users/me TOKEN_A; echo "=> role = $(j .role)"
  req POST /api/login "" "{\"email\":\"$EMAIL_A\",\"password\":\"Test1234!\"}"; echo "=> role trong login = $(j .user.role)"; }

bug16() { note "Kiểu price không nhất quán giữa các id"; reset
  req GET /api/products/1; echo "=> id 1 price type = $(j '.price|type')"
  req GET /api/products/2; echo "=> id 2 price type = $(j '.price|type')"; }

ALL=$(declare -F | awk '{print $3}' | grep '^bug[0-9]' | sort)
SEL=${*:-$ALL}
for b in $SEL; do b=${b,,}; b=${b/bug-/bug}
  id=$(printf 'BUG-%02d' "$((10#${b#bug}))")
  { echo "# $id – transcript tái hiện thật, $(date '+%Y-%m-%d %H:%M:%S %Z'), SUT eshop-sut@$(git -C eshop-sut log -1 --format=%h 2>/dev/null || echo 85af3ba)"; "$b"; } > "$OUTDIR/${id}_curl.txt" 2>&1
  echo "$id -> $OUTDIR/${id}_curl.txt"
done
scripts/reset_sut.sh >/dev/null
