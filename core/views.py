from rest_framework.views import APIView
from rest_framework.response import Response



class APIRootView(APIView):
    """
    Endpoint for the API root, providing links to other API endpoints.
    """
    def get(self, request, format=None):
        return Response({
        "drivers": request.build_absolute_uri("drivers"),
        "events": request.build_absolute_uri("events"),
        "teams": request.build_absolute_uri("teams"),
    })