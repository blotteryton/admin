from django.conf import settings
from users import models

def RequestExposerMiddleware(get_response):
    def middleware(request):
        models.exposed_request = request
        print("here")
        response = get_response(request)
        return response

    return middleware
