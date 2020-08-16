from django.contrib import admin
from .models import UserSubscriber
from django.urls import path
from django.conf.urls import include, url
from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required

# Register your models here.
@admin.register(UserSubscriber)
class UserSubscriberAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "created_at", "is_active")
    ordering = ("-created_at",) 
    list_filter = ("created_at",)             
    change_list_template = 'admin/user_change_list.html'
    
    actions = ['make_inactive', 'make_active']

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)


    def make_active(self, request, queryset):
        queryset.update(is_active=True)


    def get_urls(self):
        urls = super(UserSubscriberAdmin, self).get_urls()
        my_urls = [
            path('sendemail/', self.send_email,  name="custom_view"),
        ]
        return my_urls + urls


    def send_email(self, request):
        hello =self.model.objects.values('email')
        print(hello)
        self.message_user(request, "Email sent")
        return HttpResponseRedirect("../")
