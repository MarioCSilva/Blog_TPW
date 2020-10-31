from django.contrib import admin

from app.models import *
# Register your models here.


admin.site.register(Page)
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Followers)

