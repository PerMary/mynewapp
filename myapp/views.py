from django.shortcuts import render, get_object_or_404
from .models import Position, Demand
from .forms import DemandForm, PositionForm
from django.shortcuts import redirect
from django.utils import timezone

#Вывод всех заявок на главной странице
def demand_list(request):
	demands = Demand.objects.order_by('created_date')	
	return render(request, 'myapp/demand_list.html', {'demands': demands})

#Добавление новой заявки
def demand_new(request):
	if request.method == "POST":
		form = DemandForm(request.POST)
		if form.is_valid():
			demand = form.save(commit=False)
			demand.created_date = timezone.now()
			demand.save()
			return redirect('demand_detail', pk=demand.id)
	else:
		form = DemandForm()
		return render (request, 'myapp/demand_new.html', {'form': form})

#Редактирование заявки
def demand_edit(request,pk):
	demand = get_object_or_404(Demand, pk=pk)
	if request.method == "POST":
		form = DemandForm(request.POST, instance=demand)
		if form.is_valid():
			demand = form.save(commit=False)
			demand.save()
			return redirect('demand_list')
	else:
		form = DemandForm(instance=demand)
		return render (request, 'myapp/demand_edit.html', {'form': form})

#Просмотр конкретной завяки (описание с таблицей позиций)
def demand_detail(request, pk):
	demand = get_object_or_404(Demand, pk=pk)
	positions = Position.objects.filter(id_demand=pk)
	return render(request, 'myapp/demand_detail.html', {'demand': demand, 'positions': positions})

#Удаление заявки на главной странице 
def demand_remove(request,pk):
	demand = get_object_or_404(Demand, pk=pk)
	demand.delete()
	return redirect('demand_list')

#Добавление новой позиции в заявку
def position_new(request, pk):
	demand = get_object_or_404(Demand, pk=pk)
	positions = Position.objects.filter(id_demand=pk)
	if request.method == "POST":
		form = PositionForm(request.POST)
		if form.is_valid():
			positions = form.save(commit=False)
			#При сохранении форма должна автоматически привязаться к заявке в которой она создается 
			positions.id_demand = demand 
			positions.save()
			return redirect('demand_detail', pk=demand.pk)
	else:
	    form = PositionForm()
	return render(request, 'myapp/position_new.html', {'demand': demand, 'form': form})

#Редактирование позиции
def position_edit(request, pk):
	demand = get_object_or_404(Demand, pk=pk)
	#как привязать к конкретной позиции
	positions = Position.objects.get(id_demand=pk)
	if request.method == "POST":
		form = PositionForm(request.POST, instance=positions)
		if form.is_valid():
			position = form.save(commit=False)
			#При сохранении форма должна автоматически привязаться к заявке в которой она создается 
			position.id_demand = demand 
			position.save()
			return redirect('demand_detail', pk=demand.pk)
	else:
	    form = PositionForm(instance=positions)
	return render(request, 'myapp/position_new.html', {'demand': demand, 'form': form})


#Удаление позиции
#Удаляет все позиции из заявки, как удалить конкретную позицию?
def position_remove(request,pk):
	demand = get_object_or_404(Demand, pk=pk)
	position = Position.objects.filter(id_demand=pk)
	#position.id = demand
	position.delete()
	return redirect('demand_detail', pk=demand.pk)


