from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse

class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path in ["/fullRight/", "/addOrder/", "/waitPay/", "/havePay/"]:
            request.phone = request.session.get("phone")
        if request.path in ["/cart/", "/showAddress/", "/addSubCart/"]:
            #验证是否登录
            phone = request.session.get("phone")
            path = request.GET.get("from")
            if not phone:
                #没有状态保持，说明未登录
                if request.is_ajax():
                    return JsonResponse({"error":-1})
                return redirect("/login/?from=%s"%path)
            #获取缓存
            token1 = cache.get(phone)
            token2 = request.COOKIES.get("token")
            if token1 != token2:
                return redirect("/login/?from=%s"%path)
            request.phone = request.session.get("phone")
