from playwright.sync_api import sync_playwright
import pandas as pd
import time

BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"
PRE_PACKAGED_PAGES = 12
INDIVIDUAL_TEST_PAGES = 32
ITEMS_PER_PAGE = 12


def get_paginated_urls():
    urls = []
    for page in range(1, PRE_PACKAGED_PAGES):
        urls.append((f"{BASE_URL}?start={page * ITEMS_PER_PAGE}&type=2", "Pre-Packaged Job Solution"))
    for page in range(1, INDIVIDUAL_TEST_PAGES):
        urls.append((f"{BASE_URL}?start={page * ITEMS_PER_PAGE}&type=1", "Individual Test Solution"))
    return urls


def scrape_product_details(context, link):
    detail_page = context.new_page()
    detail_page.goto(link, timeout=60000)
    detail_page.wait_for_selector("main", timeout=10000)

    try:
        desc_elem = detail_page.query_selector(".container .row .col-12.col-md-8 p")
        description = desc_elem.inner_text().strip() if desc_elem else ''
    except:
        description = ''

    try:
        job_levels = detail_page.locator("text=Job levels").nth(0).evaluate(
            "el => el.nextElementSibling?.innerText") or ''
    except:
        job_levels = ''

    try:
        languages = detail_page.locator("text=Languages").nth(0).evaluate(
            "el => el.nextElementSibling?.innerText") or ''
    except:
        languages = ''

    try:
        time_text = detail_page.locator("text=Assessment length").nth(0).evaluate(
            "el => el.nextElementSibling?.innerText") or ''
        time_minutes = ''.join(filter(str.isdigit, time_text))
    except:
        time_minutes = ''

    detail_page.close()
    return description, job_levels.strip(), languages.strip(), time_minutes


def scrape_first_page(page):
    data = []
    page.goto(f"{BASE_URL}?start=0", timeout=60000)
    page.wait_for_selector('tbody tr', timeout=10000)
    rows = page.query_selector_all('tbody tr')

    for i, row in enumerate(rows):
        try:
            category = "Pre-Packaged Job Solution" if i < 12 else "Individual Test Solution"
            print(f"[INFO] Parsing row {i + 1} as {category}")

            cells = row.query_selector_all("td")
            if len(cells) < 4:
                continue

            title_elem = cells[0].query_selector("a")
            if not title_elem:
                continue

            title = title_elem.inner_text().strip()
            relative_link = title_elem.get_attribute("href")
            full_link = f"https://www.shl.com{relative_link}"

            remote_icon = cells[1].query_selector("svg[fill='limegreen']")
            remote_testing = 'Yes' if remote_icon else 'No'

            adaptive_icon = cells[2].query_selector("svg[fill='limegreen']")
            adaptive = 'Yes' if adaptive_icon else 'No'

            test_type_boxes = cells[3].query_selector_all(".badge")
            test_types = [box.inner_text().strip() for box in test_type_boxes]

            context = page.context.browser.new_context()
            description, job_levels, languages, time_minutes = scrape_product_details(context, full_link)
            context.close()

            data.append({
                "Title": title,
                "Category": category,
                "Remote Testing": remote_testing,
                "Adaptive/IRT": adaptive,
                "Test Types": ', '.join(test_types),
                "Link": full_link,
                "Description": description,
                "Job Levels": job_levels,
                "Languages": languages,
                "Assessment Length (Minutes)": time_minutes
            })

        except Exception as e:
            print(f"  ✗ Error parsing row {i + 1}: {e}")

    return data


def scrape_shl_page(page, url, category):
    data = []
    print(f"[INFO] Visiting page: {url}")
    page.goto(url, timeout=60000)
    page.wait_for_selector('tbody tr', timeout=10000)
    rows = page.query_selector_all('tbody tr')

    for i, row in enumerate(rows):
        try:
            print(f"[INFO] Parsing row {i + 1}/{len(rows)}...")

            cells = row.query_selector_all("td")
            if len(cells) < 4:
                continue

            title_elem = cells[0].query_selector("a")
            if not title_elem:
                continue

            title = title_elem.inner_text().strip()
            relative_link = title_elem.get_attribute("href")
            full_link = f"https://www.shl.com{relative_link}"

            remote_icon = cells[1].query_selector("svg[fill='limegreen']")
            remote_testing = 'Yes' if remote_icon else 'No'

            adaptive_icon = cells[2].query_selector("svg[fill='limegreen']")
            adaptive = 'Yes' if adaptive_icon else 'No'

            test_type_boxes = cells[3].query_selector_all(".badge")
            test_types = [box.inner_text().strip() for box in test_type_boxes]

            context = page.context.browser.new_context()
            description, job_levels, languages, time_minutes = scrape_product_details(context, full_link)
            context.close()

            data.append({
                "Title": title,
                "Category": category,
                "Remote Testing": remote_testing,
                "Adaptive/IRT": adaptive,
                "Test Types": ', '.join(test_types),
                "Link": full_link,
                "Description": description,
                "Job Levels": job_levels,
                "Languages": languages,
                "Assessment Length (Minutes)": time_minutes
            })

            print(f"  ✓ Scraped: {title}")

        except Exception as e:
            print(f"  ✗ Error parsing row {i + 1}: {e}")

    return data


def scrape_shl_catalog():
    all_data = []
    start_time = time.time()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Step 1: Scrape Page 1 (Mixed)
        print("\n=== Scraping First Page (Mixed Categories) ===")
        all_data.extend(scrape_first_page(page))

        # Step 2 & 3: Remaining Pages
        for url, category in get_paginated_urls():
            all_data.extend(scrape_shl_page(page, url, category))

        browser.close()

    duration = round(time.time() - start_time, 2)
    print(f"\n✅ Scraping complete! Total products: {len(all_data)}. Time taken: {duration} seconds.")
    return all_data


def save_to_csv(data, filename="shl_catalog_full.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"[INFO] Saved {len(df)} entries to '{filename}'")


if __name__ == "__main__":
    data = scrape_shl_catalog()
    save_to_csv(data)
