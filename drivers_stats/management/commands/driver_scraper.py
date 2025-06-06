import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import time

# imports django
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "formula1_stats.settings")
django.setup()
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from drivers_stats.models import Drivers

BASE_URL = "https://www.formula1.com"
START_URL = "https://www.formula1.com/en/drivers"

@sync_to_async
def save_driver(driver):
    Drivers.objects.update_or_create(
        driver=driver["driver"],
        defaults={
            "team": driver["team"],
            "driver_number": driver["driver_number"],
            "country": driver["country"],
            "podiums": driver["podiums"],
            "season_points": driver["season_points"],
            "total_points": driver["total_points"],
            "gp_entered": driver["gp_entered"],
            "world_championships": driver["world_championships"],
            "highest_race_finish": driver["highest_race_finish"],
            "highest_grid_position": driver["highest_grid_position"],
            "date_birth": driver["date_birth"],
            "place_birth": driver["place_birth"]
        }
    )
    
async def scrape_page(page, browser, url):
    await page.goto(url)
    drivers = []

    drivers_links = page.locator("a.group[href^='/en/drivers/']")
    count = await drivers_links.count()
    print(f"Total drivers found: {count}")
    
    for i in range(count):
        link = drivers_links.nth(i)
        season_points = await link.locator("p.f1-heading-wide.font-formulaOneWide.tracking-normal.font-normal.non-italic.text-fs-18px.leading-none.normal-case").inner_text( )
        drivers_href = await link.get_attribute("href")
         
        if drivers_href:          
            driver_url = BASE_URL + drivers_href  #driver_url
            print(f"Scraping URL: {driver_url}")
            
            
            try:
                driver_details = await scrape_details(browser, driver_url, season_points)
                drivers.append(driver_details)
                print(driver_details)
            except Exception as e:
                print(f"Failed to scrape at {driver_url}: {e}") 
    return drivers

async def scrape_details(browser, driver_url, season_points):
    
    page = await browser.new_page()
    await page.goto(driver_url)
    
    driver = await page.locator("xpath=/html/body/main/div/div/div/div[1]/figure/figcaption/div/h1").text_content()
    driver_number = await page.locator("xpath=/html/body/main/div/div/div/div[1]/figure/figcaption/div/div/p").text_content()
    team = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div/div[2]/dl/dd[1]").text_content()
    country = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div/div[2]/dl/dd[2]").text_content()
    podiums = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div/div[2]/dl/dd[3]").text_content()
    total_points = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div/div[2]/dl/dd[4]").text_content()
    gp_entered = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div/div[2]/dl/dd[5]").text_content()
    world_championships = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div/div[2]/dl/dd[6]").text_content()
    highest_race_finish = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div/div[2]/dl/dd[7]").text_content()
    highest_grid_position = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div/div[2]/dl/dd[8]").text_content()
    date_birth = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div/div[2]/dl/dd[9]").text_content()
    place_birth = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div/div[2]/dl/dd[10]").text_content()

    await page.close()
         
    return {
        "driver": driver.strip() if driver else None,
        "driver_number": driver_number.strip() if driver_number else None,
        "team": team.strip() if team else None,
        "country": country.strip() if country else None,
        "podiums": int(podiums.strip()) if podiums and podiums.isdigit() else None,
        "season_points": float(season_points.strip()) if season_points else None,
        "total_points": float(total_points.strip().replace(',', '')) if total_points else None,
        "gp_entered": int(gp_entered.strip()) if gp_entered and gp_entered.isdigit() else None,
        "world_championships": int(world_championships.strip()) if world_championships and world_championships.isdigit() else None,
        "highest_race_finish": highest_race_finish.strip() if highest_race_finish else None,
        "highest_grid_position": highest_grid_position.strip() if highest_grid_position else None,
        "date_birth": datetime.strptime(date_birth.strip(), "%d/%m/%Y").date() if date_birth else None,
        "place_birth": place_birth.strip() if place_birth else None
    }

async def main():
    async with async_playwright() as p:
        brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        browser = await p.chromium.launch(
            headless=True,
            executable_path=brave_path
        )
        page = await browser.new_page()
        url = START_URL
        all_drivers = []
        

        try:
            start_time = time.time()
            print(f"Hora {start_time}")
            print(f"Scraping page: {url}")
            
            drivers = await scrape_page(page, browser, url)
            for driver in drivers:
                await save_driver(driver)
            end_time = time.time()
            elapsed_time = end_time - start_time    
            print("Saved successfully on DB")
            print(f"execution time {elapsed_time:.2f} seconds, {elapsed_time/60:.2f} minutes")   
            all_drivers.extend(drivers)
        except Exception as e:
            print(f"Failed to scrape page {url}: {e}")

        await browser.close()

class Command(BaseCommand):
    help = "Scraper Drivers F1 2025 and save to DB"

    def handle(self, *args, **kwargs):
        asyncio.run(main())