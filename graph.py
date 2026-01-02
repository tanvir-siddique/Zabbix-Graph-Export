from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import time
import os
import sys


# for host in $(cat hosts);do echo $host;python3 ./graph.py $host;done 
# while IFS=, read -r name id _; do mv $id $name; done < ../srv.csv

DASHBOARD_ID = sys.argv[1]

TIME_LABEL = "Last 3 hours"   # change to "Today", "Last 7 days", etc.

ZABBIX_URL = os.getenv("ZABBIX_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DASHBOARD_URL = f"{ZABBIX_URL}/zabbix.php?action=dashboard.view&dashboardid={DASHBOARD_ID}"

# Configure headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

try:
    # Open login page
    driver.get(f"{ZABBIX_URL}/index.php")

    # Fill login form
    driver.find_element(By.NAME, "name").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.NAME, "enter").click()

    # Go to dashboard
    driver.get(DASHBOARD_URL)
    time.sleep(5)  # wait for graphs to load

    button = driver.find_element(By.CSS_SELECTOR, f'a[data-label="{TIME_LABEL}"]')
    button.click()
    print(f"✅ Clicked on '{TIME_LABEL}' button")

    time.sleep(5)  # wait for graphs to reload after clicking

    widgets = driver.find_elements(By.CLASS_NAME, "dashboard-grid-widget")
    print(f"Found {len(widgets)} widgets")

    os.makedirs(f"widgets/{DASHBOARD_ID}", exist_ok=True)

    for i, widget in enumerate(widgets, start=1):
        # Scroll each widget into view
        driver.execute_script("arguments[0].scrollIntoView(true);", widget)
        time.sleep(1)

        # Save screenshot of the widget element only
        filename = f"widgets/{DASHBOARD_ID}/widget_{i}.png"
        widget.screenshot(filename)
        print(f"✅ Saved {filename}")

finally:
    driver.quit()