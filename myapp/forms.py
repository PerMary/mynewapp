from django import forms

from .models import Demand, Position

#Добавление новой заявки
class DemandForm(forms.ModelForm):

	class Meta():
		model = Demand
		fields = ('description',)

#Добавление новой позоции в заявку
class PositionForm(forms.ModelForm):

	class Meta():
		model = Position
		fields = ('name_product', 'art_product', 'quantity', 'price_one',)
