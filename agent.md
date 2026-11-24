# Agent rules – HW06 API Testing

Quy tắc cho AI agent khi hỗ trợ làm HW06. Nguồn: `2026.HW06.API Testing_En.pdf`.

## 1. Ghi AI log (chỉ khi được yêu cầu)

- **Chỉ ghi log khi prompt có cụm "ghi vào log"** (không phân biệt hoa thường). Prompt không có cụm này thì không ghi.
- **Nối thêm** vào `report/AI_LOG.md`. Không sửa, không xóa entry cũ.
- Định dạng mỗi entry (Mục 9 của đề):

```markdown
## #<số thứ tự> – <YYYY-MM-DD HH:MM> (giờ VN)
- **AI tool:** <tên công cụ> (<model id>)
- **API / Bước:** <API 1 – Generate | API 2 – Audit | Agent Skill | ...>
- **Prompt:**
  > <nguyên văn prompt, bỏ cụm "ghi vào log">
- **AI output:**
  > <tóm tắt: AI đã làm gì, file nào tạo/sửa, kết luận chính>
- **Human review:** _(để trống – sinh viên tự điền)_
```

- Lấy giờ bằng `date "+%Y-%m-%d %H:%M"`. Không tự đoán giờ.
- Không bao giờ tự điền "Human review".

## 2. Quy tắc làm bài

### AI-first, từng bước
- Mỗi API đi đúng pipeline: **Generate → Audit → Extend → Execute → Bug report**. Mỗi lần trả lời chỉ làm một bước nhỏ rồi dừng cho người dùng review.
- Sinh test case theo từng kỹ thuật riêng: domain partition từng tham số, state transition (FR-10, lockout, OTP), security SEC-01…SEC-07, schema validation. Không gộp một prompt "sinh hết".

### Không được bịa (Anti-AI-Cheat, Mục 11)
- **Không** tạo hoặc sửa Newman output / HTML report. Chỉ sinh từ lần chạy `newman` thật, hostname `localhost`.
- **Không** bịa ảnh chụp console `X-Student-Id`, kết quả CI hay response API. Mọi response trong bug report phải lấy từ lần gọi thật.
- **Không** vẽ sơ đồ AI test generator thay sinh viên. AI chỉ được góp ý.
- Không tự điền nhãn audit VALID/INVALID/INCOMPLETE thay sinh viên khi chưa được yêu cầu; nếu đề xuất thì ghi rõ "đề xuất của AI".

### Kỹ thuật
- Mọi request mang header `X-Student-Id: {{studentId}}` qua **pre-request script cấp collection**, có `console.log` để chụp màn hình.
- Reset SUT bằng `scripts/reset_sut.sh` trước mỗi lần chạy đầy đủ.
- Mỗi bước của mỗi API là **một commit** (generate, audit, extend, execute).
- Commit message **không** ghi tên AI: không `Co-Authored-By`, không "Generated with …", không nhắc Claude/GPT/agent.

## 3. Quy ước tên file

| Loại | Tên |
|---|---|
| Collection | `collections/23120190_<API>.postman_collection.json` |
| Newman report | `results/newman/23120190_<API>_<YYYYMMDD>.html` |
| Test case Excel | `report/23120190_HW06_TestCases.xlsx` |
| File nộp | `23120190_HW06_AI_API_<điểm 3 chữ số>.zip` |
