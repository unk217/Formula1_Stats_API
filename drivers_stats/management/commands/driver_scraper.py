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
            "driver_picture": driver["driver_picture"],
            "podiums": driver["podiums"],
            "season_points": driver["season_points"],
            "career_points": driver["career_points"],
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

    drivers_links = page.locator('a[data-f1rd-a7s-click="driver_card_click"]')
    count = await drivers_links.count()
    print(f"Total drivers found: {count}")
    
    for i in range(count):
        link = drivers_links.nth(i)
        #season_points = await link.locator("p.f1-heading-wide.font-formulaOneWide.tracking-normal.font-normal.non-italic.text-fs-18px.leading-none.normal-case").inner_text( )
        drivers_href = await link.get_attribute("href")
         
        if drivers_href:          
            driver_url = BASE_URL + drivers_href  #driver_url
            print(f"Scraping URL: {driver_url}")
            
            
            try:
                driver_details = await scrape_details(browser, driver_url)
                drivers.append(driver_details)
                print(driver_details)
            except Exception as e:
                print(f"Failed to scrape at {driver_url}: {e}") 
    return drivers

async def scrape_details(browser, driver_url):
    
    page = await browser.new_page()
    await page.goto(driver_url)
    
    driver = await page.locator("xpath=/html/body/div[1]/main/div/div/div[2]/div[1]/div/div/div[7]/div[2]/div[1]/h1/span[2]").text_content()
    driver_number = await page.locator("xpath=/html/body/div[1]/main/div/div/div[2]/div[1]/div/div/div[7]/div[2]/div[1]/div/p[2]").text_content()
    team = await page.locator("xpath=/html/body/div[1]/main/div/div/div[2]/div[1]/div/div/div[7]/div[2]/div[1]/div/p[1]").text_content()
    driver_picture = await page.locator("xpath=/html/body/div[1]/main/div/div/div[2]/div[1]/div/div/div[4]/img").get_attribute("src")
    country = await page.locator("xpath=/html/body/div[1]/main/div/div/div[2]/div[1]/div/div/div[7]/div[2]/div[1]/div/div/p").text_content()
    podiums = await page.locator("xpath=/html/body/div[1]/main/div/div/div[2]/div[2]/div/div/div/div/div[1]/div/div[1]/dl[2]/div[6]/dd").text_content()
    season_points = await page.locator("xpath=/html/body/div[1]/main/div/div/div[2]/div[2]/div/div/div/div/div[1]/div/div[1]/dl[1]/div[2]/dd").text_content()
    career_points = await page.locator("xpath=/html/body/div[1]/main/div/div/div[2]/div[2]/div/div/div/div/div[3]/div/dl/div[2]/dd").text_content()
    gp_entered = await page.locator("xpath=/html/body/div[1]/main/div/div/div[2]/div[2]/div/div/div/div/div[3]/div/dl/div[1]/dd").text_content()
    world_championships = await page.locator("xpath=/html/body/div[1]/main/div/div/div[2]/div[2]/div/div/div/div/div[3]/div/dl/div[7]/dd").text_content()
    highest_race_finish = await page.locator("xpath=/html/body/div[1]/main/div/div/div[2]/div[2]/div/div/div/div/div[3]/div/dl/div[3]/dd").text_content()
    highest_grid_position = await page.locator("xpath=/html/body/div[1]/main/div/div/div[2]/div[2]/div/div/div/div/div[3]/div/dl/div[5]/dd").text_content()
    date_birth = await page.locator("xpath=/html/body/div[1]/main/div/div/div[2]/div[3]/div/div/div/div[1]/div[2]/dl/div[1]/dd").text_content()
    place_birth = await page.locator("xpath=/html/body/div[1]/main/div/div/div[2]/div[3]/div/div/div/div[1]/div[2]/dl/div[2]/dd").text_content()

    await page.close()
         
    return {
        "driver": driver.strip() if driver else None,
        "driver_number": driver_number.strip() if driver_number else None,
        "team": team.strip() if team else None,
        "driver_picture": driver_picture.strip() if driver_picture else None,
        "country": country.strip() if country else None,
        "podiums": int(podiums.strip()) if podiums and podiums.isdigit() else None,
        "season_points": float(season_points.strip()) if season_points else None,
        "career_points": float(career_points.strip().replace(',', '')) if career_points else None,
        "gp_entered": int(gp_entered.strip()) if gp_entered and gp_entered.isdigit() else None,
        "world_championships": int(world_championships.strip()) if world_championships and world_championships.isdigit() else None,
        "highest_race_finish": highest_race_finish.strip() if highest_race_finish else None,
        "highest_grid_position": highest_grid_position.strip() if highest_grid_position else None,
        "date_birth": datetime.strptime(date_birth.strip(), "%d/%m/%Y").date() if date_birth else None,
        "place_birth": place_birth.strip() if place_birth else None
    }

async def main():
    async with async_playwright() as p:
        #brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        brave_path = "/usr/bin/brave-browser"
        browser = await p.chromium.launch(
            headless=False,
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