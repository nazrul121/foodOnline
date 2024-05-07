from django.shortcuts import render, HttpResponse, get_object_or_404,redirect
from django.contrib import messages
from menu.forms import CategoryForm, FoodForm
from menu.models import Category, FoodItem
from .models import Vendor
from django.template.defaultfilters import slugify

# Create your views here.
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/menu_builder.html', context)


def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    # return HttpResponse(vendor)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category).order_by('-created_at')[:15000]
    context = {
        'fooditems': fooditems,
        'category': category,
    }
    return render(request, 'vendor/fooditems_by_category.html', context)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request=request)  # Pass request object
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            # existing_category = Category.objects.filter(vendor=category.vendor, category_name=category_name).exists()
            # if existing_category:
            #     message = f"You already have <b>{category_name}</b> category"
            #     messages.warning(request, message)
            #     return redirect('add_category')
            
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)

    else:
        form = CategoryForm()

    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)


def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            
            # form.save()
            # messages.success(request, 'Category updated successfully!')
            # return redirect('menu_builder')    

            existing_category = Category.objects.filter(
                vendor=category.vendor,category_name__iexact=category_name
            ).exclude(id=category.id).exists()

            if existing_category:
                message = f"You already have <b>{category_name}</b> category"
                messages.warning(request, message)
                return redirect('edit_category', pk=category.id)
            else:
                form.save()
                messages.success(request, 'Category updated successfully!')
                return redirect('menu_builder')            

    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'vendor/edit_category.html', context)


def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('menu_builder')


def add_food(request):
    # print(request.user)
    user_id = request.user.id
    
    if request.method == 'POST':
        form = FoodForm(request.POST,request.FILES) #pass user_id to form to get category data matching with this vendor
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(foodtitle)
            form.save()
            messages.success(request, 'Food Item added successfully!')
            return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodForm()
        # get category matching with vendor, we did this with above line sending user_id to form
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))

    context = {
        'form': form,
    }
    return render(request, 'vendor/add_food.html', context)

def edit_food(request, pk=None):
    user_id = request.user.id
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(foodtitle)
            form.save()
            messages.success(request, 'Food Item updated successfully!')
            return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)

    else:
        form = FoodForm(instance=food)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))

    context = {
        'form': form,
        'food': food,
    }
    return render(request, 'vendor/edit_food.html', context)



def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request, 'Food Item has been deleted successfully!')
    return redirect('fooditems_by_category', food.category.id)
