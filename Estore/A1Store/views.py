from django.shortcuts import render,redirect,HttpResponseRedirect
from .forms import SignUpForm ,User
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from .models import Product,Category
from .models import order
from django.views import View
class Index(View):
    def post(self,request):
        if request.user.is_authenticated:
                product=request.POST.get('product')
                remove=request.POST.get('remove')
                cart=request.session.get('cart')
                if cart:
                    quantity=cart.get(product)
                    if quantity:
                        if remove:
                            if quantity<=1:
                                cart.pop(product)
                            else:
                                cart[product]=quantity-1
                        else:
                            cart[product]=quantity+1
                    else:
                        cart[product]=1
                else:
                    cart={}
                    cart[product]=1
                request.session['cart']=cart
                print('cart',request.session['cart'])
                return redirect('/menu/')
        return HttpResponseRedirect('/login/')


    def get(self,request):
        cart=request.session.get('cart')
        if not cart:
            request.session['cart']={}
        products=Product.get_all_product();

        data={}
        data['products']=products
        print('you are', request.session.get('user_id'))

        return render(request,'menu.html',data)



def F1(request):
    return render(request,'main.html')

def F3(request):
    return render(request,'about.html')
def F4(request):
    return render(request,'service.html')

def sign_up(request):
    if request.method=="POST":
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            fm.save()
    else:
       fm=SignUpForm()
    return render(request,'signup.html',{'form':fm})

def user_login(request):
    # if not request.user.is_authenticated:
        if request.method=="POST":
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upass=fm.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    request.session['user_id'] = user.id
                    return HttpResponseRedirect('/menu/')
        else:
            fm=AuthenticationForm()
            # print('you are', request.session.get('user_id'))

        return render(request,'login.html',{'form':fm})
    # else:
    #     return HttpResponseRedirect('/login/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
class Cart(View):
    def get(self,request):
        ids=list(request.session.get('cart').keys())
        product=Product.get_products_by_id(ids)
        print(product)
        return render(request,'cart.html',{'products':product})


class Checkout(View):
    def post(self,request):
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        user=request.session.get('user_id')
        cart=request.session.get('cart')
        products=Product.get_products_by_id(list(cart.keys()))
        print(address,phone, user,cart,products)

        for product in products:
            print(cart.get(str(product.id)))
            Order=order(user=User(id=user),product=product,price=product.price,address=address,phone=phone,quantity=cart.get(str(product.id)))
            Order.placeOrder();
        request.session['cart']={}


        return redirect('cart')

class History(View):
    def get(self,request):
        user=request.session.get('user_id')
        history=order.get_orders_history_by_user(user)
        print(history)
        return render(request,'history.html',{'historys':history})



