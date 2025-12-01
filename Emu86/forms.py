from django import forms

CODE_COLS = 48
CODE_ROWS = 48

class MainForm(forms.Form):
    code = forms.CharField(required=False,
                           widget=forms.Textarea(attrs={'cols': CODE_COLS,
                                                        'rows': CODE_ROWS,
                                                        'oninput':
                                                        'checkForScript()'}))
