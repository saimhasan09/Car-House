from django.contrib import admin
from . import models

# Register your models here.
# admin.site.register(models.Category)


# customize database view
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}  # slug field value ta name dea fil hobe
    list_display = ["name", "slug"]  # ja ja amra dekte cai name and slug


admin.site.register(models.Category, CategoryAdmin)
