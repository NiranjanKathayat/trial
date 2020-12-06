from .models import Product, Category, CategoryType
from django.forms import ModelForm


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

class CategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = '__all__'

class CategoryTypeForm(ModelForm):

    class Meta:
        model = CategoryType
        fields = '__all__'

