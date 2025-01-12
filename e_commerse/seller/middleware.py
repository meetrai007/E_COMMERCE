class ClearSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Clear the session if the request is for the admin site
        if request.path.startswith('/admin/') and 'not_admin' in request.session:
            request.session.flush()
        response = self.get_response(request)
        return response
