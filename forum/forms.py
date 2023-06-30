from django import forms
from forum.models import LogMessage
from forum.models import Profile

class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ("message",)   # NOTE: the trailing comma is required
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', )