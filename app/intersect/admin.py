from django.contrib import admin
from intersect.models import  ClientResult, ClientTable, ClientTask, SimpleHash

# Register your models here.
admin.site.register(SimpleHash)
admin.site.register(ClientTable)
admin.site.register(ClientTask)
admin.site.register(ClientResult)