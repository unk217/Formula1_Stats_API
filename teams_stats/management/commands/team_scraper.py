from asgiref.sync import sync_to_async
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import time

import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "formula1_stats.settings")
django.setup()
from django.core.management.base import BaseCommand
from teams_stats.models import Team

BASE_URL = "https://www.formula1.com"
START_URL = "https://www.formula1.com/en/teams"

@sync_to_async
def save_team(team):
    Team.objects.update_or_create(
        name=team["name"],
        defaults={
            "full_name": team["full_name"],
            "points": team["points"],
            "base": team["base"],
            "team_principal": team["team_principal"],
            "chassis": team["chassis"],
            "power_unit": team["power_unit"],
            "first_entry": team["first_entry"],
            "world_championships": team["world_championships"],
            "highest_race_finish": team["highest_race_finish"],
            "pole_positions": team["pole_positions"],
            "fastest_laps": team["fastest_laps"],	
        }
        )

async def scrape_page(page, browser, url):
    await page.goto(url)
    teams = []

    teams_links = page.locator("a.group[href^='/en/teams/']")
    count = await teams_links.count()
    print(f"Total teams found: {count}")
    
    for i in range(count):
        link = teams_links.nth(i)
        name = await link.locator("div.f1-inner-wrapper.flex.flex-col.gap-micro.text-brand-black").inner_text()
        points = await link.locator("p.f1-heading-wide.font-formulaOneWide.tracking-normal.font-normal.non-italic.text-fs-18px.leading-none.normal-case").inner_text()
        team_href = await link.get_attribute("href")
        
        if team_href:
            team_url = BASE_URL + team_href
            print(f"Scraping URL: {team_url}")
            
            try:
                team_details = await scrape_details(browser, team_url, name, points)
                teams.append(team_details)
                print(team_details)
            except Exception as e:
                print(f"Error scraping {team_url}: {e}")

    return teams

async def scrape_details(browser, team_url, name, points):
        page = await browser.new_page()
        #await page.set_default_timeout(60000)  # Set timeout to 60 seconds
        await page.goto(team_url)
        
        full_name = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div[1]/div[2]/dl/dd[1]").inner_text()
        base = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div[1]/div[2]/dl/dd[2]").inner_text()
        team_principal = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div[1]/div[2]/dl/dd[3]").inner_text()
        chassis = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div[1]/div[2]/dl/dd[5]").inner_text()
        power_unit = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div[1]/div[2]/dl/dd[6]").inner_text()
        first_entry = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div[1]/div[2]/dl/dd[7]").inner_text()
        world_championships = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div[1]/div[2]/dl/dd[8]").inner_text()
        highest_race_finish = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div[1]/div[2]/dl/dd[9]").inner_text()
        pole_positions = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div[1]/div[2]/dl/dd[10]").inner_text()
        fastest_laps = await page.locator("xpath=/html/body/main/div/div/div/div[1]/div[1]/div[2]/dl/dd[11]").inner_text()
        
        await page.close()
        
        return {
            "name": name.strip() if name else None,
            "full_name": full_name.strip() if full_name else None,
            "points": float(points.strip()) if points else None,
            "base": base.strip() if base else None,
            "team_principal": team_principal.strip() if team_principal else None,
            "chassis": chassis.strip() if chassis else None,
            "power_unit": power_unit.strip() if power_unit else None,
            "first_entry": first_entry.strip() if first_entry else None,
            "world_championships": int(world_championships.strip()) if world_championships and world_championships.isdigit() else 0,
            "highest_race_finish": highest_race_finish.strip() if highest_race_finish else None,
            "pole_positions": int(pole_positions.strip()) if pole_positions and pole_positions.isdigit() else 0,
            "fastest_laps": int(fastest_laps.strip()) if fastest_laps and fastest_laps.isdigit() else 0,
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
        all_teams = []
        
        try:
            start_time = time.time()
            print(f"Hora {start_time}")
            print(f"Scraping page: {url}")
            teams = await scrape_page(page, browser, url)
            for team in teams:
                await save_team(team)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("Saved successfully on DB")
            print(
                f"Scraping completed in {elapsed_time:.2f} seconds {elapsed_time/60:.2f} minutes")
            all_teams.extend(teams)
        except Exception as e:
            print(f"Failed to scrape teams:{url}: {e}")
            
        await browser.close()
            
class Command(BaseCommand):
    help = "Scraper Teams F1 2025 and save to DB"

    def handle(self, *args, **kwargs):
        asyncio.run(main())