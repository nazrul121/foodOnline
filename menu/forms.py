from urllib import request

from django import forms
from django.utils.text import slugify
from .models import Category, FoodItem
from vendor.models import Vendor
from accounts.validators import allow_only_images_validator

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['category_name'].required = False
        self.fields['description'].required = False

    def clean(self):
        cleaned_data = super().clean()
        user = self.request.user if self.request else None
        category_name = cleaned_data.get('category_name')

        if not category_name:
            self.add_error('category_name', 'Empty category name is not allowed')
            
        if user and user.is_authenticated:
            vendor = self.get_vendor(user)
            if vendor:
                if category_name:
                    # Check for existing categories with the same name for the same vendor
                    existing_categories = Category.objects.filter(
                        vendor=vendor, category_name__iexact=category_name
                    ).exclude(id=self.instance.id if self.instance else None)

                    if existing_categories.exists():
                        self.add_error('category_name', f'You already have "{category_name}" category.')

        return cleaned_data

    def get_vendor(self, user):
        try:
            return Vendor.objects.get(user=user)
        except Vendor.DoesNotExist:
            return None




class FoodForm(forms.ModelForm):
   
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100', 'required':False}), validators=[allow_only_images_validator])
    is_available = forms.BooleanField(label='Is available', required=False, widget=forms.CheckboxInput(attrs={'id': 'isAvalCheck'}))

    def __init__(self, *args, **kwargs):
        # user_id = kwargs.pop('user_id', None)
        # vendor = Vendor.objects.get(user=user_id)
        # print("Logged-in user ID:", vendor)  # Print the logged-in user ID
        # super(FoodForm, self).__init__(*args, **kwargs)

        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['food_title'].required = False
        self.fields['description'].required = False
        self.fields['price'].required = False
        self.fields['is_available'].required = False
        self.fields['image'].required = False

        # if vendor:
        #     self.fields['category'].queryset = Category.objects.filter(vendor=vendor)
        
      
    class Meta:
        model = FoodItem
        fields = ['category', 'food_title', 'description', 'price', 'image', 'is_available']

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        food_title = cleaned_data.get('food_title')
        price = cleaned_data.get('price')

        if not category:
            self.add_error('category', 'Empty category is not allowed')
        if not food_title:
            self.add_error('food_title', 'Empty food title is not allowed')
        
        if not price:
            self.add_error('price', 'Empty food price is required')


# from django import forms
# from .models import Category
# from vendor.models import Vendor  # Assuming Vendor model is imported correctly

# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['category_name', 'description']

#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request', None)  # Extract the 'request' object if passed
#         super().__init__(*args, **kwargs)
#         self.fields['category_name'].required = False
#         self.fields['description'].required = False

#     def clean(self):
#         cleaned_data = super().clean()
#         category_name = cleaned_data.get('category_name')
 
            
#         if not category_name:
#              self.add_error('category_name', 'Empty category name is not allowed')
