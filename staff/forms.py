from django import forms
from .models import TestReport

from django.forms import NumberInput
class TestReportForms(forms.ModelForm):
    class Meta:
        model=TestReport
        fields=['Age','HR','O2Sat','Temp','SBP','DBP','Resp']
        widgets = {
            
            'Age': NumberInput(attrs={'placeholder': 'enter age'}),
            'HR': NumberInput(attrs={'placeholder': 'enter heart rate'}),
            'O2Sat': NumberInput(attrs={'placeholder': 'enter o2 saturation'}),
            'Temp': NumberInput(attrs={'placeholder': 'enter temprature'}),
            'SBP': NumberInput(attrs={'placeholder': 'enter Systolic Blood Pressure'}),
            'DBP': NumberInput(attrs={'placeholder': 'enter Diastolic Blood Pressure'}),
            'Resp':NumberInput(attrs={'placeholder': 'enter respiration rate'}),
        }
    def clean_Age(self,*args,**kwargs):
        ge=self.cleaned_data.get('Age')
        if (ge<0 or ge>100) :
             raise  forms.ValidationError("enter a valid age")
        return ge
       

        
       
    def clean_HR(self,*args,**kwargs):
        data=self.cleaned_data.get('HR')
        if (data<40 or data>150) :
            raise forms.ValidationError("enter a valid heartrate")
        return data
    def clean_O2Sat(self,*args,**kwargs):
        d=self.cleaned_data.get('O2Sat')
        if (d>100):
            raise forms.ValidationError("enter a valid oxygen saturation rate")
        return d
    def clean_Temp(self,*args,**kwargs):
        d=self.cleaned_data.get('Temp')
        if (d<86 or d>120):
            raise forms.ValidationError("enter a valid temperature")
        return d
    def clean_SBP(self,*args,**kwargs):
        d=self.cleaned_data.get('SBP')
        if (d<60 or d>280):
            raise forms.ValidationError("enter a valid systolic blood pressure")
        return d
    def clean_DBP(self,*args,**kwargs):
        d=self.cleaned_data.get('DBP')
        if (d<40 or d>180):
            raise forms.ValidationError("enter a valid diasystolic blood pressure")
        return d
    def clean_Resp(self,*args,**kwargs):
        d=self.cleaned_data.get('Resp')
        if (d<8 or d>32):
            raise forms.ValidationError("enter a valid respiration rate")
        return d
    def save(self,commit=True,*args,**kwargs):
        obj=super(TestReportForms,self).save(commit=False,*args,**kwargs)
        if commit:
            obj.MAP=(((2*(obj.DBP))+(obj.SBP))/3)
            obj.save()
        return obj
