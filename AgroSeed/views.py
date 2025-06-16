from django.shortcuts import render,redirect 
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import Product, Cart, Address,Order,Profile
from django.db.models import Q
from django.db import IntegrityError
from django.core.mail import send_mail
import re
import random
import razorpay
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.forms import SetPasswordForm  
from django.contrib import messages 

# Create your views here.



def home(request):
   # context={}
    #products=product.objects.all()
    #context["products"]=products
   # l=[i for i in range(1,11)]
   #context['list']=l  #list comprehension is way of creationg a list from any iterable object.    range(), list
    return render(request, 'home.html')


def register(request):
    context={}
    try:
     if request.method=="POST":
        un=request.POST["uname"]
        em=request.POST["uemail"]
        p=request.POST["upass"]
        cp=request.POST["ucpass"]
        print(un,em,p,cp)
        if un=="" or em=="" or p=="" or cp=="":
            context["error"]="fields cannot be empty!"
            return render(request,'register.html',context)
        elif p!=cp:
            context["error"]="Please check the password again!"
            return render(request,"register.html",context)
        elif len(p)<8:
            context["error"]="Password must contain atleast 8 charachter"
            return render(request,"register.html",context)
        else:
            u=User.objects.create_user(username=un,email=em,password=p)
            u.save()
            #return redirect ("/login")
            context["msg"]="User created successfully, Please login now !"
            return render(request,"register.html",context)
     else:
            return render(request,'register.html')
     
    except IntegrityError:
        context["error"]="user already exist!, Please enter another username"
        return render(request,'register.html', context)
    

def ulogin(request):
    context={}
    if request.method=="POST":
        un=request.POST["uname"]
        p=request.POST["upass"]
        print(un,p)
        if un=="" or p=="":
            context["error"]="All fields are required"
            return render (request,'login.html',context)
        else:
            u=authenticate(username=un,password=p)
            print(u)
            if u is not None:
                 # print(u)
                 login(request,u)
                 return redirect('/')
            else:
                 context["error"]="username or password is invalid"
                 return render(request,"login.html",context)
                 return HttpResponse("Data Fetched...!")
    return render(request, 'login.html')

def ulogout(request):
    logout(request)
    return redirect("/")



def productdetails(request,pid):
    context={}
    prod=Product.objects.get(id=int(pid))
    context["product"]=prod
    return render(request,'productsdetail.html',context)


def products(request):
    print(request.user.is_authenticated)
    context={}
    products=Product.objects.all()
    context["products"]=products
    return render(request,"products.html",context)

def filterbycategory(request,cat):
    context={}
    print(cat)
    products=Product.objects.filter(category=cat)
    context["products"]=products
    return render(request,'products.html',context)

def sortbyprice(request,x):
    context={}
    if x=="1":
        products=Product.objects.order_by("-price").all()
    else:
        products=Product.objects.order_by("price").all() #asc order low to high
    context["products"]=products
    return render(request,'products.html',context)


def filterbyprice(request):
    context={}
    try:
        mn=request.GET["min"]
        mx=request.GET["max"]
        q1=Q(price__gte=mn)
        q2=Q(price__lte=mx)
        products=Product.objects.filter(q1&q2)
        context["products"]=products
        return render(request,"products.html",context)

    except ValueError:
     products=Product.objects.all()
     context["error"]="please enter minimum and maximum value"
     context["products"]=products
     return render(request,"products.html",context)


def addtocart(request,pid):
    context={}
    prod=Product.objects.get(id=int(pid))
    context["product"]=prod
    if request.user.is_authenticated:
        u=User.objects.get(id=request.user.id)
        p=Product.objects.get(id=int(pid))
        print(u.username)
        q1=Q(userid=u.id)
        q2=Q(pid=p.id)
        cart=Cart.objects.filter(q1&q2)
        if len(cart)==1:
            context["msg"]="Product Already ADDED to your cart"
            return render(request,"productsdetail.html",context)
        else:
           cart=Cart.objects.create(userid=u,pid=p)
           cart.save()
           context["success"]="Product ADDED to your cart successfully!"
        return render(request,"productsdetail.html",context)
         
        return render(request,"productsdetail.html",context)
    
    else:
        return redirect("/login")
       
    return render(request,"productsdetail.html",context)


def viewcart(request):
    context={}
    total=0
    items=0
    u=User.objects.get(id=request.user.id)
    carts=Cart.objects.filter(userid=u)
    for c in carts:
        items+=c.qty
        total+=c.pid.price * c.qty
    print(total)
    context["total"]=total
    context["carts"]=carts
    context["items"]=items
    return render(request,"cart.html",context)

def updateqty(request,x,cid):
    context={}
    cart=Cart.objects.get(id=int(cid))
    if x=="1":
        cart.qty+=1 and cart.qty<=10
        cart.save()
       
    elif cart.qty>1:
         cart.qty-=1
         
         cart.save()
    return redirect("/viewcart")


def removecart(request,cid):
     cart=Cart.objects.get(id=int(cid))
     cart.delete()
     return redirect("/viewcart")


def checkaddress(request):
    context={}
    u=User.objects.get(id=request.user.id)
    add=Address.objects.filter(user_id=u)
    print(len(add))
    if len(add)>=1:
        return redirect("/placeorder")

    else:

       if request.method=="POST":
        fn=request.POST["fname"]
        ad=request.POST["address"]
        ct=request.POST["city"]
        st=request.POST["state"]
        zp=request.POST["zipcode"]
        mob=request.POST["mobile"]
        print(re.match("[6-9]\d{9}",mob))
        if fn=="" or ad=="" or ct=="" or st=="" or zp=="" or mob=="":
            context["error"]="Fields cannot be empty!"
            return render(request,'address.html',context)
        elif not fn.isalpha():
            context["ferror"]="Only letters are allowed for Full name"
            return render(request,"address.html",context)

        elif not ct.isalpha():
            context["cerror"]="Please enter valid City !"
            return render(request,"address.html",context)
        
        elif not st.isalpha():
            context["serror"]="Please enter valid State !"
            return render(request,"address.html",context)
    
        elif  not len(zp)==6 and not zp.isdigit():
            context["error"]="Please enter valid zip code!"
            return render(request,'address.html',context)
        
        elif not re.match("[6-9]\d{9}",mob):
            context["error"]="Please enter valid Mobile Number!"
            return render(request,'address.html',context)
        
        else:
           addr=Address.objects.create(user_id=u,fullname=fn,address=ad,city=ct,state=st,pincode=zp,mobile=mob)
           addr.save()
           return redirect("/placeorder")
       else:
        return render(request,"address.html",context)

def placeorder(request):
    context={}
    u=User.objects.get(id=request.user.id)
    carts=Cart.objects.filter(userid=u)
    for c in carts:
        oid=random.randint(1000,9999)
        order=Order.objects.create(order_id=oid,user_id=u,p_id=c.pid,amt=c.pid.price*c.qty,qty=c.qty)
        order.save()
        return redirect("/fetchorder")
    

def fetchorder(request):
    context={}
    u=User.objects.get(id=request.user.id)
    address=Address.objects.get(user_id=u)
    context["address"]=address
   
    items=0
    total=0
    
    
    q1=Q(user_id=u)
    q2=Q(payment_status="unpaid")
    orders=Order.objects.filter(q1&q2)
    for order in orders:
        items+=order.qty
        total+=order.amt
    context["orders"]=orders
    context["items"]=items
    context["total"]=total
    return render(request,"fetchorder.html",context)


def makepayment(request):
    context={}
    u=User.objects.get(id=request.user.id)
    address=Address.objects.get(user_id=u)
    context["address"]=address
    total=0
    q1=Q(user_id=u)
    q2=Q(payment_status="unpaid")
    orders=Order.objects.filter(q1&q2)
    for order in orders:
        total+=order.amt
    context["orders"]=orders
    context["total"]=total
    client = razorpay.Client(auth=("rzp_test_6wZ986hRbPrnoS", "56gj07Rf6EL4i8Olc3Z1UyLn"))
    data = { "amount": total*100, "currency": "INR", "receipt":"1111" }
    payment = client.order.create(data=data)
    context["payment"]=payment
    print(context["payment"])
    return render(request,"pay.html",context) 

def mail_send(request):
    user=User.objects.get(id=request.user.id)
    send_mail(
    "order confirmation mail",
    "Dear customer, \n your order is confirmed and will delivered in 3 working days",
    "himanishinde2003@gmail.com",
    [user.email],
    fail_silently=False,
)
    return redirect("/change_status")

def change_status(request):
    u=User.objects.get(id=request.user.id)
    context={}
    q1=Q(user_id=u)
    q2=Q(payment_status="unpaid")
    orders=Order.objects.filter(q1&q2)
    orders.update(payment_status="paid")
    return redirect("/")


def myorders(request):
    u=User.objects.get(id=request.user.id)
    context={}
    total=0
    q1=Q(user_id=u)
    q2=Q(payment_status="paid")
    orders=Order.objects.filter(q1&q2)
    context["orders"]=orders
    return render(request,"order.html",context)



def about_section(request):
    return render(request,"about.html")


@login_required
def upload_profile_image(request):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        # Get or create the user's profile
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        profile.image = request.FILES['profile_image']
        profile.save()
        
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def edit_address(request):
    user = request.user
    try:
        address = Address.objects.get(user_id=user.id)  # Use user directly if ForeignKey
    except Address.DoesNotExist:
        address = None

    if request.method == 'POST':
        fname = request.POST.get('fname')
        addr = request.POST.get('address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        zipcode = request.POST.get('zipcode')
        mobile = request.POST.get('mobile')

        # Validate all fields
        if not fname or not addr or not state or not city or not zipcode or not mobile:
            messages.error(request, "Please fill all the fields")
            return render(request, 'address.html', {'initial': request.POST})

        # Validate Zipcode: 5 or 6 digits, not all 0s
        if not re.fullmatch(r'^(?!0+$)\d{5,6}$', zipcode):
            messages.error(request, "Please enter valid zipcode")
            return render(request, 'address.html', {'initial': request.POST})

        # Validate Mobile number: exactly 10 digits
        if not re.fullmatch(r'^\d{10}$', mobile):
          messages.error(request, "Please enter valid number")
          return render(request, 'address.html', {'initial': request.POST})

        # Save or update address
        if address:
            address.fullname = fname
            address.address = addr
            address.state = state
            address.city = city
            address.pincode = zipcode
            address.mobile = mobile
            address.save()
        else:
            Address.objects.create(
                user=user,
                fullname=fname,
                address=addr,
                state=state,
                city=city,
                pincode=zipcode,
                mobile=mobile
            )

        return redirect('/fetchorder')

    else:
        initial = {
            'fname': address.fullname if address else '',
            'address': address.address if address else '',
            'state': address.state if address else '',
            'city': address.city if address else '',
            'zipcode': address.pincode if address else '',
            'mobile': address.mobile if address else '',
        }
        return render(request, 'address.html', {'initial': initial})

