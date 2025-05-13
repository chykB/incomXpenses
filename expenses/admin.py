from django.contrib import admin
from .models import Expense, Category
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date', 'description', 'owner', 'category',)
    search_fields = ('amount', 'date', 'owner', 'category',)
    list_filter = ('category',)
    ordering = ('-date',)

admin.site.register(Expense)
admin.site.register(Category)