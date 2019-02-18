from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.utils import timezone
import math
from django.contrib.auth.models import User

#Заявка
class Demand(models.Model):
	created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания:')
	id = models.AutoField(primary_key=True)
	description = models.CharField(max_length=200, verbose_name='Описание заявки:')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

	def __str__(self):
		return self.description

	#Подсчет количества позиций
	def position_count(self):
		return Position.objects.filter(id_demand=self.id).count()
	
	#Подсчет количесвтва товаров
	def product_count(self):
		prod_count = Position.objects.filter(id_demand=self.id).aggregate(Sum("quantity"))['quantity__sum']
		if prod_count == None:
			prod_count = 0
		return prod_count

	#Подчет общей стоимости всех позиций в зявке
	def price_all(self):
		price_all= 0
		positions = Position.objects.filter(id_demand=self.id)
		for position in positions:
			price_all += position.quantity * position.price_one
		return price_all

	#Подчет общей стоимости всех позиций в зявке с НДС
#	def price_all_nds(self):
		#price_all_nds= 0
		#positions = Position.objects.filter(id_demand=self.id)
		#for position in positions:
			#price_all_nds += (position.quantity * position.price_one)*1.2
		#pon = math.ceil(price_all_nds)
		#return pon


#Позиции
class Position(models.Model):
	id = models.AutoField(primary_key=True)
	id_demand = models.ForeignKey(Demand, null=False, blank=False, on_delete=models.CASCADE, verbose_name='Номер заявки: ')
	name_product = models.CharField(max_length=50, verbose_name='Наименование:', blank=False)
	art_product = models.CharField(max_length=15, verbose_name='Артикул:', blank=False)
	quantity = models.PositiveSmallIntegerField(blank=False, null=False, verbose_name='Количество:')
	price_one = models.FloatField(verbose_name='Цена за 1 шт:', blank=False)

	def __str__(self):
		return "Позиция " + str(self.id) + ", " + self.name_product 

#	def price_one_nds(self):
		#pon = self.price_one*1.2
		#x = math.ceil(pon)
		#return x

	#Подсчет общей стоимости позиции
	def cost(self):
		return(self.quantity * self.price_one)

	#Подсчет общей стоимости позиции с НДС
#	def cost_nds(self):
		#cost_nds= (self.quantity * self.price_one)*1.2
		#x = math.ceil(cost_nds)
		#return x

#Вывод названия более 30 символов
	def name_reduction(self):
		if len(self.name_product) > 30:
		    return self.name_product[:30] + "..."
		else:
			return self.name_product

