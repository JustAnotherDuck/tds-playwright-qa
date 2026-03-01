import asyncio
from playwright.async_api import async_playwright

# REPLACE THESE WITH YOUR 10 ACTUAL LINKS FROM THE ASSIGNMENT
URLS = [
    "https://sanand0.github.io/tdsdata/js_table/?seed=58",
    "https://sanand0.github.io/tdsdata/js_table/?seed=59",
    "https://sanand0.github.io/tdsdata/js_table/?seed=60",
    "https://sanand0.github.io/tdsdata/js_table/?seed=61",
    "https://sanand0.github.io/tdsdata/js_table/?seed=62
    "https://sanand0.github.io/tdsdata/js_table/?seed=63",
    "https://sanand0.github.io/tdsdata/js_table/?seed=64",
    "https://sanand0.github.io/tdsdata/js_table/?seed=65",
    "https://sanand0.github.io/tdsdata/js_table/?seed=66",
    "https://sanand0.github.io/tdsdata/js_table/?seed=67"
]

async def main():
    total_sum = 0.0
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for i, url in enumerate(URLS):
            print(f"Scraping Page {i+1}...")
            await page.goto(url)
            
            # Wait for dynamic network requests to finish so the table renders
            await page.wait_for_load_state("networkidle")
            
            # Inject JavaScript directly into the browser to cleanly sum the table cells
            page_sum = await page.evaluate('''() => {
                let sum = 0;
                document.querySelectorAll("td").forEach(td => {
                    // Remove commas and extract the number
                    let text = td.innerText.replace(/,/g, '');
                    let match = text.match(/-?\\d+(\\.\\d+)?/);
                    if (match) {
                        sum += parseFloat(match[0]);
                    }
                });
                return sum;
            }''')
            
            total_sum += page_sum
            
        await browser.close()
        
    # The grader will read this exact log line
    print("=" * 40)
    print(f"FINAL TOTAL SUM: {total_sum}")
    print("=" * 40)

if __name__ == "__main__":
    asyncio.run(main())
