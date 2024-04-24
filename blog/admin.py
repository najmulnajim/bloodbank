from django.contrib import admin
from .models import BlogModel,Comments

# Register your models here.
class BlogModelAdmin(admin.ModelAdmin):
    list_display=['title','author']
admin.site.register(BlogModel,BlogModelAdmin)

class CommentsAdmin(admin.ModelAdmin):
    list_display=['commenter_name','blog']
admin.site.register(Comments,CommentsAdmin)