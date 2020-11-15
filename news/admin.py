from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import News, Category



class NewsAdmin(admin.ModelAdmin):
    list_display = ('id','title','category', 'created_at','updated_at','is_published')
    list_display_links = ('id','title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter =  ('is_published', 'category')
    fields  = ('title','category', 'content', 'is_published', 'views', 'created_at','updated_at')
    readonly_fields = ('views','created_at','updated_at')
    save_on_top = True
    # def get_photo(self, obj):
    #     if obj.photo:
    #         return mark_safe(f'<img src="{obj.photo.url}" width ="100">')
    #     else:
    #         return 'Фото не установлено'
    # get_photo.short_description = 'Миниатюра'
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id','title')
    search_fields = ('title',)    
    
admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title='Админ-панель "Управление новостями"'
admin.site.site_header='Админ-панель "Управление новостями"'

