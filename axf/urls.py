from django.conf.urls import url

from axf import views

urlpatterns = [
    url(r'^index/$', views.index),

    url(r'^home/$', views.home),


    url(r'^market/(\w+)/(\d+)/(\d+)/$', views.market),
    url(r'^cart/$', views.cart),
    #添加减少购物车
    url(r'^addSubCart/$', views.addSubCart),
    url(r'^choiceCart/$', views.choiceCart),
    url(r'^fullRight/$', views.fullRight),
    url(r'^addOrder/$', views.addOrder),
    url(r'^waitPay/$', views.waitPay),
    url(r'^havePay/$', views.havePay),
    url(r'^pay/$', views.pay),
    url(r'^orderPayOver/$', views.orderPayOver),


    url(r'^mine/$', views.mine),
    url(r'^login/$', views.login),
    url(r'^verifycode/$', views.verifycode),
    url(r'^quit/$', views.quit),
    url(r'^upImage/$', views.upImage),
    #地址
    url(r'^showAddress/$', views.showAddress),
    url(r'^addAddress/$', views.addAddress),
    url(r'^changeAddress/$', views.changeAddress),
]