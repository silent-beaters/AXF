from django.shortcuts import render, redirect

from django.http import HttpResponse, JsonResponse
import random

from axf.models import Product, Category, Child, Address, Cart, Order, OrderProduct

from django.core.cache import cache

from axf.models import AxfUser
import uuid
from django.contrib.auth import logout

import os
from django.conf import settings
import oss2
import io
from PIL import Image
from axf.view_func import upfile2
from axf.view_func import NON_PAYMENT, HAVE_PAID


from alipay import AliPay

# Create your views here.
def index(request):
    return render(request, "common/base.html")


def home(request):
    return render(request, "home/home.html")










def market(request, gid, cid, sid):
    #获取组信息
    categories = Category.objects.all().order_by("sort")

    #获取子组信息
    childs = Child.objects.filter(category_id=gid)

    #获取显示商品信息
    products = Product.objects.filter(category_id=gid)
    #过滤
    if cid != "0":
        products = products.filter(child_id=cid)
    if sid == "1":
        products = products.order_by("sort")
    elif sid == "2":
        products = products.order_by("price")
    elif sid == "3":
        products = products.order_by("-price")

    #获取当前用户的购物车数据
    phone = request.session.get("phone")
    if phone:
        carts = Cart.objects.filter(user__phone=phone)
        for cart in carts:
            for product in products:
                if cart.product.id == product.id:
                    product.num = cart.num
                    break

    return render(request, "market/market.html", {"categories": categories, "products": products, "childs": childs, "gid": gid, "cid": cid})


def cart(request):
    flag = request.GET.get("flag")
    carts = Cart.objects.filter(user__phone=request.phone)

    return render(request, "cart/cart.html", {"carts": carts, "flag": flag})
def addSubCart(request):
    user = AxfUser.objects.get(pk=request.phone)
    #判断是否允许该用户继续添加购物车
    if user.cartNum >= settings.LIMIT_CART:
        return JsonResponse({"error": 1, "data":"超过购物车上限"})

    num = int(request.GET.get("num"))
    pid = int(request.GET.get("pid"))

    cart = None
    try:
        cart = Cart.objects.get(product_id=pid)
        #添加过
        cart.num += num
        if cart.num <= 0:
            cart.delete()
        else:
            cart.save()
    except Cart.DoesNotExist as e:
        if num == 1:
            #没添加过
            product = Product.objects.get(pk=pid)
            cart = Cart.create(user, product, num)
            cart.save()
    if cart:
        return JsonResponse({"error":0, "data":{"pid": cart.product.id,"num": cart.num}})
    else:
        return JsonResponse({"error": 1})

def choiceCart(request):
    cartid = int(request.GET.get("cartid"))
    cart = Cart.objects.get(pk=cartid)
    cart.isChoice = not cart.isChoice
    cart.save()
    flag = 0
    if cart.isChoice:
        flag = 1
    return JsonResponse({"error": 0, "data":flag})
def fullRight(request):
    carts = Cart.objects.filter(user__phone=request.phone)
    if not len(carts):
        return JsonResponse({"error": 1})
    # 1
    flag = int(request.GET.get("flag"))
    choice = False
    if not flag:
        choice = True
        flag = 1
    else:
        flag = 0
    for cart in carts:
        cart.isChoice = choice
        cart.save()
    return JsonResponse({"error": 0,"data":{"flag":flag}})


#下订单
def addOrder(request):
    carts = Cart.objects.filter(user__phone=request.phone).filter(isChoice=True)
    if not len(carts):
        return redirect("/cart/?from=cart&flag=1")

    address = Address.objects.get(pk=1)
    user = AxfUser.objects.get(pk=request.phone)
    orderid = str(uuid.uuid4())
    price = 0
    for cart in carts:
        price += (cart.num * cart.product.price)
    order = Order.create(orderid, user, address, price)

    order.save()
    #将购物车数据添加到订单商品表中
    for cart in carts:
        orderProduct = OrderProduct.create(order,cart.product,cart.num)
        orderProduct.save()
        cart.delete()
    return redirect("/waitPay/")

def waitPay(request):
    orders = Order.objects.filter(user__phone=request.phone).filter(flag=NON_PAYMENT)
    return render(request, "mine/waitPay.html", {"orders": orders})
def havePay(request):
    orders = Order.objects.filter(user__phone=request.phone).filter(flag=HAVE_PAID)
    return render(request, "mine/havePay.html", {"orders": orders})
def pay(reqeust):
    orderid = reqeust.GET.get("orderid")
    order = Order.objects.get(pk=orderid)

    #支付成功

    alipay = AliPay(
        appid=settings.APPID,
        app_notify_url=None,
        app_private_key_string=settings.APP_PRIVATE_KEY,
        alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY,
        sign_type="RSA",
        debug = False
    )

    # order_string = alipay.api_alipay_trade_wap_pay(
    #     out_trade_no=orderid,
    #     total_amount=10000,
    #     subject="三只松鼠",
    #     return_url="http://www.sunck.wang:8001/orderPayOver/",
    #     notify_url="http://www.sunck.wang:8001/home"
    # )

    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=orderid,
        total_amount=order.price,
        subject="闪零小分队",
        return_url="http://39.105.32.156:8000/orderPayOver/",
        notify_url="http://39.105.32.156:8000/home"
    )


    return redirect("https://openapi.alipaydev.com/gateway.do?"+order_string)
def orderPayOver(request):
    # print("-------------------------orderPayOver")
    # print(request.GET)
    order = Order.objects.get(pk=request.GET.get("out_trade_no"))
    order.flag = HAVE_PAID
    order.save()
    return redirect("/havePay/")


def mine(request):
    phone = request.session.get("phone")
    user = None
    money1 = 0
    money2 = 0
    if phone:
        user = AxfUser.objects.get(pk=phone)
        money1 = Order.objects.filter(flag=NON_PAYMENT).count()
        money2 = Order.objects.filter(flag=HAVE_PAID).count()
    return render(request, "mine/mine.html", {"phone": phone, "user": user, "money1": money1, "money2": money2})
def login(request):
    if request.method == "GET":
        path = request.GET.get("from")
        return render(request, "mine/login.html", {"path": path})
    else:
        phone = request.POST.get("phone")
        tokenValue = str(uuid.uuid4())
        #判断reids数据库是否存在（phone:token值）
        if cache.get(phone):
            #用户存在
            user = AxfUser.objects.get(pk=phone)
            #修改的token
            user.token = tokenValue
            # urlPath = "/mine/"
            urlPath = "/" + request.GET.get("from") + "/"
        else:
            #用户不存在
            user = AxfUser.create(phone, tokenValue, None)
            urlPath = "/upImage/"
        user.save()
        #状态保持
        request.session["phone"] = phone
        # 同步到redis
        cache.set(phone, tokenValue)
        response = redirect(urlPath)
        # 将token值写入cookie
        response.set_cookie("token", tokenValue)
        return response
def verifycode(request):
    str = '1234567890'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 6):
        rand_str += str[random.randrange(0, len(str))]
    # 将验证码以短信的形式发出
    # phone = request.GET.get("phone")
    # text = "您的验证码是：%s。请不要把验证码泄露给其他人。"%rand_str
    # send_sms(text, phone)
    #存储到session
    rand_str = "1"
    request.session["verifycode"] = rand_str
    print("----------------", rand_str)
    return JsonResponse({"error": 0, "data":{"verifycode": rand_str}})
def quit(request):
    logout(request)
    #删除客户端中的名为token的cookie键值对
    response = redirect("/mine/")
    response.delete_cookie("token")
    return response
def upImage(request):
    if request.method == "GET":
        return render(request, "mine/upImage.html")
    else:
        for key in request.FILES:
            files = request.FILES.getlist(key)
            for file in files:
                fileName = str(uuid.uuid4()) + ".jpg"
                # filePath = os.path.join(settings.MEDIA_ROOT, fileName)
                # with open(filePath, "wb") as fp:
                #     for info in file.chunks():
                #         fp.write(info)
                # url = upfile1(fileName, filePath)
                imgage = Image.open(file)
                buf = io.BytesIO()
                imgage.save(buf, "png")
                url = upfile2(fileName, buf.getvalue())
                #找到当前用户
                phone = request.session.get("phone")
                user = AxfUser.objects.get(pk=phone)
                user.img = url
                user.save()
        return redirect("/mine/")


def showAddress(request):
    phone = request.session.get("phone")
    addresses = Address.objects.filter(user_id=phone)
    return render(request, "mine/showAddress.html", {"addresses": addresses})


def addAddress(request):
    if request.method == "GET":
        return render(request, "mine/addAddress.html")
    else:
        phone = request.session.get("phone")
        user = AxfUser.objects.get(pk=phone)
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        province = request.POST.get("province")
        city = request.POST.get("city")
        area = request.POST.get("area")
        detailAddress = request.POST.get("location")
        address = Address.create(name, phone, province, city, area, detailAddress, user)
        address.save()
        return redirect("/showAddress/?from=showAddress")


def changeAddress(request):
    if request.method == "GET":
        addressid = request.GET.get("addressid")
        address = Address.objects.get(pk=addressid)
        return render(request, "mine/changeAddress.html", {"address": address})
    else:
        addressid = request.POST.get("addressid")
        address = Address.objects.get(pk=addressid)
        address.name = request.POST.get("name")
        address.phone = request.POST.get("phone")
        address.province = request.POST.get("province")
        address.city = request.POST.get("city")
        address.area = request.POST.get("area")
        address.detailAddress = request.POST.get("location")
        address.save()
        return redirect("/showAddress/?from=showAddress")
