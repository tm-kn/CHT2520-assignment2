from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def root(request):
    return Response({
        "sheets": reverse('api:sheets:root', request=request),
    })
