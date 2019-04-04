from rest_framework.reverse import reverse

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def root(request):
    return Response({
        "sheets":
        reverse('api:sheets:root', request=request),
    })
