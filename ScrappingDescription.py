import asyncio
import csv
from playwright.async_api import async_playwright

BASE_URL = "https://infosec-conferences.com"

async def safe_inner_text(element):
    try:
        return (await element.inner_text()).strip()
    except Exception:
        return ""

async def get_event_detail(page, url):
    try:
        await page.goto(url, timeout=60000, wait_until="domcontentloaded")
        await asyncio.sleep(1)  # esperar carga JS

        # Intentar varios selectores comunes para descripción
        selectors = [
            "div.event-description",
            "div#eventContent",
            "section.description",
            "article",
            "div.content"
        ]
        for sel in selectors:
            el = await page.query_selector(sel)
            if el:
                desc = await safe_inner_text(el)
                if desc:
                    return desc
        return ""
    except Exception as e:
        return f"Error: {e}"

async def scrape_events(output_csv="infosec_with_descriptions.csv"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(BASE_URL)
        await page.wait_for_selector("table.table-striped tbody tr", timeout=60000)

        with open(output_csv, "w", encoding="utf-8", newline="") as f_out:
            writer = csv.writer(f_out)
            # Escribir encabezados + descripción
            header_cells = await page.query_selector_all("table.table-striped thead tr th")
            headers = [await safe_inner_text(cell) for cell in header_cells]
            headers.append("Description")
            writer.writerow(headers)

            while True:
                rows = await page.query_selector_all("table.table-striped tbody tr")
                for row in rows:
                    cols = await row.query_selector_all("td")
                    row_data = []
                    event_url = None
                    for idx, col in enumerate(cols):
                        text = await safe_inner_text(col)
                        row_data.append(text)
                        if idx == 0:
                            link = await col.query_selector("a")
                            if link:
                                href = await link.get_attribute("href")
                                if href and href.startswith("/"):
                                    event_url = BASE_URL + href
                                else:
                                    event_url = href
                    description = ""
                    if event_url:
                        description = await get_event_detail(page, event_url)
                        await asyncio.sleep(0.5)
                    row_data.append(description)
                    writer.writerow(row_data)

                next_button = await page.query_selector("ul.pagination li.page-item.next:not(.disabled) a")
                if next_button:
                    await next_button.click()
                    await page.wait_for_load_state("networkidle")
                    await page.wait_for_selector("table.table-striped tbody tr", timeout=60000)
                    await asyncio.sleep(1)
                else:
                    break

        await browser.close()
        print(f"Scraping completado. Datos guardados en {output_csv}")

if __name__ == "__main__":
    asyncio.run(scrape_events())
