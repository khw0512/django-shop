from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer
from django.shortcuts import render, get_object_or_404, redirect
from .models import Stuff, Cart, Order, PostImage
from .forms import StuffForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from ckeditor_uploader.fields import RichTextUploadingField


# Create your views here.


def index(request):
    stuffs = Stuff.objects.all()
    context = {'stuffs': stuffs}
    return render(request, 'mall/index.html', context)


def detail(request, stuff_id):
    stuff = Stuff.objects.get(id=stuff_id)
    images = PostImage.objects.filter(stuff=stuff_id)
    context = {'stuff': stuff, 'images': images}
    return render(request, 'mall/detail.html', context)


def register(request):
    if request.method == "POST":
        stuff = Stuff(name=request.POST.get('name'), price=request.POST.get(
            'price'), detail=request.POST.get('detail'), image=request.FILES.get('image'))
        stuff.pub_date = timezone.now()+timedelta(hours=9)
        stuff.save()
        return redirect('mall:index')
    else:
        form = StuffForm()
        return render(request, 'mall/register.html', {'form': form})


@login_required(login_url='common:login')
def info(request):
    orders = Order.objects.filter(
        user=request.user).order_by('-order_date')
    pub_times = []
    orderlists = []
    for order in orders:
        pub_times.append(order.order_date)
    pub_times = list(set(pub_times))
    for pub_time in pub_times:
        total = 0
        orders = Order.objects.filter(order_date=pub_time)
        for order in orders:
            total += order.subtotal
        orderlists.append([orders, total])
    context = {'orderlists': orderlists,
               'username': request.user.username, 'email': request.user.email}
    return render(request, 'mall/info.html', context)


@login_required(login_url='common:login')
def cart(request):
    uCart = Cart.objects.filter(user=request.user)
    stuffs = uCart
    context = {'stuffs': stuffs}
    return render(request, 'mall/cart.html', context)


@login_required(login_url='common:login')
def addCart(request, stuff_id):
    uCart = Cart.objects.filter(user=request.user)
    stuff = Stuff.objects.get(id=stuff_id)
    for uCart2 in uCart:
        if uCart2.stuffs.id == stuff_id:
            uCart2.quantity += 1
            uCart2.save()
            break
    else:
        uCart2 = Cart.objects.create(user=request.user, stuffs=stuff)
        uCart2.quantity += 1
        uCart2.save()

    return redirect('mall:cart')


@login_required(login_url='common:login')
def subCart(request, stuff_id):
    uCart = Cart.objects.filter(user=request.user)
    for uCart2 in uCart:
        if uCart2.stuffs.id == stuff_id:
            uCart2.delete()
            break
    return redirect('mall:cart')


@login_required(login_url='common:login')
def plusStuff(request, stuff_id):
    uCart = Cart.objects.filter(user=request.user)
    for uCart2 in uCart:
        if uCart2.stuffs.id == stuff_id:
            uCart2.quantity += 1
            uCart2.save()
            break
    return redirect('mall:cart')


@login_required(login_url='common:login')
def minusStuff(request, stuff_id):
    uCart = Cart.objects.filter(user=request.user)
    for uCart2 in uCart:
        if uCart2.stuffs.id == stuff_id:
            uCart2.quantity -= 1
            uCart2.save()
            if uCart2.quantity == 0:
                uCart2.delete()
            break
    return redirect('mall:cart')


@login_required(login_url='common:login')
def buyAtIndex(request, stuff_id):
    uCart = Cart.objects.filter(user=request.user)
    stuff = Stuff.objects.get(id=stuff_id)
    for uCart2 in uCart:
        if uCart2.stuffs.id == stuff_id:
            uCart2.quantity += 1
            uCart2.save()
            break
    else:
        uCart2 = Cart.objects.create(user=request.user, stuffs=stuff)
        uCart2.quantity += 1
        uCart2.save()
    return redirect('mall:cart')


@login_required(login_url='common:login')
def buy(request):
    subtotal = 0
    order_date = datetime.now()
    if request.method == 'POST':
        uCarts = Cart.objects.filter(user=request.user)
        for uCart in uCarts:
            if request.POST.get(uCart.stuffs.name):
                stuff_name = request.POST[uCart.stuffs.name]
                stuff = Stuff.objects.get(name=stuff_name)
                uCart = Cart.objects.get(user=request.user, stuffs=stuff)
                orderlist = Order.objects.create(
                    user=request.user, stuff=uCart.stuffs, order_date=order_date, quantity=uCart.quantity)
                orderlist.save()
                subtotal = uCart.quantity*uCart.stuffs.price
                orderlist.subtotal = subtotal
                orderlist.save()

        orders = Order.objects.filter(user=request.user)
        pub_times = []
        orderlists = []
        for order in orders:
            pub_times.append(order.order_date)
        pub_times = list(set(pub_times))
        for pub_time in pub_times:
            orders = Order.objects.filter(order_date=pub_time)
            total = 0
            for order in orders:
                total += order.subtotal
            orderlists.append([orders, total])
        context = {'orderlists': orderlists,
                   'username': request.user.username, 'email': request.user.email}
    else:
        context = {'username': request.user.username,
                   'email': request.user.email}
    return render(request, 'mall/info.html', context)


@login_required(login_url='common:login')
def delpage(request):
    stuffs = Stuff.objects.all()
    context = {'stuffs': stuffs}
    return render(request, 'mall/delpage.html', context)


@login_required(login_url='common:login')
def delstuff(request, stuff_id):
    stuff = Stuff.objects.get(id=stuff_id)
    stuff.delete()
    return redirect('mall:delpage')


@login_required(login_url='common:login')
def edit(request):
    return render(request, 'mall/editpage.html')


@login_required(login_url='common:login')
def update(request, stuff_id):
    stuff = get_object_or_404(Stuff, id=stuff_id)
    files = request.FILES
    form = StuffForm(request.POST, request.FILES, instance=stuff)
    if request.method == "POST":
        if form.is_valid():
            stuff = form.save(commit=False)
            stuff.save()
            return redirect('mall:detail', stuff_id=stuff.pk)
        else:
            return redirect('mall:index')
    else:
        form = StuffForm(instance=stuff)
        return render(request, 'mall/editpage.html', {'form': form})


@login_required(login_url='common:login')
def test(request):
    return render(request, 'mall/test.html')


def joolmain(request):
    return render(request, 'jool/main.html')


def joolabout(request):
    return render(request, 'jool/about.html')


class PostViewSet(ModelViewSet):
    queryset = Stuff.objects.all().order_by('-pub_date')
    serializer_class = PostSerializer

# def register(request):
#    if request.method == "POST":
#        stuff = Stuff(name=request.POST.get('name'), price=request.POST.get(
#            'price'), detail=request.POST.get('detail'), image=request.FILES.get('image'))
#        stuff.pub_date = timezone.now()+timedelta(hours=9)
#        stuff.save()
#        return redirect('mall:index')
#    else:
#        form = StuffForm()
#        return render(request, 'mall/register.html', {'form': form})
