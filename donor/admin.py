from django.contrib import admin
from .models import UserModel,District,Division,DonationRequestModel

# Register your models here.
admin.site.register(UserModel)
admin.site.register(District)
admin.site.register(Division)
admin.site.register(DonationRequestModel)