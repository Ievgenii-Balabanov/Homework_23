import asyncio
import aiohttp
import time
import os

from dotenv import load_dotenv


def configure():
    load_dotenv()


async def get_json(client, url):
    async with client.get(url, ssl=False) as response:
        assert response.status == 200
        return await response.json()


async def get_visualcrossing_api(client, url):
    api_url = await get_json(client, url)
    temperature = api_url["currentConditions"]["temp"]

    print(f"Temperature by 'Visualcrossing.com' is: {temperature} ºC")
    return temperature


async def get_oceandrivers_api(client, url):
    api_url = await get_json(client, url)
    temperature = api_url["TEMPERATURE"]

    print(f"Temperature by 'Oceandrivers.com' is: {temperature} ºC")
    return temperature


async def get_open_meteo_api(client, url):
    api_url = await get_json(client, url)
    temperature = api_url["current_weather"]["temperature"]

    print(f"Temperature by 'Open-meteo.com' is: {temperature} ºC")
    return temperature


async def get_weatherapi_api(client, url):
    api_url = await get_json(client, url)
    temperature = api_url["current"]["temp_c"]

    print(f"Temperature by 'Weatherapi.com' is: {temperature} ºC")
    return temperature


async def main():
    configure()
    loop = asyncio.get_running_loop()
    async with aiohttp.ClientSession(loop=loop) as client:
        visualcrossing, oceandrivers, weatherapi, open_meteo = await asyncio.gather(  # noqa E501
            get_visualcrossing_api(
                client,
                f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services"  # noqa E501
                f"/timeline/new%20york?unitGroup=metric&include=current%2Cfcst&key="  # noqa E501
                f"{os.getenv('VISUALCROSSING_API_KEY')}&options=nonulls&contentType=json",  # noqa E501
            ),
            get_oceandrivers_api(
                client,
                "https://api.oceandrivers.com:443/v1.0/getWeatherDisplay/new%20york/?period=latestdata",  # noqa E501
            ),
            get_weatherapi_api(
                client,
                f"http://api.weatherapi.com/v1/current.json?key={os.getenv('WEATHERAPI')}&q"  # noqa E501
                f"=New York&aqi=no",
            ),
            get_open_meteo_api(
                client,
                "https://api.open-meteo.com/v1/forecast?latitude=40.7143&longitude=-74.006"  # noqa E501
                "&current_weather=true",
            ),
        )

        temperature_list = visualcrossing + oceandrivers + weatherapi + open_meteo  # noqa E501
        average_temperature = temperature_list / 4
        print()
        print(f"Average current temperature in New York is: {round(average_temperature, 1)}ºC")  # noqa E501


if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"File: {__file__} was executed in {elapsed:0.2f} seconds.")
