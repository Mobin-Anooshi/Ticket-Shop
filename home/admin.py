from django.contrib import admin
from .models import Travel,TravelDetails,Distance,Ticket

# Register your models here.


admin.site.register(Travel)
admin.site.register(TravelDetails)
admin.site.register(Distance)
admin.site.register(Ticket)