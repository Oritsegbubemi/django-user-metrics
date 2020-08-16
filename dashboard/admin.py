from django.contrib import admin
from .models import UserSubscriber
from .forms import SendEmailForm
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

# Register your models here.
@admin.register(UserSubscriber)
class UserSubscriberAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "created_at", "is_active")
    ordering = ("-created_at",) 
    list_filter = ("created_at",)             
    change_list_template = 'admin/user_change_list.html'
    
    actions = ['make_inactive', 'make_active']

    @method_decorator(staff_member_required)
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    @method_decorator(staff_member_required)
    def make_active(self, request, queryset):
        queryset.update(is_active=True)


class SendUserEmails(FormView):
    template_name = 'admin/send_email.html'
    form_class = SendEmailForm
    #success_url = '/thanks/'
    success_url = reverse_lazy('admin:users_user_changelist')

    def form_valid(self, form):
        users = form.cleaned_data['users']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        email_users.delay(users, subject, message)
        user_message = '{0} users emailed successfully!'.format(form.cleaned_data['users'].count())
        messages.success(self.request, user_message)
        return super(SendUserEmails, self).form_valid(form)