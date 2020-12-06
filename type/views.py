from django.shortcuts import render, redirect

from type.forms import ProductForm, CategoryForm, CategoryTypeForm
from type.models import Product, CategoryType, Category


def allTypes(request):
    category = Category.objects.all()
    category_type = CategoryType.objects.all()
    products = Product.objects.all()
    return render(request, 'type/base.html', {'products':products, 'category':category, 'category_type': category_type})

def add_new(request):
    if request.method == 'POST':
        print('post')
        product_form = ProductForm(request.POST, request.FILES)
        category_type = CategoryTypeForm(request.POST)
        if product_form.is_valid():
            product_form.save()
            print('saved')
        return redirect('/type/')
    else:
        category_type = CategoryTypeForm()
        product_form = ProductForm()
        print('Error3.....')
    return render(request, 'type/add_new.html', {'category_type':category_type, 'product_form':product_form})

def add_new_category(request):
    if request.method == 'POST':
        print('post')
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            print('saved')
        return redirect('/type/')
    else:
        category_form = CategoryForm()
        print('Error2.....')
    return render(request, 'type/add_new.html', {'product_form':category_form})

def add_new_branch_category(request):
    if request.method == 'POST':
        print('post')
        category_type_form = CategoryTypeForm(request.POST)
        if category_type_form.is_valid():
            category_type_form.save()
            print('saved')
        return redirect('/type/')
    else:
        category_type_form = CategoryTypeForm()
        print('Error1.....')
    return render(request, 'type/add_new.html', {'product_form':category_type_form})


