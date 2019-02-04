from django.db import models
from django.conf import settings
from django.utils import timezone

#Заявка
class Demand(models.Model):
	created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания:')
	id = models.AutoField(primary_key=True)
	description = models.CharField(max_length=200, verbose_name='Описание заявки:')
	#position = 
	#product = 
	#price_all = 

	def __str__(self):
		return self.description

	def position_count(self):
		return Position.objects.filter(id_demand=self.id).count()

	def product_count(self):
		#как вывести количество всех товаров
		return Position.objects.filter(quantity=self.id).count()

#Позиции
class Position(models.Model):
	id = models.AutoField(primary_key=True)
	id_demand = models.ForeignKey(Demand, null=False, blank=False, on_delete=models.CASCADE, verbose_name='Номер заявки: ')
	name_product = models.CharField(max_length=50, verbose_name='Наименование:', blank=False)
	art_product = models.CharField(max_length=15, verbose_name='Артикул:', blank=False)
	quantity = models.PositiveSmallIntegerField(blank=False, null=False, verbose_name='Количество:')
	price_one = models.FloatField(verbose_name='Цена за 1 шт:', blank=False)
	#price_all =

	def __str__(self):
		return "Позиция " + str(self.id) + ", " + self.name_product 

	def cost(self):
		return(self.quantity * self.price_one)

