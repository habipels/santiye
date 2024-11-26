class ExcludeFirebaseSWMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/firebase-messaging-sw.js':
            request.LANGUAGE_CODE = None
        return self.get_response(request)
