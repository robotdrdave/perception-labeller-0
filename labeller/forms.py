from django import forms

class SpamForm(forms.Form):
    field = forms.TypedChoiceField(label='Answer', coerce=lambda x: x =='True', 
                                   choices=((False, 'Not Spam'), (True, 'Spam')))

class YNForm(forms.Form):
    field = forms.TypedChoiceField(label='Answer', coerce=lambda x: x =='True', 
                                   choices=((False, 'No'), (True, 'Yes')))

class OpinionForm(forms.Form):
    yn_field = forms.TypedChoiceField(label='Answer', coerce=lambda x: x =='True', 
                                   choices=((False, 'No'), (True, 'Yes')))
    text_field = forms.CharField(label='If yes, What is the subjective span of text?', required=False, 
                                 widget=forms.TextInput(attrs={'size':80}))

class FactForm(forms.Form):
    yn_field = forms.TypedChoiceField(label='Answer', coerce=lambda x: x =='True', 
                                   choices=((False, 'No'), (True, 'Yes')))
    text_field = forms.CharField(label='If yes, What is the objective span of text?', required=False, 
                                 widget=forms.TextInput(attrs={'size':80}))

class ProductForm(forms.Form):
    yn_field = forms.TypedChoiceField(label='Answer', coerce=lambda x: x =='True', 
                                   choices=((False, 'No'), (True, 'Yes')))
    text_field = forms.CharField(label='If yes, What is the product or service mentioned?', required=False, 
                                 widget=forms.TextInput(attrs={'size':80}))