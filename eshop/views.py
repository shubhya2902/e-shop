from random import random

from django.shortcuts import render, redirect, HttpResponse
from main.models import Category,Product,Contact_us,Order1,Brand
from django.contrib.auth import authenticate,login
from main.models import Usercreateform
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

def Master(request):
    return render(request,'master.html')

def Index(request):
    category = Category.objects.all()
    categoryID = request.GET.get('category')
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')

    if categoryID: #jar category id bhetla tr tya id chya related jevdhe products ahet tevdhe display honar
        product = Product.objects.filter(sub_category = categoryID).order_by('-id')  #order by -id he je item recently (saglayt shevti ) add kelet te display honyasathi
    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')
    else:
        product = Product.objects.all() #jar tyala catgory id nahi bhetla tr all products display honar

    context = {
        'category':category,
        'product':product,
        'brand':brand,
    }
    return render(request, 'index.html',context)

def signup(request):
    if request.method == 'POST':
        form = Usercreateform(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
            )
            login(request,new_user)
            return redirect('index')
    else:
        form = Usercreateform()

    context = {
            'form':form
    }

    return render(request,'registration/signup.html',context)


@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")

@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")

@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")

@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement (product=product)
    return redirect("cart_detail")

@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request,'cart/cart_detail.html')



def contact_page(request):
    if request.method == "POST":
        contact = Contact_us(
            name= request.POST.get('name'),
            email = request.POST.get('email'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message')
        )
        contact.save()

    return render(request,'contact.html')



def checkout(request):
    if request.method == "POST":
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        pincode = request.POST.get("pincode")
        cart = request.session.get("cart")
        uid = request.session.get("_auth_user_id")
        user = User.objects.get(pk=uid)

        for i in cart:
            a = int(cart[i]['price'])
            b = cart[i]['quantity']
            total = a * b

            order = Order1(
                user = user,
                product = cart[i]['name'],
                price = cart[i]['price'],
                quantity = cart[i]['quantity'],
                image = cart[i]['image'],
                address = address,
                phone = phone,
                pincode = pincode,
                total = total,
            )
            order.save()
        request.session['cart'] = {}
        return redirect('index')

    return HttpResponse("this is checkout page")


def your_order(request):
    uid = request.session.get("_auth_user_id")
    user = User.objects.get(pk=uid)

    order = Order1.objects.filter( user = user)
    context = {
        'order' : order,
    }
    return render(request,'order.html',context)


def Product_page(request):
    category = Category.objects.all()
    categoryID = request.GET.get('category')

    brand = Brand.objects.all()
    brandID = request.GET.get('brand')

    if categoryID:  # jar category id bhetla tr tya id chya related jevdhe products ahet tevdhe display honar
        product = Product.objects.filter(sub_category=categoryID).order_by('-id')  # order by -id he je item recently (saglayt shevti ) add kelet te display honyasathi
    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')
    else:
        product = Product.objects.all()  # jar tyala catgory id nahi bhetla tr all products display honar

    context = {
        'category':category,
        'brand':brand,
        'product':product,
    }
    return render(request,'product.html',context)


def Product_detail(request,id):
    category = Category.objects.all()
    categoryID = request.GET.get('category')

    brand = Brand.objects.all()
    brandID = request.GET.get('brand')

    product_detail = Product.objects.filter(id=id).first()
    related_product = Product.objects.filter(category = product_detail.category).exclude(id=id)[:4]

    if categoryID:  # jar category id bhetla tr tya id chya related jevdhe products ahet tevdhe display honar
        product = Product.objects.filter(sub_category=categoryID).order_by('-id')  # order by -id he je item recently (saglayt shevti ) add kelet te display honyasathi
    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')
    else:
        product = Product.objects.all()  # jar tyala catgory id nahi bhetla tr all products display honar

    context = {
        'category': category,
        'brand': brand,
        'product': product,
        'prod':product_detail,
        'related':related_product,
    }
    return render(request, 'product_detail.html', context)


def Search(request):
    query = request.GET['query']
    product = Product.objects.filter(name__icontains = query)

    context = {
        'product':product,
    }
    return render(request,'search.html',context)

def Account(request):
    return render(request,'account.html')

def info(request):
    category = Category.objects.all()
    categoryID = request.GET.get('category')

    brand = Brand.objects.all()
    brandID = request.GET.get('brand')

    if categoryID:  # jar category id bhetla tr tya id chya related jevdhe products ahet tevdhe display honar
        product = Product.objects.filter(sub_category=categoryID).order_by('-id')  # order by -id he je item recently (saglayt shevti ) add kelet te display honyasathi
    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')
    else:
        product = Product.objects.all()  # jar tyala catgory id nahi bhetla tr all products display honar

    context = {
        'category':category,
        'brand':brand,
        'product':product,
    }
    return render(request,'info.html',context)
