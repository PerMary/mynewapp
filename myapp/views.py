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
			return redirect('demand_detail', id_demand=demand.id)
	else:
		form = DemandForm()
		return render (request, 'myapp/demand_new.html', {'form': form})

#Редактирование заявки
def demand_edit(request,id_demand):
	demand = get_object_or_404(Demand, id_demand=id_demand)
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
def demand_detail(request, id_demand):
	demand = get_object_or_404(Demand, id=id_demand)
	positions = Position.objects.filter(id_demand=id_demand)
	return render(request, 'myapp/demand_detail.html', {'demand': demand, 'positions': positions})

#Удаление заявки на главной странице 
def demand_remove(request,id_demand):
	demand = get_object_or_404(Demand, id=id_demand)
	demand.delete()
	return redirect('demand_list')

#Добавление новой позиции в заявку
def position_new(request, id_demand):
	demand = get_object_or_404(Demand, id=id_demand)
	positions = Position.objects.filter(id_demand=id_demand)
	if request.method == "POST":
		form = PositionForm(request.POST)
		if form.is_valid():
			positions = form.save(commit=False)
			#При сохранении форма должна автоматически привязаться к заявке в которой она создается 
			positions.id_demand = demand 
			positions.save()
			return redirect('demand_detail', id_demand=id_demand)
	else:
	    form = PositionForm()
	return render(request, 'myapp/position_new.html', {'demand': demand, 'form': form})

#Редактирование позиции
def position_edit(request, id_demand, id_position):
	demand = get_object_or_404(Demand, id=id_demand)
	position = Position.objects.get(id=id_demand)
	if request.method == "POST":
		form = PositionForm(request.POST, instance=position)
		if form.is_valid():
			position = form.save(commit=False)
			position.id = id_position
			position.id_demand = demand 
			position.save()
			return redirect('demand_detail', id_demand=id_demand)
	else:
	    form = PositionForm(instance=position)
	return render(request, 'myapp/position_new.html', {'demand': demand, 'form': form})


#Удаление позиции
def position_remove(request,id_demand, id_position):
	demand = get_object_or_404(Demand, id=id_demand)
	position = Position.objects.get(id=id_position)
	position.id = id_position
	position.id_demand = demand
	position.delete()
	return redirect('demand_detail', id_demand=demand.id)


