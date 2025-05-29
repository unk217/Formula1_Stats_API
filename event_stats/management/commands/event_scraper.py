# imports del script
import asyncio
import re
#import json
from playwright.async_api import async_playwright

# imports django
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "formula1_stats.settings")
django.setup()
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand

from event_stats.models import Event

BASE_URL = "https://www.formula1.com"
START_URL = "https://www.formula1.com/en/racing/2025"
CIRCUIT_URL = "/circuit"

@sync_to_async
def save_event(event):
    Event.objects.update_or_create(
                    event = event["event"],
                    defaults= {
                        "country": event["country"],
                        "circuit": event["circuit"],
                        "city": event["city"],
                        "date": event["date"],
                        "first_gp": event["first_gp"],
                        "number_laps": event["number_laps"],
                        "circuit_lenght": event["circuit_lenght"],
                        "race_distance": event["race_distance"],
                        "lap_record": event["lap_record"],
                        }
                )

async def scrape_page(page, browser, url):
    await page.goto(url)
    circuits = []

    circuits_links = await page.query_selector_all("a.group[href^='/en/racing/2025/']")
    for link in circuits_links:

        circuits_href = await link.get_attribute("href")
        
        if circuits_href:
            
            if "pre-season-testing" in circuits_href.lower():
                print(f"Skipping pre-season-testing: {circuits_href}")
                continue
                     
            circuit_url = BASE_URL + circuits_href + CIRCUIT_URL
            print(f"Scraping URL: {circuit_url}")
            
            try:
                event_details = await scrape_details(browser, circuit_url)
                circuits.append(event_details)
                print(event_details)
            except Exception as e:
                print(f"Failed to scrape at {circuit_url}: {e}")
                print(circuit_url)
    return circuits  

async def scrape_details(browser, circuit_url):
    
    page = await browser.new_page()
    await page.goto(circuit_url)
    
    event = await page.locator("xpath=/html/body/main/div[2]/div/div[1]/div[1]/p").text_content()
    country = await page.locator("xpath=/html/body/main/div[1]/section/div/h1").text_content()
    circuit = await page.locator("xpath=/html/body/main/div[2]/div/div[2]/div/div[1]/div[1]/h2").text_content()
    city = await page.locator("xpath=/html/body/main/div[2]/div/div[3]/div/div[1]/section/div/h2[1]").text_content()
    date = await page.locator("xpath=/html/body/main/div[1]/section/div/span").text_content()
    first_gp = await page.locator("xpath=/html/body/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div[1]/h2").text_content()
    number_laps = await page.locator("xpath=/html/body/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div[2]/h2").text_content()
    circuit_lenght = await page.locator("xpath=/html/body/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div[3]/h2").text_content()
    race_distance = await page.locator("xpath=/html/body/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div[4]/h2").text_content()
    lap_record = await page.locator("xpath=/html/body/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div[5]/h2").text_content()
    
    
    
    await page.close()
    
     # --- Transformaciones de datos ---
    # Para 'date': Quitar espacios extra y normalizar
    if date:
        date = " ".join(date.strip().split()) # Esto divide por cualquier espacio y une con un solo espacio
    
    # Para 'lap_record': Añadir un espacio entre el tiempo y el nombre
    if lap_record:
        # Usamos una expresión regular para encontrar el patrón de tiempo y el nombre.
        # El patrón r"(\d{1,2}:\d{2}.\d{3})(.*)" busca un tiempo (ej. 1:30.734)
        # en el primer grupo, y el resto (el nombre) en el segundo grupo.
        
        match = re.match(r"(\d{1,2}:\d{2}\.\d{3})(.*)", lap_record)
        if match:
            time_part = match.group(1)
            name_part = match.group(2).strip() # Limpiamos espacios del nombre
            lap_record = f"{time_part} {name_part}"
        else:
            # Si no encuentra el patrón, solo limpia el string original.
            lap_record = lap_record.strip()
    
    return {
        "event": event.strip() if event else None,
        "country": country.strip() if country else None,
        "circuit": circuit.strip() if circuit else None,
        "city": city.strip() if city else None,
        "date": date.strip() if date else None,
        "first_gp": first_gp.strip() if first_gp else None,
        "number_laps": number_laps.strip() if number_laps else None,
        "circuit_lenght": circuit_lenght.strip() if circuit_lenght else None,
        "race_distance": race_distance.strip() if race_distance else None,
        "lap_record": lap_record if lap_record else None,
        
        
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
        #all_circuits = []

        try:
            print(f"Scraping page: {url}")
            circuits = await scrape_page(page, browser, url)
            #all_circuits.extend(circuits)
            for event in circuits:
                await save_event(event)
                print(f"Saved event: {event['event']}")
            print("saved successfully on DB")
       
        except Exception as e:
            print(f"Failed to scrape page {url}: {e}")

       # print("F1 events have been saved to F1.json")

        await browser.close()

class Command(BaseCommand):
    help = "Scrapea eventos F1 2025 y los guarda en la base de datos"

    def handle(self, *args, **kwargs):
        asyncio.run(main())
