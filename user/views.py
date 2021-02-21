from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import json
from .models import *
# Create your views here.

def homepage(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request,"index.html",context)

class RegistrationForm(UserCreationForm):
    """Provide a view for creating users with only the requisite fields."""

    class Meta:
        model = User
        # Note that password is taken care of for us by auth's UserCreationForm.
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

def register(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')

	else:
		form = RegistrationForm()

	return render(request,"signup.html",{'form':form})

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
	else:
		items = []
		order = {'get_cart_total':0,'get_cart_items':0}

	context = {'items':items,'order':order}
	return render(request,"cart.html",context)

def checkout(request):
	context = {}
	return render(request,"checkout.html",context)

def login(request):
	context = {}
	return render(request,"registration/login.html",context)

def updateitem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('action:',action)
	print('productId',productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer,complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order = order,product = product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('item added!',safe=False)