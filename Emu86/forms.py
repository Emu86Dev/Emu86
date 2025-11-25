from django import forms


class MainForm(forms.Form):
    code = forms.CharField(required=False,
                           widget=forms.Textarea(attrs={'cols': 40,
                                                        'rows': 24,
                                                        'oninput':
                                                        'checkForScript()'}))
