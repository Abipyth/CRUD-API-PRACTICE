from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import *
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt
def reg(request):
    if request.method=="POST":
        un=request.POST.get("username")
        pw1=request.POST.get("password1")
        pw2=request.POST.get("password2")
        email=request.POST.get("email")
        fn=request.POST.get("first_name")
        ln=request.POST.get("last_name")
        role=request.POST.get("role")

        user=User.objects.create_user(username=un, password=pw1, email=email, first_name=fn, last_name=ln)

        if pw1!=pw2:
            return HttpResponse("password doesnt match")
        
        #if User.objects.filter(username=un).exists():
            #return HttpResponse("user already exists")
        
        if role=="Admin":
            admin_group, created= Group.objects.get_or_create(name="Admin")
            user.groups.add(admin_group)

        elif role=="Store Keeper":
            storekeeper_group, created= Group.objects.get_or_create(name="Store Keeper")
            user.groups.add(storekeeper_group)
        else:
            customer_group, created= Group.objects.get_or_create(name="Customer")
            user.groups.add(customer_group)

        user.save()
        return HttpResponse("users created successfully")
        
    return render(request,"reg.html")


@csrf_exempt
def log(request):
    form=AuthenticationForm()
    if request.method=="POST":
        form=AuthenticationForm(request,request.POST)
        
        if form . is_valid():
            un=form.cleaned_data.get("username")
            pw=form.cleaned_data.get("password")
            user=authenticate(request, username=un, password=pw)

            if form is not None:
                login(request,user)
                return HttpResponse("loged in success")

    return render(request,"log.html", context={"form":form})

@login_required
@csrf_exempt
def lout(request):
    logout(request)
    return redirect ("log")

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_storekeeper(user):
    return user.groups.filter(name='Store Keeper').exists()

def is_customer(user):
    return user.groups.filter(name='Customer').exists()

@login_required
@user_passes_test(lambda u: is_admin(u) or is_storekeeper(u))
@csrf_exempt
def add(request):
    if request.method=="POST":
        name=request.POST.get("name")
        desc=request.POST.get("desc")

        data=Product.objects.create(name=name, desc=desc)
        data.save()
        return HttpResponse("product added successfully")
    return render(request, "add.html")

@login_required
@csrf_exempt
def pview(request):
    data=Product.objects.all()
    return render(request,"pview.html", context={"data":data})
@login_required
@user_passes_test(lambda u: is_admin(u) or is_storekeeper(u))
@csrf_exempt
def update(request,id):
    data=Product.objects.get(id=id)

    if request.method=="POST":
        name=request.POST.get("name")
        desc=request.POST.get("desc")

        data.name=name
        data.desc=desc
        data.save()

        return HttpResponse("updated successfully")

    return render(request,"update.html", context={"data":data})
@login_required
@user_passes_test(is_admin)
@csrf_exempt
def delete(request,id):
    data=Product.objects.get(id=id)
    data.delete()
    return HttpResponse("deleted successfully")
    
def pview_json(request,id):
    if not request.user.is_authenticated :
        return JsonResponse({"error":"user is not authenticated"},status=401)
    
    pids=request.GET.getlist('ids')
    name_query=request.GET.get("name", " ")

    if pids==True :
        products=Product.objects.filter(id__in=pids)
        product_list=  [{"id":product.id , "name": product.name, "desc":product.desc } for product in products ]

    elif name_query ==True :
        products=Product.objects.filter(name__icontains=name_query)
        product_list=  [{"id":product.id , "name": product.name, "desc":product.desc } for product in products ]
    else:
        products=Product.objects.get(id=id)
        product_list=  [{"id":products.id , "name": products.name, "desc":products.desc }  ]
    #print(type(product_list))
    return JsonResponse(product_list,safe=False)

def pview_json1(request,name):     ######################  this function uses the HTTP GET method
    if not request.user.is_authenticated :
        return JsonResponse({"error":"user is not authenticated"},status=401)
    
    pids=request.GET.getlist('ids')
    name_query=request.GET.get("name", " ")

    try:

        if pids==True:
            products=Product.objects.filter(id__in=pids)
            product_list=  [{"id":product.id , "name": product.name, "desc":product.desc } for product in products ]

        elif name_query ==True :
            products=Product.objects.filter(name__icontains=name_query)
            product_list=  [{"id":product.id , "name": product.name, "desc":product.desc } for product in products ]
        else:
            products=Product.objects.get(name=name)
            product_list=  [{"id":products.id , "name": products.name, "desc":products.desc }  ]
        #print(type(product_list))
        return JsonResponse(product_list,safe=False)
    except Exception as e:
        return JsonResponse({"error":str(e)})

@login_required
def pview_html(request, id=None):
    if not request.user.is_authenticated:
        return HttpResponse("User is not authenticated", status=401)
    
    # Get list of product IDs and name query from GET parameters
    pids = request.GET.getlist('ids')
    name_query = request.GET.get("name", "")

    # If product IDs are provided, filter by these IDs
    if pids:
        products = Product.objects.filter(id__in=pids)
    # If a name query is provided, filter products containing the name query
    elif name_query:
        products = Product.objects.filter(name__icontains=name_query)
    else:
        # If neither IDs nor name query is provided
        if id:
            # If an ID is provided in the URL, filter by this ID
            products = Product.objects.filter(id=id)
        else:
            # If no ID is provided, get all products
            products = Product.objects.all()

    # Render the products in the template
    return render(request, "product_view.html", {"products": products})
@csrf_exempt
@require_http_methods(["POST"])
def add_product_json(request):
    try:                                            ####### handling errors
        data=json.loads(request.body)
        product=Product.objects.create(
            name=data["name"],
            desc=data["desc"]
              )
        return JsonResponse({"id":product.id, "name":product.name, "desc":product.desc},status=201)   ### 201 status code for create a data

    except Exception as e:
        return JsonResponse({"error":str(e)},status=400 )
@csrf_exempt
@require_http_methods(["GET"])
def view_product_json(request):
    try:
        products=Product.objects.all().values()
        return JsonResponse(list(products), status=200, safe=False)

    except Exception as e:
        return JsonResponse({"error":str(e)},status=400 )
@csrf_exempt
@require_http_methods(["PUT"])
def update_product_json(request,id):
    try:
        data=json.loads(request.body)
        product=Product.objects.get(id=id)
        product.name=data.get("name")
        product.desc=data.get("desc")
        product.save()
        return JsonResponse({"id":product.id, "name":product.name, "desc":product.desc},status=201)

    except product.DoesNotExist:
        return JsonResponse({"error":"product not found"},status=404 )
    
    except Exception as e:
        return JsonResponse({"error":str(e)},status=400 )
    
@csrf_exempt
@require_http_methods(["PATCH"])
def part_update_product_json(request,id):
    try:
        data=json.loads(request.body)
        product=Product.objects.get(id=id)
        if "name" in data:
            product.name=data.get("name")
        if "desc" in data:
            product.desc=data.get("desc")
        product.save()
        return JsonResponse({"id":product.id, "name":product.name, "desc":product.desc},status=201)

    except product.DoesNotExist:
        return JsonResponse({"error":"product not found"},status=404 )
    
    except Exception as e:
        return JsonResponse({"error":str(e)},status=400 )
    

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_product_json(request,id):
    try:
        product=Product.objects.get(id=id)
        product.delete()
        return JsonResponse({"success":"product deleted successfully"})
    
    except Exception as e:
        return JsonResponse({"error":str(e)},status=400 )

        


