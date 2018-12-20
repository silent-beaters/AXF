from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class VerifycodeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == "/login/" and request.method == "POST":
            verifycode1 = request.POST.get("verifycode")
            verifycode2 = request.session.get("verifycode")
            if verifycode1 != verifycode2:
                return redirect("/login/")
        return None

