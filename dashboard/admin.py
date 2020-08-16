import json
from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from django.urls import path
from .models import UserSubscriber
from .forms import SendEmailForm
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages


@admin.register(UserSubscriber)
class UserSubscriberAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "created_at", 'is_active')
    ordering = ("-created_at",)
    change_list_template = 'admin/user_change_list.html'
    list_filter = ("created_at",)     

    # Inject chart data on page load in the ChangeList view
    def changelist_view(self, request, extra_context=None):
        chart_data = self.chart_data()
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path("chart_data/", self.admin_site.admin_view(self.chart_data_endpoint))
        ]
        return extra_urls + urls

    def chart_data_endpoint(self, request):
        chart_data = self.chart_data()
        return JsonResponse(list(chart_data), safe=False)

    def chart_data(self):
        return (
            UserSubscriber.objects.annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
            
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
    success_url = '/admin/dashboard/usersubscriber/'

    def form_valid(self, form):
        users = form.cleaned_data['users']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        send_mail(
            subject,
            message,
            'from@example.com',
            [users],
            fail_silently=False,
        )
        user_message = '{0} users emailed successfully!'.format(form.cleaned_data['users'].count())
        messages.success(self.request, user_message)
        return super(SendUserEmails, self).form_valid(form)