from getpass import getpass

from playwright.sync_api import sync_playwright, expect

URL = "https://sso.hutech.edu.vn/login"

# ==========================================
# Thông tin đăng nhập
# ==========================================
username = input("Tài khoản: ")
password = getpass("Mật khẩu: ")  # không hiện mật khẩu khi gõ

# Loại tài khoản: CB-GV-NV / SINHVIEN_DAIHOC / HOC_VIEN
account_type = "CB-GV-NV"

ACCOUNT_TYPE_IDS = {
    "CB-GV-NV": "MOBILE_HUTECH",
    "SINHVIEN_DAIHOC": "SINHVIEN_DAIHOC",
    "HOC_VIEN": "HOC_VIEN",
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    print("🔄 Đang mở trang đăng nhập...")
    page.goto(URL, wait_until="domcontentloaded")

    # ==========================================
    # Bước 1: Chọn Loại Tài Khoản
    # ==========================================
    # Input radio là custom-control của Bootstrap: bị ẩn (opacity 0) và nằm
    # dưới label, nên .check() trên input sẽ cuộn + thử lại liên tục.
    # => Click vào label hiển thị (label.custom-control-label) thay cho input.
    print(f"🔄 Đang chọn loại tài khoản: {account_type}")
    account_type_id = ACCOUNT_TYPE_IDS[account_type]

    radio = page.locator(f"#{account_type_id}")
    radio_label = page.locator(f'label.custom-control-label[for="{account_type_id}"]')

    radio_label.wait_for(state="visible")  # chờ Angular render xong form
    radio_label.click()
    expect(radio).to_be_checked()
    print(f"✅ Đã chọn: {account_type}")

    # ==========================================
    # Bước 2: Nhập Tài Khoản
    # ==========================================
    print("🔄 Đang nhập tài khoản...")
    page.locator('input[name="username"]').fill(username)

    # ==========================================
    # Bước 3: Nhập Mật Khẩu
    # ==========================================
    print("🔄 Đang nhập mật khẩu...")
    page.locator('input[type="password"]').fill(password)

    # ==========================================
    # Bước 4: Nhấn Nút Đăng Nhập
    # ==========================================
    # 'button:has-text("Đăng nhập")' khớp cả nút "Đăng nhập bằng Google"
    # => chỉ lấy nút submit nằm trong form.
    print("🔄 Đang nhấn nút Đăng nhập...")
    login_button = page.locator("form button.btn-primary")

    expect(login_button).to_be_enabled()  # nút chỉ mở khi form hợp lệ
    login_button.click()

    # ==========================================
    # Bước 5: Chờ & Kiểm tra Kết quả
    # ==========================================
    page.wait_for_load_state("networkidle")

    print("\n" + "=" * 50)
    print("📋 KẾT QUẢ")
    print("=" * 50)
    print(f"URL hiện tại: {page.url}")
    print(f"Title: {page.title()}")

    input("\n⏸️ Nhấn Enter để đóng trình duyệt...")
    browser.close()