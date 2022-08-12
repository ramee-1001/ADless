from django.contrib import admin
from .models import blogList, Keyword

# Register your models here.
class blogAdmin(admin.ModelAdmin):
    search_fields = ['keyword']

admin.site.register(blogList, blogAdmin)
admin.site.register(Keyword, blogAdmin)
