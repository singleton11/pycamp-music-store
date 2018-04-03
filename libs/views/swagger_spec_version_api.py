from rest_framework.response import Response
from rest_framework.views import APIView

from libs.swagger import get_current_swagger_spec_version


class SwaggerSpecVersionView(APIView):
    """Reports the version of the swagger specification that the API is
    supposed to be compatible with.
    """

    def get(self, request):
        return Response({
            'version': get_current_swagger_spec_version()
        })
