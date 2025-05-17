from django.contrib import admin

from contact.models import Category, Contact



# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email', 'category__name', 'show')
    search_fields = ('first_name', 'last_name', 'phone', 'email','category__name')
    list_filter = ('created_date',)
    ordering = ('-created_date',)
    list_editable = ('show',)
    list_per_page = 10
    list_max_show_all = 100

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)