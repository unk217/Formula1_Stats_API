import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import RaceSerializer


@api_view(["GET"])
def consume_api_externa(request):
    api_url = "https://api.jolpi.ca/ergast/f1/2025/races/"
    response = requests.get(api_url)
    response.raise_for_status()

    races = response.json().get("MRData", {}).get("RaceTable", {}).get("Races", [])
    serializer = RaceSerializer(races, many=True)
    return Response(serializer.data)
