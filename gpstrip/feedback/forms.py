from django import forms

class FeedbackForms(forms.Form):
    feedback_text = forms.CharField(label="Відгук", required=False, widget=forms.Textarea(attrs={
        'placeholder': 'Відгук'}))