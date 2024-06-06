from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import CustomUserCreationForm,ProductForm,MessageForm
from .models import CustomUser, Product, Message,Transaction,Category
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


def index(request):
    search_query=request.GET.get('search','')
    context={
        "products":Product.objects.all().order_by('-created_at'),
        "ordinateur":Product.objects.filter(category=1),
        "telephone":Product.objects.filter(category=2),
        "vetement":Product.objects.filter(category=3),
        
    }
    if search_query:
        prod_search=Product.objects.filter(title__icontains=search_query)
        context["prod_search"]=prod_search
    
    return render(request,"appli1/index.html",context)



def logout_view(request):
    logout(request)
    return redirect('logged_out')




def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return HttpResponse("Invalid credentials")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {"form": form})


@login_required
def dashboard_view(request):
    user = request.user
    products = Product.objects.filter(seller=user)
    messages_sent = Message.objects.filter(sender=user)
    messages_received = Message.objects.filter(recipient=user).order_by('-timestamp')
    transactions = Transaction.objects.filter(seller=user) | Transaction.objects.filter(buyer=user)

    # Initialisation des formulaires par défaut
    product_form = ProductForm()
    message_form = MessageForm(user=user)
    
    if request.method == 'POST':
        if 'post_product' in request.POST:
            product_form = ProductForm(request.POST, request.FILES)
            if product_form.is_valid():
                product = product_form.save(commit=False)
                product.seller = user
                product.save()
                return redirect('dashboard')
        elif 'send_message' in request.POST:
            message_form = MessageForm(request.POST,user=user)
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.sender = user
                message.save()
                return redirect('dashboard')
        
        elif 'achete_produit' in request.POST:
            product_id=request.POST.get('product_id')
            product=get_object_or_404(Product,id=product_id)
            content=f"je veux en savoir plus sur ce produit pour acheter: {product.title}"
            Message.objects.create(sender=user,recipient=product.seller,content=content)
            
            return redirect('dashboard')

    context = {
        'products': products,
        'messages_sent': messages_sent,
        'messages_received': messages_received,
        'transactions': transactions,
        'product_form': product_form,
        'message_form': message_form,
        "prod":Product.objects.all().order_by('-created_at')
    }
    return render(request, 'appli1/dashboard.html', context)


def delete_product_view(request,product_id):
    product=get_object_or_404(Product,id=product_id,seller=request.user)
    if request.method=='POST':
        product.delete()
        messages.success(request,'Produit supprimé avec succes')
        return redirect('dashboard')

    return render(request,'appli1/dashboard.html')

def delete_message_view(request,message_id):
    message=get_object_or_404(Message,id=message_id,recipient=request.user)
    if request.method=='POST':
        message.delete()
        messages.success(request,'Message supprimé avec succes')
        return redirect('dashboard')

    return render(request,'appli1/dashboard.html')
