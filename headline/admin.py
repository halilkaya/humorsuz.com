from django.contrib import admin
from headline.models import Category, Object, Headline

class CategoryAdmin(admin.ModelAdmin):
    pass

class ObjectAdmin(admin.ModelAdmin):
    pass

class HeadlineAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Object, ObjectAdmin)
admin.site.register(Headline, HeadlineAdmin)
