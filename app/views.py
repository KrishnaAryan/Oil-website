from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def home(request):
#  return render(request, 'app/index.html')
class ProductView(View):
    def get(self, request):
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        
        vegetable = Product.objects.filter(category='Vegetable')
        canola = Product.objects.filter(category='Canola')
        sunflower = Product.objects.filter(category='Sunflower')
        olive = Product.objects.filter(category='Olive')
        peanut = Product.objects.filter(category='Peanut')
        sesame = Product.objects.filter(category='Sesame')
        coconut = Product.objects.filter(category='Coconut')
        corn = Product.objects.filter(category='Corn')
        soybean = Product.objects.filter(category='Soybean')
        palm = Product.objects.filter(category='Palm')
        return render(request, 'app/index.html',{'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles, 'vegetable': vegetable, 'canola': canola, 'sunflower': sunflower, 'olive': olive, 'peanut': peanut, 'sesame': sesame, 'coconut': coconut, 'corn': corn, 'soybean': soybean, 'palm': palm})


# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetails(View):
    def get(self, request, pk):
        product=Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
    user= request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        # print(cart)
        amount=0.0
        # shiping is is fixed 80.0
        shipping_amount=80.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity * p.product.discount_price)
                amount +=tempamount
                totalamount=amount +shipping_amount
            return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount,'shipping_amount':shipping_amount})
        else:
            return render(request, 'app/emptycart.html')
@login_required
def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        # shiping is is fixed 80.0
        shipping_amount=80.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discount_price)
            amount +=tempamount
            # totalamount=amount +shipping_amount

        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)
@login_required
def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        # shiping is is fixed 80.0
        shipping_amount=80.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discount_price)
            amount +=tempamount
            # totalamount=amount +shipping_amount

        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)
@login_required
def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        # c.quantity-=1
        c.delete()
        amount=0.0
        # shiping is is fixed 80.0
        shipping_amount=80.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discount_price)
            amount +=tempamount


        data={
            # 'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)
@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form= CustomerProfileForm()
        return render(request, 'app/profile.html',{'form':form, 'active':'btn-primary'})
    def post(self, request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Coustomer(user=user,name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Update Successfully')
        return render(request, 'app/profile.html',{'form':form, 'active':'btn-primary'})
@login_required
def address(request):
    add=Coustomer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add,'active':'btn-primary'})
@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed':op})

def mobile(request, data=None):
    if data == None:
        mobiles=Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data== 'below':
        mobiles=Product.objects.filter(category='M').filter(discount_price__lt=10000)
    elif data== 'above':
        mobiles=Product.objects.filter(category='M').filter(discount_price__gt=10000)
    return render(request, 'app/mobile.html', {'mobiles':mobiles})

def laptop(request, data=None):
    if data == None:
        laptop=Product.objects.filter(category='L')
    elif data == 'Redmi' or data == 'Samsung':
        laptop=Product.objects.filter(category='L').filter(brand=data)
    elif data== 'below':
        laptop=Product.objects.filter(category='L').filter(discount_price__lt=10000)
    elif data== 'above':
        laptop=Product.objects.filter(category='L').filter(discount_price__gt=10000)
    return render(request, 'app/laptop.html', {'laptop':laptop})

def topwear(request, data=None):
    if data == None:
        topwear=Product.objects.filter(category='TW')
    elif data == 'Redmi' or data == 'Samsung':
        topwear=Product.objects.filter(category='TW').filter(brand=data)
    elif data== 'below':
        topwear=Product.objects.filter(category='TW').filter(discount_price__lt=10000)
    elif data== 'above':
        topwear=Product.objects.filter(category='TW').filter(discount_price__gt=10000)
    return render(request, 'app/topwear.html', {'topwear':topwear})

def bottomwear(request, data=None):
    if data == None:
        bottomwear=Product.objects.filter(category='BW')
    elif data == 'Redmi' or data == 'Samsung':
        bottomwear=Product.objects.filter(category='BW').filter(brand=data)
    elif data== 'below':
        bottomwear=Product.objects.filter(category='BW').filter(discount_price__lt=10000)
    elif data== 'above':
        bottomwear=Product.objects.filter(category='BW').filter(discount_price__gt=10000)
    return render(request, 'app/bottomwear.html', {'bottomwear':bottomwear})


# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
class CustomerRegistrationFormView(View):
    def get(self, request):
        form= CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self, request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulation!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})
@login_required      
def checkout(request):
    user=request.user
    add=Coustomer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=80
    totalamount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity * p.product.discount_price)
            amount +=tempamount
        totalamount=amount+shipping_amount
    return render(request, 'app/checkout.html',{'add':add, 'totalamount':totalamount, 'cart_items':cart_items ,"shipping_amount":shipping_amount},)
@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Coustomer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")
        