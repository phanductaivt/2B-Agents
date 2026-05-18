# Requirement Document: Basic Inventory Management System

**Document version:** v1.0  
**Project name:** Basic Inventory Management System  
**Prepared for:** Multi-Agent Requirement Processing Demo  
**Primary purpose:** Provide a simple but structured requirement file for testing PO, BA, UX/UI, FE, BE, and QA agents.  
**Language:** Vietnamese  

---

## 1. Tổng quan dự án

Hệ thống quản lý kho cơ bản cho phép người dùng quản lý danh sách sản phẩm và số lượng tồn kho. Phạm vi ban đầu chỉ tập trung vào các chức năng cốt lõi gồm: tạo sản phẩm, xem danh sách sản phẩm trong kho, tìm kiếm sản phẩm, cập nhật thông tin sản phẩm, cập nhật số lượng tồn kho, và xoá sản phẩm khỏi kho.

Hệ thống không bao gồm các nghiệp vụ nâng cao như nhập kho theo phiếu, xuất kho theo đơn hàng, phân quyền nhiều cấp, quản lý nhiều kho, báo cáo tài chính, tích hợp kế toán hoặc barcode trong phiên bản này.

---

## 2. Mục tiêu nghiệp vụ

- Giúp người dùng lưu trữ danh sách sản phẩm trong kho một cách có hệ thống.
- Giúp người dùng biết được số lượng tồn kho hiện tại của từng sản phẩm.
- Giúp người dùng nhanh chóng tìm kiếm sản phẩm theo tên hoặc mã sản phẩm.
- Giúp người dùng cập nhật thông tin sản phẩm và tồn kho khi có thay đổi.
- Giúp người dùng xoá các sản phẩm không còn kinh doanh hoặc không còn cần quản lý.

---

## 3. Phạm vi chức năng

### 3.1 In scope

- Tạo mới sản phẩm.
- Xem danh sách sản phẩm trong kho.
- Tìm kiếm sản phẩm trong kho.
- Xem chi tiết sản phẩm.
- Cập nhật thông tin sản phẩm.
- Cập nhật số lượng tồn kho.
- Xoá sản phẩm.
- Kiểm tra dữ liệu đầu vào cơ bản.
- Hiển thị trạng thái tồn kho theo số lượng.

### 3.2 Out of scope

- Đăng nhập và phân quyền người dùng.
- Quản lý nhiều chi nhánh hoặc nhiều kho.
- Quản lý nhập kho, xuất kho bằng chứng từ.
- Quản lý nhà cung cấp.
- Quản lý đơn hàng bán hàng.
- Quản lý giá vốn, lợi nhuận, công nợ.
- Tích hợp barcode, QR code.
- Import/export Excel.
- Báo cáo biểu đồ nâng cao.

---

## 4. Đối tượng sử dụng

| Actor ID | Actor | Mô tả |
|---|---|---|
| ACT-001 | Nhân viên quản lý kho | Người trực tiếp tạo, cập nhật, tìm kiếm và xoá sản phẩm trong hệ thống. |

---

## 5. Giả định nghiệp vụ

- Mỗi sản phẩm có một mã sản phẩm duy nhất.
- Số lượng tồn kho không được nhỏ hơn 0.
- Người dùng có quyền thao tác toàn bộ chức năng trong phạm vi hệ thống.
- Dữ liệu sản phẩm được lưu trong cơ sở dữ liệu nội bộ của hệ thống.
- Sản phẩm bị xoá sẽ không còn hiển thị trong danh sách kho.

---

## 6. Dữ liệu sản phẩm

### 6.1 Product Entity

| Field ID | Tên trường | Kiểu dữ liệu | Bắt buộc | Quy tắc |
|---|---|---|---|---|
| FLD-001 | Product ID | UUID/String | Có | Hệ thống tự sinh, không cho người dùng chỉnh sửa. |
| FLD-002 | Product Code | String | Có | Không được trùng với sản phẩm khác. Tối đa 50 ký tự. |
| FLD-003 | Product Name | String | Có | Tối đa 255 ký tự. |
| FLD-004 | Description | Text | Không | Mô tả ngắn về sản phẩm. Tối đa 1.000 ký tự. |
| FLD-005 | Unit | String | Có | Ví dụ: cái, hộp, kg, chai, bộ. |
| FLD-006 | Quantity | Integer | Có | Số nguyên, lớn hơn hoặc bằng 0. |
| FLD-007 | Minimum Stock | Integer | Không | Dùng để cảnh báo tồn kho thấp. Nếu nhập thì phải >= 0. |
| FLD-008 | Status | Enum | Có | ACTIVE, LOW_STOCK, OUT_OF_STOCK. Hệ thống tự tính theo tồn kho. |
| FLD-009 | Created At | Datetime | Có | Hệ thống tự ghi nhận. |
| FLD-010 | Updated At | Datetime | Có | Hệ thống tự cập nhật khi có thay đổi. |

---

## 7. Quy tắc nghiệp vụ

| Rule ID | Quy tắc |
|---|---|
| BR-001 | Product Code là duy nhất trong toàn hệ thống. |
| BR-002 | Product Name không được để trống. |
| BR-003 | Quantity không được nhỏ hơn 0. |
| BR-004 | Nếu Quantity = 0 thì Status = OUT_OF_STOCK. |
| BR-005 | Nếu Quantity > 0 và Quantity <= Minimum Stock thì Status = LOW_STOCK. |
| BR-006 | Nếu Quantity > Minimum Stock hoặc không có Minimum Stock thì Status = ACTIVE. |
| BR-007 | Khi xoá sản phẩm, hệ thống phải yêu cầu người dùng xác nhận trước khi xoá. |
| BR-008 | Sản phẩm đã bị xoá không hiển thị trong danh sách và kết quả tìm kiếm. |
| BR-009 | Khi cập nhật sản phẩm, hệ thống phải ghi nhận Updated At mới nhất. |
| BR-010 | Tìm kiếm không phân biệt chữ hoa, chữ thường. |

---

## 8. Functional Requirements

### FR-001: Tạo mới sản phẩm

**Mô tả:**  
Người dùng có thể tạo một sản phẩm mới trong kho bằng cách nhập các thông tin cơ bản của sản phẩm.

**Actor:** ACT-001  
**Priority:** High  
**Input:** Product Code, Product Name, Description, Unit, Quantity, Minimum Stock  
**Output:** Sản phẩm mới được tạo và hiển thị trong danh sách kho.

**Business rules liên quan:** BR-001, BR-002, BR-003, BR-004, BR-005, BR-006

**Acceptance Criteria:**

- AC-001.1: Khi người dùng nhập đầy đủ thông tin hợp lệ và bấm lưu, hệ thống tạo sản phẩm thành công.
- AC-001.2: Nếu Product Code bị trùng, hệ thống hiển thị lỗi: "Mã sản phẩm đã tồn tại".
- AC-001.3: Nếu Product Name bị bỏ trống, hệ thống hiển thị lỗi: "Tên sản phẩm không được để trống".
- AC-001.4: Nếu Quantity nhỏ hơn 0, hệ thống hiển thị lỗi: "Số lượng tồn kho không hợp lệ".
- AC-001.5: Sau khi tạo thành công, sản phẩm xuất hiện trong danh sách sản phẩm.
- AC-001.6: Hệ thống tự động tính trạng thái tồn kho theo số lượng và minimum stock.

---

### FR-002: Xem danh sách sản phẩm trong kho

**Mô tả:**  
Người dùng có thể xem danh sách toàn bộ sản phẩm đang được quản lý trong kho.

**Actor:** ACT-001  
**Priority:** High  
**Input:** Không bắt buộc  
**Output:** Danh sách sản phẩm gồm mã sản phẩm, tên sản phẩm, đơn vị tính, số lượng, trạng thái tồn kho.

**Business rules liên quan:** BR-004, BR-005, BR-006, BR-008

**Acceptance Criteria:**

- AC-002.1: Hệ thống hiển thị danh sách sản phẩm đang hoạt động.
- AC-002.2: Danh sách không hiển thị sản phẩm đã bị xoá.
- AC-002.3: Mỗi dòng sản phẩm hiển thị tối thiểu: Product Code, Product Name, Unit, Quantity, Status.
- AC-002.4: Nếu chưa có sản phẩm, hệ thống hiển thị thông báo: "Chưa có sản phẩm trong kho".
- AC-002.5: Người dùng có thể mở màn hình chi tiết từ một sản phẩm trong danh sách.

---

### FR-003: Tìm kiếm sản phẩm trong kho

**Mô tả:**  
Người dùng có thể tìm kiếm sản phẩm theo Product Code hoặc Product Name.

**Actor:** ACT-001  
**Priority:** High  
**Input:** Keyword  
**Output:** Danh sách sản phẩm phù hợp với từ khoá tìm kiếm.

**Business rules liên quan:** BR-008, BR-010

**Acceptance Criteria:**

- AC-003.1: Người dùng có thể nhập từ khoá vào ô tìm kiếm.
- AC-003.2: Hệ thống tìm kiếm theo Product Code hoặc Product Name.
- AC-003.3: Tìm kiếm không phân biệt chữ hoa, chữ thường.
- AC-003.4: Nếu có kết quả phù hợp, hệ thống hiển thị danh sách sản phẩm phù hợp.
- AC-003.5: Nếu không có kết quả, hệ thống hiển thị thông báo: "Không tìm thấy sản phẩm phù hợp".
- AC-003.6: Sản phẩm đã bị xoá không xuất hiện trong kết quả tìm kiếm.

---

### FR-004: Xem chi tiết sản phẩm

**Mô tả:**  
Người dùng có thể xem thông tin chi tiết của một sản phẩm cụ thể.

**Actor:** ACT-001  
**Priority:** Medium  
**Input:** Product ID  
**Output:** Thông tin chi tiết sản phẩm.

**Business rules liên quan:** BR-008

**Acceptance Criteria:**

- AC-004.1: Khi người dùng chọn một sản phẩm, hệ thống mở màn hình chi tiết sản phẩm.
- AC-004.2: Màn hình chi tiết hiển thị đầy đủ các trường dữ liệu của sản phẩm.
- AC-004.3: Nếu sản phẩm không tồn tại hoặc đã bị xoá, hệ thống hiển thị thông báo: "Sản phẩm không tồn tại".

---

### FR-005: Cập nhật thông tin sản phẩm

**Mô tả:**  
Người dùng có thể cập nhật thông tin cơ bản của sản phẩm gồm Product Name, Description, Unit, Minimum Stock.

**Actor:** ACT-001  
**Priority:** High  
**Input:** Product ID và thông tin cần cập nhật  
**Output:** Thông tin sản phẩm được cập nhật.

**Business rules liên quan:** BR-002, BR-005, BR-006, BR-009

**Acceptance Criteria:**

- AC-005.1: Người dùng có thể mở màn hình chỉnh sửa từ danh sách hoặc chi tiết sản phẩm.
- AC-005.2: Người dùng có thể cập nhật Product Name, Description, Unit, Minimum Stock.
- AC-005.3: Nếu Product Name bị bỏ trống, hệ thống hiển thị lỗi: "Tên sản phẩm không được để trống".
- AC-005.4: Nếu Minimum Stock nhỏ hơn 0, hệ thống hiển thị lỗi: "Tồn kho tối thiểu không hợp lệ".
- AC-005.5: Sau khi cập nhật thành công, hệ thống hiển thị thông báo: "Cập nhật sản phẩm thành công".
- AC-005.6: Hệ thống cập nhật lại Updated At.
- AC-005.7: Hệ thống tính lại Status nếu Minimum Stock thay đổi.

---

### FR-006: Cập nhật số lượng tồn kho

**Mô tả:**  
Người dùng có thể cập nhật trực tiếp số lượng tồn kho hiện tại của sản phẩm.

**Actor:** ACT-001  
**Priority:** High  
**Input:** Product ID, Quantity mới  
**Output:** Số lượng tồn kho được cập nhật.

**Business rules liên quan:** BR-003, BR-004, BR-005, BR-006, BR-009

**Acceptance Criteria:**

- AC-006.1: Người dùng có thể nhập số lượng tồn kho mới cho sản phẩm.
- AC-006.2: Nếu Quantity mới là số nguyên >= 0, hệ thống cho phép cập nhật.
- AC-006.3: Nếu Quantity nhỏ hơn 0, hệ thống hiển thị lỗi: "Số lượng tồn kho không hợp lệ".
- AC-006.4: Sau khi cập nhật thành công, hệ thống hiển thị số lượng mới trong danh sách sản phẩm.
- AC-006.5: Hệ thống tự động tính lại Status sau khi Quantity thay đổi.
- AC-006.6: Hệ thống cập nhật lại Updated At.

---

### FR-007: Xoá sản phẩm

**Mô tả:**  
Người dùng có thể xoá một sản phẩm khỏi hệ thống quản lý kho.

**Actor:** ACT-001  
**Priority:** Medium  
**Input:** Product ID  
**Output:** Sản phẩm bị xoá khỏi danh sách quản lý.

**Business rules liên quan:** BR-007, BR-008

**Acceptance Criteria:**

- AC-007.1: Người dùng có thể chọn chức năng xoá từ danh sách hoặc chi tiết sản phẩm.
- AC-007.2: Trước khi xoá, hệ thống hiển thị hộp thoại xác nhận.
- AC-007.3: Nếu người dùng xác nhận xoá, hệ thống xoá sản phẩm khỏi danh sách.
- AC-007.4: Nếu người dùng huỷ, hệ thống không xoá sản phẩm.
- AC-007.5: Sau khi xoá, sản phẩm không còn hiển thị trong danh sách và kết quả tìm kiếm.
- AC-007.6: Nếu xoá sản phẩm không tồn tại, hệ thống hiển thị thông báo: "Sản phẩm không tồn tại".

---

## 9. User Stories

### US-001: Tạo sản phẩm mới

Là nhân viên quản lý kho, tôi muốn tạo sản phẩm mới để hệ thống ghi nhận sản phẩm cần quản lý trong kho.

**Liên kết requirement:** FR-001

---

### US-002: Xem danh sách sản phẩm

Là nhân viên quản lý kho, tôi muốn xem danh sách sản phẩm để biết hiện kho đang có những sản phẩm nào.

**Liên kết requirement:** FR-002

---

### US-003: Tìm kiếm sản phẩm

Là nhân viên quản lý kho, tôi muốn tìm kiếm sản phẩm theo mã hoặc tên để nhanh chóng tra cứu thông tin sản phẩm.

**Liên kết requirement:** FR-003

---

### US-004: Xem chi tiết sản phẩm

Là nhân viên quản lý kho, tôi muốn xem chi tiết sản phẩm để kiểm tra đầy đủ thông tin của sản phẩm đó.

**Liên kết requirement:** FR-004

---

### US-005: Cập nhật thông tin sản phẩm

Là nhân viên quản lý kho, tôi muốn cập nhật thông tin sản phẩm để dữ liệu trong hệ thống luôn chính xác.

**Liên kết requirement:** FR-005

---

### US-006: Cập nhật tồn kho

Là nhân viên quản lý kho, tôi muốn cập nhật số lượng tồn kho để phản ánh đúng số lượng hiện có trong kho.

**Liên kết requirement:** FR-006

---

### US-007: Xoá sản phẩm

Là nhân viên quản lý kho, tôi muốn xoá sản phẩm không còn quản lý để danh sách kho gọn gàng và chính xác.

**Liên kết requirement:** FR-007

---

## 10. Gợi ý màn hình UX/UI

### SCR-001: Màn hình danh sách sản phẩm

**Mục tiêu:** Hiển thị toàn bộ sản phẩm trong kho và cho phép tìm kiếm, tạo mới, chỉnh sửa, xoá.

**Thành phần chính:**

- Tiêu đề: Quản lý kho
- Nút: Tạo sản phẩm
- Ô tìm kiếm: Nhập mã hoặc tên sản phẩm
- Bảng danh sách sản phẩm gồm các cột:
  - Mã sản phẩm
  - Tên sản phẩm
  - Đơn vị tính
  - Số lượng
  - Trạng thái
  - Cập nhật lần cuối
  - Hành động: Xem, Sửa, Xoá

---

### SCR-002: Màn hình tạo/cập nhật sản phẩm

**Mục tiêu:** Cho phép nhập hoặc chỉnh sửa thông tin sản phẩm.

**Thành phần chính:**

- Product Code
- Product Name
- Description
- Unit
- Quantity
- Minimum Stock
- Nút Lưu
- Nút Huỷ

**Ghi chú:** Khi cập nhật sản phẩm, Product Code không được chỉnh sửa trong phiên bản này.

---

### SCR-003: Màn hình chi tiết sản phẩm

**Mục tiêu:** Hiển thị đầy đủ thông tin sản phẩm.

**Thành phần chính:**

- Mã sản phẩm
- Tên sản phẩm
- Mô tả
- Đơn vị tính
- Số lượng tồn kho
- Tồn kho tối thiểu
- Trạng thái tồn kho
- Ngày tạo
- Ngày cập nhật
- Nút Sửa
- Nút Xoá
- Nút Quay lại

---

## 11. Non-Functional Requirements

| NFR ID | Nhóm | Yêu cầu |
|---|---|---|
| NFR-001 | Usability | Giao diện đơn giản, người dùng mới có thể thao tác các chức năng chính trong vòng 5 phút. |
| NFR-002 | Performance | Danh sách sản phẩm phải tải trong vòng 2 giây với dữ liệu dưới 10.000 sản phẩm. |
| NFR-003 | Reliability | Dữ liệu không bị mất sau khi người dùng tạo, cập nhật hoặc xoá sản phẩm. |
| NFR-004 | Validation | Hệ thống phải kiểm tra dữ liệu bắt buộc trước khi lưu. |
| NFR-005 | Maintainability | Mỗi chức năng cần được tách rõ để dễ mở rộng thêm nhập kho, xuất kho trong tương lai. |
| NFR-006 | Security | Phiên bản demo chưa yêu cầu đăng nhập, nhưng API không được cho phép cập nhật dữ liệu thiếu Product ID. |

---

## 12. API gợi ý cho BE Agent

| API ID | Method | Endpoint | Mục đích |
|---|---|---|---|
| API-001 | POST | /api/products | Tạo sản phẩm mới |
| API-002 | GET | /api/products | Lấy danh sách sản phẩm |
| API-003 | GET | /api/products/{id} | Lấy chi tiết sản phẩm |
| API-004 | GET | /api/products/search?keyword= | Tìm kiếm sản phẩm |
| API-005 | PUT | /api/products/{id} | Cập nhật thông tin sản phẩm |
| API-006 | PATCH | /api/products/{id}/quantity | Cập nhật số lượng tồn kho |
| API-007 | DELETE | /api/products/{id} | Xoá sản phẩm |

---

## 13. Data validation

| Validation ID | Trường | Điều kiện | Thông báo lỗi |
|---|---|---|---|
| VAL-001 | Product Code | Bắt buộc | Mã sản phẩm không được để trống |
| VAL-002 | Product Code | Không được trùng | Mã sản phẩm đã tồn tại |
| VAL-003 | Product Name | Bắt buộc | Tên sản phẩm không được để trống |
| VAL-004 | Unit | Bắt buộc | Đơn vị tính không được để trống |
| VAL-005 | Quantity | Phải là số nguyên >= 0 | Số lượng tồn kho không hợp lệ |
| VAL-006 | Minimum Stock | Nếu nhập thì phải là số nguyên >= 0 | Tồn kho tối thiểu không hợp lệ |

---

## 14. Test scenarios gợi ý cho QA Agent

| Test Case ID | Requirement | Kịch bản kiểm thử | Kết quả mong đợi |
|---|---|---|---|
| TC-001 | FR-001 | Tạo sản phẩm với dữ liệu hợp lệ | Sản phẩm được tạo thành công |
| TC-002 | FR-001 | Tạo sản phẩm với Product Code bị trùng | Hệ thống báo lỗi mã sản phẩm đã tồn tại |
| TC-003 | FR-001 | Tạo sản phẩm thiếu Product Name | Hệ thống báo lỗi tên sản phẩm không được để trống |
| TC-004 | FR-001 | Tạo sản phẩm với Quantity = -1 | Hệ thống báo lỗi số lượng tồn kho không hợp lệ |
| TC-005 | FR-002 | Xem danh sách khi chưa có sản phẩm | Hệ thống hiển thị thông báo chưa có sản phẩm trong kho |
| TC-006 | FR-002 | Xem danh sách khi có sản phẩm | Hệ thống hiển thị đúng danh sách sản phẩm |
| TC-007 | FR-003 | Tìm kiếm theo Product Code tồn tại | Hệ thống trả về sản phẩm phù hợp |
| TC-008 | FR-003 | Tìm kiếm theo Product Name viết thường trong khi dữ liệu viết hoa | Hệ thống vẫn trả về sản phẩm phù hợp |
| TC-009 | FR-003 | Tìm kiếm keyword không tồn tại | Hệ thống hiển thị không tìm thấy sản phẩm phù hợp |
| TC-010 | FR-005 | Cập nhật Product Name hợp lệ | Hệ thống cập nhật thành công |
| TC-011 | FR-005 | Cập nhật Product Name rỗng | Hệ thống báo lỗi tên sản phẩm không được để trống |
| TC-012 | FR-006 | Cập nhật Quantity = 0 | Hệ thống cập nhật Status = OUT_OF_STOCK |
| TC-013 | FR-006 | Cập nhật Quantity nhỏ hơn Minimum Stock | Hệ thống cập nhật Status = LOW_STOCK |
| TC-014 | FR-006 | Cập nhật Quantity lớn hơn Minimum Stock | Hệ thống cập nhật Status = ACTIVE |
| TC-015 | FR-007 | Xoá sản phẩm và xác nhận | Sản phẩm bị xoá khỏi danh sách |
| TC-016 | FR-007 | Xoá sản phẩm nhưng bấm huỷ | Sản phẩm vẫn còn trong danh sách |

---

## 15. Requirement Traceability Matrix

| User Story | Functional Requirement | Business Rule | Acceptance Criteria | Test Case |
|---|---|---|---|---|
| US-001 | FR-001 | BR-001, BR-002, BR-003, BR-004, BR-005, BR-006 | AC-001.1 → AC-001.6 | TC-001 → TC-004 |
| US-002 | FR-002 | BR-004, BR-005, BR-006, BR-008 | AC-002.1 → AC-002.5 | TC-005, TC-006 |
| US-003 | FR-003 | BR-008, BR-010 | AC-003.1 → AC-003.6 | TC-007 → TC-009 |
| US-004 | FR-004 | BR-008 | AC-004.1 → AC-004.3 | Có thể bổ sung |
| US-005 | FR-005 | BR-002, BR-005, BR-006, BR-009 | AC-005.1 → AC-005.7 | TC-010, TC-011 |
| US-006 | FR-006 | BR-003, BR-004, BR-005, BR-006, BR-009 | AC-006.1 → AC-006.6 | TC-012 → TC-014 |
| US-007 | FR-007 | BR-007, BR-008 | AC-007.1 → AC-007.6 | TC-015, TC-016 |

---

## 16. Gợi ý output mong muốn từ từng Agent

### PO Agent

- Xác định mục tiêu sản phẩm.
- Kiểm tra scope in/out.
- Ưu tiên feature theo MVP.
- Đề xuất roadmap mở rộng sau MVP.

### BA Agent

- Phân tích requirement chi tiết.
- Chuẩn hoá business rule.
- Tạo BPMN hoặc flow nghiệp vụ.
- Tạo FRS/BRD từ requirement này.
- Tạo mapping User Story → Functional Requirement → Acceptance Criteria.

### UX/UI Agent

- Tạo wireframe cho các màn hình SCR-001, SCR-002, SCR-003.
- Đề xuất layout form tạo/sửa sản phẩm.
- Đề xuất trạng thái hiển thị cho ACTIVE, LOW_STOCK, OUT_OF_STOCK.

### FE Agent

- Tạo giao diện danh sách sản phẩm.
- Tạo form tạo/cập nhật sản phẩm.
- Tạo chức năng tìm kiếm client-side hoặc gọi API.
- Tạo modal xác nhận xoá.

### BE Agent

- Thiết kế database schema cho Product.
- Tạo CRUD API theo mục 12.
- Validate dữ liệu đầu vào.
- Xử lý logic tính Status tồn kho.

### QA Agent

- Tạo test case chi tiết từ mục 14.
- Bổ sung edge case.
- Tạo checklist kiểm thử UI/API.
- Tạo dữ liệu test mẫu.

---

## 17. Dữ liệu mẫu

| Product Code | Product Name | Description | Unit | Quantity | Minimum Stock | Expected Status |
|---|---|---|---|---:|---:|---|
| SP001 | Bàn phím cơ Keychron K2 | Bàn phím cơ không dây | cái | 15 | 5 | ACTIVE |
| SP002 | Chuột Logitech MX Master 3S | Chuột không dây văn phòng | cái | 3 | 5 | LOW_STOCK |
| SP003 | Màn hình Dell 24 inch | Màn hình văn phòng | cái | 0 | 2 | OUT_OF_STOCK |
| SP004 | Cáp USB-C 1m | Cáp sạc và truyền dữ liệu | sợi | 100 | 20 | ACTIVE |

---

## 18. Tiêu chí hoàn thành MVP

MVP được xem là hoàn thành khi hệ thống đáp ứng đầy đủ các điều kiện sau:

- Người dùng tạo được sản phẩm hợp lệ.
- Người dùng xem được danh sách sản phẩm.
- Người dùng tìm kiếm được sản phẩm theo mã hoặc tên.
- Người dùng xem được chi tiết sản phẩm.
- Người dùng cập nhật được thông tin sản phẩm.
- Người dùng cập nhật được số lượng tồn kho.
- Người dùng xoá được sản phẩm sau khi xác nhận.
- Hệ thống kiểm tra được các lỗi dữ liệu cơ bản.
- Hệ thống tự động tính đúng trạng thái tồn kho.
- QA Agent có thể tạo test case từ requirement này mà không cần thêm tài liệu khác.

---

## 19. Ghi chú cho Multi-Agent Demo

File requirement này được thiết kế để agent có thể xử lý theo chuỗi:

1. PO Agent đọc mục tiêu, scope, MVP.
2. BA Agent chuẩn hoá requirement thành BRD/FRS.
3. UX/UI Agent tạo wireframe từ screen requirement.
4. FE Agent tạo giao diện từ FRS và wireframe.
5. BE Agent tạo API/schema từ functional requirement và data model.
6. QA Agent tạo test case từ acceptance criteria và traceability matrix.