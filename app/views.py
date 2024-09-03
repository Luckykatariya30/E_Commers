from django.shortcuts import render,redirect
from django.views import  View
from .models import Cart,Product,OrderPlaced,Customer
from .forms import CustomerRegistraionForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
 def get(self,request):
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')
  laptops = Product.objects.filter(category='L')
  return render(request , 'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles ,'laptops':laptops})


class ProductDetailView(View):
 def get(self,request,pk):
  product = Product.objects.get(pk=pk)
  item_already =False
  if request.user.is_authenticated:
   item_already = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render(request, 'app/productdetail.html' , {'product':product,'item_already_in_cart':item_already})

@login_required
def add_to_cart(request):
 
 user = request.user
 product_id = request.GET.get('prod_id')
 print(product_id)
 product = Product.objects.get(id=product_id)
 if Cart.objects.filter(Q(product=product_id) & Q(user=user)).exists():
  c = Cart.objects.get(Q(product=product_id) & Q(user=user))
  c.quantity += 1
  c.save()
 else:
  cart = Cart(user=user , product=product)
  cart.save()
  cart = Cart.objects.filter(user=user) 
 return redirect('/cart') 

# def show_cart(request): 
#  return render(request , 'app/addtocart.html')
@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  cart = Cart.objects.filter(user=user)
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  if cart_product:
   amount = 0.0
   shipping_amount = 30.0
   total_amount = 0.0
   for p in cart_product:
    temp_amount =(p.quantity * p.product.discounted_price)
    amount += temp_amount
    total_amount = amount + shipping_amount
    
   return render(request, 'app/addtocart.html' , {'carts':cart,'amount':amount,'total':total_amount,'shipping':shipping_amount})
  else:
   return render(request , 'app/emptycart.html')
  
@login_required
def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  print(prod_id)
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity += 1
  c.save()
  user = request.user
  amount = 0.0
  shipping_amount = 30.0
  total_amount = 0.0
  cart_product = Cart.objects.filter(user=user)
  if cart_product:
   for p in cart_product:
    temp_amount =(p.quantity * p.product.discounted_price)
    amount += temp_amount
   total_amount = amount +shipping_amount
   data ={
     'quantity':c.quantity,
     'amount': amount,
     'shipping':shipping_amount,
     'total':total_amount
    }
   return JsonResponse(data)
@login_required
def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  print(prod_id)
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity -= 1
  c.save()
  user = request.user
  amount = 0.0
  shipping_amount = 30.0
  total_amount = 0.0
  cart_product = Cart.objects.filter(user=user)
  if cart_product:
   for p in cart_product:
    temp_amount =(p.quantity * p.product.discounted_price)
    amount += temp_amount
   total_amount = amount +shipping_amount
   data ={
     'quantity':c.quantity,
     'amount': amount,
     'shipping':shipping_amount,
     'total':total_amount
    }
   return JsonResponse(data)
  
@login_required
def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  print(prod_id)
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.delete()
  user = request.user
  amount = 0.0
  shipping_amount = 30.0
  total_amount = 0.0
  cart_product = Cart.objects.filter(user=user)
  if cart_product:
   for p in cart_product:
    temp_amount =(p.quantity * p.product.discounted_price)
    amount += temp_amount
   total_amount = amount +shipping_amount
   data ={
     'amount': amount,
     'shipping':shipping_amount,
     'total':total_amount
    }
   return JsonResponse(data)

@login_required
def buy_now(request):
 return redirect('/checkout')

def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add , 'active':'btn-primary'} )

@login_required
def orders(request):
 order = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'order_placed':order})

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request , data = None):
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data=='vivo'or data=='xieomi'or data=='oneplus'or data=='oppo':
  mobiles = Product.objects.filter(category='M').filter(brand = data)
 elif data == 'below':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=18000)

 elif data == 'above':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=18000)
 return render(request, 'app/mobile.html',{'mobiles':mobiles})

def laptop(request, data=None):
 if data == None:
  laptop = Product.objects.filter(category='L')
 elif data=='mac'or data=='hp'or data=='dell'or data=='leenova':
  laptop = Product.objects.filter(category='L').filter(brand = data)
 elif data == 'below':
  laptop = Product.objects.filter(category='L').filter(discounted_price__lt=50000)
 elif data == 'above':
  laptop = Product.objects.filter(category='L').filter(discounted_price__gt=50000)
 return render(request, 'app/laptop.html',{'laptops':laptop})
 
def topwear(request , data = None):
 if data == None:
  topwear = Product.objects.filter(category='TW')
 elif data=='lie'or data=='livace'or data=='adidas':
  topwear = Product.objects.filter(category='TW').filter(brand = data)
 elif data == 'below':
  topwear = Product.objects.filter(category='TW').filter(discounted_price__lt=250)
 elif data == 'above':
  topwear = Product.objects.filter(category='TW').filter(discounted_price__gt=250)
 return render(request, 'app/topwears.html',{'topwears':topwear}) 

def bottomwear(request , data = None):
 if data == None:
  bottomwear = Product.objects.filter(category='BW')
 elif data=='lie'or data=="livies":
  bottomwear = Product.objects.filter(category='BW').filter(brand = data)
 elif data == 'below':
  bottomwear = Product.objects.filter(category='BW').filter(discounted_price__lt=400)
 elif data == 'above':
  bottomwear = Product.objects.filter(category='BW').filter(discounted_price__gt=400)
 return render(request, 'app/bottomwears.html',{'bottomwears':bottomwear}) 



class CustomerRegistrationView(View):
 def get(self,request):
  form =CustomerRegistraionForm()
  return render(request ,'app/customerregistration.html', {'form':form})
 
 def post(self,request):
  form =CustomerRegistraionForm(request.POST)
  if form.is_valid():
   messages.success(request,'Congratulations! Registered Successfully ')
   form.save()
  return redirect('/registration')


# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
@login_required
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 product_id = request.GET.get("prod_id")
 cart_item = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 30.0
 total_amount = 0.0
 
 if cart_item:
  for p in cart_item:
   temp_amount =(p.quantity * p.product.discounted_price)
   amount += temp_amount
 total_amount = amount +shipping_amount

 return render(request, 'app/checkout.html',locals())
@login_required
def payment_done(request):
 user = request.user
 cart = Cart.objects.filter(user=user)
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id=custid)
 if cart:
  for c in cart:
   order = OrderPlaced(user=user , customer=customer , product = c.product , quantity = c.quantity)
   order.save()
   c.delete()
  return redirect('/orders')
 

#{'add': add,'cart_items':cart_item,'total_amount':total_amount}

# def profile(request):
#  return render(request, 'app/profile.html')
@method_decorator(login_required , name='dispatch')
class ProfileView(View):
 def get(self,request):
  form = CustomerProfileForm()
  return render(request ,'app/profile.html',{'forms':form})

 def post(self,request):
  forms =CustomerProfileForm(request.POST)
  if forms.is_valid():
   usr = request.user
   name = forms.cleaned_data['name']
   locality = forms.cleaned_data['locality']
   city = forms.cleaned_data['city']
   state = forms.cleaned_data['state']
   zipcode = forms.cleaned_data['zipcode']
   reg = Customer(user=usr, name=name ,locality=locality ,city=city, state=state ,zipcode=zipcode)
   reg.save()
   messages.success(request,'Congratulations! Created Profile Successfully ')
  return redirect('/profile')
