from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.category


class CategoryType(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    branch_name = models.CharField(max_length=30)

    def __str__(self):
        return self.branch_name


class Product(models.Model):
    category_type = models.ForeignKey(CategoryType, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURl(self):
        try:
            url = 'image.url'
        except:
            url = ''
        return url
