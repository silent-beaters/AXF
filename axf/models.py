from django.db import models

# Create your models here.
from axf.view_func import NON_PAYMENT

class AxfManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isDelete=False)

# class ProductManager(AxfManager):
#     def create(self):
#         obj = self.model()
#         return obj


#商品表
class Product(models.Model):
    objects = AxfManager()
    name = models.CharField(max_length=20)
    longName = models.CharField(max_length=40)
    productId = models.CharField(max_length=20)
    storeNums = models.IntegerField()
    specifics = models.CharField(max_length=20)
    sort = models.IntegerField()
    marketPrice = models.FloatField()
    price = models.FloatField()
    category = models.ForeignKey("Category")
    child = models.ForeignKey("Child")
    img = models.CharField(max_length=200)
    keywords = models.CharField(max_length=40)
    brandId = models.CharField(max_length=20)
    brandName = models.CharField(max_length=40)
    safeDay = models.CharField(max_length=20)
    safeUnit = models.CharField(max_length=20)
    safeUnitDesc = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    class Meta:
        db_table = "products"

#分组表
class Category(models.Model):
    objects = AxfManager()
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=20)
    sort = models.IntegerField()
    isDelete = models.BooleanField(default=False)
    class Meta:
        db_table = "categories"



class Child(models.Model):
    objects = AxfManager()
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=20)
    sort = models.IntegerField()
    category = models.ForeignKey("Category")
    isDelete = models.BooleanField(default=False)
    class Meta:
        db_table = "childs"


class AxfUser(models.Model):
    objects = AxfManager()
    phone = models.CharField(max_length=20, primary_key=True)
    token = models.CharField(max_length=100)
    img = models.CharField(max_length=500, null=True)
    isDelete = models.BooleanField(default=False)
    cartNum = models.IntegerField(default=0)
    class Meta:
        db_table = "axfusers"
    @classmethod
    def create(cls, phone, token, img):
        return cls(phone=phone, token=token, img=img)


class Address(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    area = models.CharField(max_length=20)
    detailAddress = models.CharField(max_length=200)
    fullAddress = models.CharField(max_length=400)
    user = models.ForeignKey("AxfUser")
    class Meta:
        db_table = "addresses"
    @classmethod
    def create(cls, name, phone, province, city, area, detailAddress, user):
        fullAddress = province + "省" + city + "市" + area + detailAddress
        return cls(name=name, phone=phone, province=province, city=city, area=area, detailAddress=detailAddress, fullAddress=fullAddress, user=user)


'''
购物车表
    所属用户   外键
    购买商品   外键
    购买数量
    是否选中
'''
class Cart(models.Model):
    user = models.ForeignKey("AxfUser")
    product = models.ForeignKey("Product")
    num = models.IntegerField()
    isChoice = models.BooleanField(default=True)
    @classmethod
    def create(cls, user, product, num):
        return cls(user=user, product=product, num=num)
    class Meta:
        db_table = "carts"

'''
订单表
    订单编号   主键
    所属用户   外键
    邮寄地址   外键
    总价
    状态   未支付、已支付、未发货、已发货、已收货、待评价、已评价、已完成(订单流转)
    创建时间
    修改时间
'''
class Order(models.Model):
    orderid = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey("AxfUser")
    address = models.ForeignKey("Address")
    price = models.FloatField()
    flag = models.IntegerField(default=NON_PAYMENT)
    createTime = models.DateTimeField(auto_now_add=True)
    lastTime = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=200, null=True)
    class Meta:
        db_table = "orders"
    @classmethod
    def create(cls, orderid, user, address, price):
        return cls(orderid=orderid, user=user, address=address, price=price)

'''
订单商品表
    所属订单   外键
    商品       外键
    数量
'''
class OrderProduct(models.Model):
    order = models.ForeignKey("Order")
    product = models.ForeignKey("Product")
    num = models.IntegerField()
    class Meta:
        db_table = "order_products"
    @classmethod
    def create(cls, order, product, num):
        return cls(order=order, product=product, num=num)

