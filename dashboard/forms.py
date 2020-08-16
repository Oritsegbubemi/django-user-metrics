from django import forms
from django.contrib.auth.models import User
from .models import UserSubscriber

class SendEmailForm(forms.Form):
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ('Subject')}))
    message = forms.CharField(widget=forms.Textarea)
    #users = forms.ModelMultipleChoiceField(label="To", queryset=User.objects.all(),widget=forms.SelectMultiple())
    users = forms.ModelMultipleChoiceField(label="To", queryset=UserSubscriber.objects.values('email'),widget=forms.SelectMultiple())


    def send_email(self, request, queryset):
        form = SendEmailForm(initial={'users': UserSubscriber.objects.values('email')})
        return render(request, 'admin/send_email.html', {'form': form})