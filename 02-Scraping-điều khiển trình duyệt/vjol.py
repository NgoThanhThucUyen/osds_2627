"""
Thu thập thông tin bài báo khoa học trên VJOL (vjol.info.vn) bằng Playwright.
Quy trình: mở trang tìm kiếm -> nhập chủ đề -> lấy danh sách link
           -> vào từng bài lấy chi tiết -> lưu ra file Excel.
"""
import time

import pandas as pd
from playwright.sync_api import sync_playwright

# ------------------------- CẤU HÌNH -------------------------
URL_TIM_KIEM = "https://vjol.info.vn/index/vi/search/"
CHU_DE = "machine learning"        # chủ đề cần tìm
FILE_EXCEL = "ket_qua_vjol.xlsx"   # tên file kết quả
SO_BAI_TOI_DA = 200                 # giới hạn số bài cần lấy
THOI_GIAN_DUNG = 0                 # số giây dừng sau mỗi thao tác để quan sát kết quả


# ------------------------- HÀM HỖ TRỢ -------------------------
def lay_text(locator):
    """Trả về nội dung chữ của phần tử đầu tiên, hoặc chuỗi rỗng nếu không có."""
    if locator.count() == 0:
        return ""
    return locator.first.inner_text().strip()


def lay_meta(page, ten):
    """Đọc giá trị thẻ <meta name="..."> trong phần <head> của trang."""
    the = page.locator(f'meta[name="{ten}"]')
    if the.count() == 0:
        return ""
    return (the.first.get_attribute("content") or "").strip()


# ------------------------- BƯỚC 1: TÌM KIẾM -------------------------
def tim_kiem(page, chu_de):
    """Mở trang tìm kiếm, nhập chủ đề và bấm nút Tìm kiếm."""
    page.goto(URL_TIM_KIEM)
    time.sleep(THOI_GIAN_DUNG)               # dừng để quan sát trang tìm kiếm

    page.fill("#query", chu_de)
    time.sleep(THOI_GIAN_DUNG)               # dừng để thấy chủ đề đã được nhập

    page.click("button.submit")
    page.wait_for_url("**query=**")          # chờ chuyển sang trang kết quả
    page.wait_for_load_state("domcontentloaded")
    time.sleep(THOI_GIAN_DUNG)               # dừng để quan sát trang kết quả


# ------------------------- BƯỚC 2: LẤY DANH SÁCH LINK -------------------------
def lay_danh_sach_link(page, so_bai_toi_da):
    """Duyệt các trang kết quả, trả về danh sách link bài báo."""
    ds_link = []
    while len(ds_link) < so_bai_toi_da:
        cac_the_a = page.locator("ul.search_results div.obj_article_summary h3.title a")
        for i in range(cac_the_a.count()):
            link = cac_the_a.nth(i).get_attribute("href")
            if link and link not in ds_link:
                ds_link.append(link)

        # Nếu còn trang kết quả kế tiếp thì bấm sang, không thì dừng
        nut_trang_sau = page.locator("div.cmp_pagination a.next")
        if nut_trang_sau.count() == 0:
            break
        nut_trang_sau.first.click()
        page.wait_for_load_state("domcontentloaded")
        time.sleep(THOI_GIAN_DUNG)           # dừng để quan sát trang kết quả kế tiếp
    return ds_link[:so_bai_toi_da]


# ------------------------- BƯỚC 3: LẤY CHI TIẾT 1 BÀI -------------------------
def lay_chi_tiet(page, link):
    """Mở trang chi tiết của 1 bài báo và trả về dict thông tin."""
    page.goto(link)
    page.wait_for_selector("h1.page_title")
    time.sleep(THOI_GIAN_DUNG)               # dừng để quan sát trang chi tiết

    tieu_de = lay_text(page.locator("h1.page_title"))

    ds_tac_gia = page.locator("ul.authors span.name").all_inner_texts()
    tac_gia = "; ".join(t.strip() for t in ds_tac_gia if t.strip())

    # Phần tóm tắt gồm nhiều đoạn <p>; đoạn bắt đầu bằng "Keywords"/"Từ khóa" tách riêng
    tom_tat, tu_khoa = [], ""
    for doan in page.locator("section.item.abstract p").all_inner_texts():
        doan = doan.strip()
        if doan.lower().startswith(("keyword", "key word", "từ khóa", "từ khoá")):
            tu_khoa = doan.split(":", 1)[-1].strip()
        elif doan:
            tom_tat.append(doan)

    link_pdf = ""
    the_pdf = page.locator("a.obj_galley_link.pdf")
    if the_pdf.count() > 0:
        link_pdf = the_pdf.first.get_attribute("href") or ""

    return {
        "Tiêu đề": tieu_de,
        "Tác giả": tac_gia,
        "Tạp chí": lay_meta(page, "citation_journal_title"),
        "Số": lay_text(page.locator("div.item.issue a.title")),
        "Ngày xuất bản": lay_text(page.locator("div.item.published div.value")),
        "Tóm tắt": "\n".join(tom_tat),
        "Từ khóa": tu_khoa,
        "Link bài báo": link,
        "Link PDF": link_pdf,
    }


# ------------------------- BƯỚC 4: LƯU EXCEL -------------------------
def luu_excel(ds_bai_bao, ten_file):
    """Ghi danh sách bài báo ra file Excel và chỉnh độ rộng cột cho dễ đọc."""
    df = pd.DataFrame(ds_bai_bao)
    df.insert(0, "STT", range(1, len(df) + 1))
    do_rong = {"STT": 6, "Tiêu đề": 50, "Tác giả": 30, "Tạp chí": 30, "Số": 16,
               "Ngày xuất bản": 14, "Tóm tắt": 80, "Từ khóa": 30,
               "Link bài báo": 45, "Link PDF": 45}
    with pd.ExcelWriter(ten_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="BaiBao")
        sheet = writer.sheets["BaiBao"]
        for o_tieu_de in sheet[1]:
            cot = o_tieu_de.column_letter
            sheet.column_dimensions[cot].width = do_rong.get(o_tieu_de.value, 20)
        sheet.freeze_panes = "A2"


# ------------------------- CHƯƠNG TRÌNH CHÍNH -------------------------
def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)   # hiện cửa sổ trình duyệt
        page = browser.new_page()
        page.set_default_timeout(30000)      # chờ tối đa 30 giây cho mỗi thao tác

        print(f"Đang tìm kiếm chủ đề: {CHU_DE}")
        tim_kiem(page, CHU_DE)

        ds_link = lay_danh_sach_link(page, SO_BAI_TOI_DA)
        print(f"Tìm thấy {len(ds_link)} bài báo")

        ds_bai_bao = []
        for stt, link in enumerate(ds_link, start=1):
            try:
                bai = lay_chi_tiet(page, link)
                ds_bai_bao.append(bai)
                print(f"[{stt}/{len(ds_link)}] {bai['Tiêu đề'][:70]}")
            except Exception as loi:
                print(f"[{stt}/{len(ds_link)}] LỖI ở {link}: {loi}")

        browser.close()

    if ds_bai_bao:
        luu_excel(ds_bai_bao, FILE_EXCEL)
        print(f"Đã lưu {len(ds_bai_bao)} bài báo vào file {FILE_EXCEL}")
    else:
        print("Không có bài báo nào để lưu.")


if __name__ == "__main__":
    main()