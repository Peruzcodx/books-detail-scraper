from playwright.sync_api import sync_playwright
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws.append(["Title", "Price", "Availability"])

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("http://books.toscrape.com")

    page_num = 1

    while True:
        print(f"Scraping page {page_num}...")

        books = page.locator(".product_pod").all()
        num = 0

        for book in books:
            num+=1
            title = book.locator("h3 a").get_attribute("title")
            price = book.locator(".price_color").inner_text()
            availability = book.locator(".instock.availability").inner_text().strip()
            print(f"Title:{num} {title}, Price: {price}, Availability: {availability}")
            ws.append([title, price, availability])

        next_button = page.locator("li.next a")


        if next_button.count() == 0:
            print("No more pages. Done.")
            break

        next_button.click()
        page.wait_for_load_state("networkidle")
        page_num += 1

    browser.close()

wb.save("pw_books.xlsx")
print("Saved!")
