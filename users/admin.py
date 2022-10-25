from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import *

User = get_user_model()

#This is necessary because we are redefining the class "User" in the model
@admin.register(User)
class UserAdmin(UserAdmin):
    pass

class NFTAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name', 'description')
    list_editable = ('price',)
    list_filter = ('collection',)

    # def save_model(self, request, obj, form, change):
    #     obj.user_id = request.user.id
    #     obj.save()
    # def get_list_display(self, request):
    #     print(request)
        #return ", ".join([cat.name for cat in request.NFT.all()])

class NFTCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(CategoryNFT, NFTCategoryAdmin)
admin.site.register(NFT, NFTAdmin)
