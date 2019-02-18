from django.shortcuts import render, get_object_or_404
from .models import Position, Demand
from .forms import DemandForm, PositionForm
from django.shortcuts import redirect
from django.utils import timezone
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse, Http404
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors, styles
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, Permission, User



#Вывод всех заявок на главной странице
@login_required
def demand_list(request):
	demands = Demand.objects.order_by('created_date')	
	return render(request, 'myapp/demand_list.html', {'demands': demands})

#Добавление новой заявки
@login_required
@permission_required('myapp.add_demand', 'non' )
def demand_new(request):
	if request.method == "POST":
		form = DemandForm(request.POST)
		if form.is_valid():
			demand = form.save(commit=False)
			demand.created_date = timezone.now()
			demand.user = request.user
			demand.save()
			return redirect('demand_detail', id_demand=demand.id)
	else:
		form = DemandForm()
		return render (request, 'myapp/demand_new.html', {'form': form})

#Редактирование заявки
@login_required
@permission_required('myapp.change_demand', 'non' )
def demand_edit(request,id_demand):
	demand = get_object_or_404(Demand, id=id_demand)
	#if request.user.groups.filter(name="Начальники") or demand.user == request.user:
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
@login_required
def demand_detail(request, id_demand):
	demand = get_object_or_404(Demand, id=id_demand)
	positions = Position.objects.filter(id_demand=id_demand)
	return render(request, 'myapp/demand_detail.html', {'demand': demand, 'positions': positions})

#Удаление заявки на главной странице
@login_required 
@permission_required('myapp.delete_demand', 'non' )
def demand_remove(request,id_demand):
	demand = get_object_or_404(Demand, id=id_demand)
	if demand.user == request.user or request.user.groups.filter(name="Начальники"):
	    if request.method == "POST":
	        demand.delete()
	        return redirect('demand_list')
	    else:
	        return render (request, 'myapp/demand_remove.html')
	else:
	    return render (request, 'myapp/non.html')
	
#Ограничение доступа
def non(request):
	return render(request, 'myapp/non.html')

#Добавление новой позиции в заявку
@login_required
@permission_required('myapp.add_position', 'non' )
def position_new(request, id_demand):
	demand = get_object_or_404(Demand, id=id_demand)
	positions = Position.objects.filter(id_demand=id_demand)
	if request.method == "POST":
		form = PositionForm(request.POST)
		if form.is_valid():
			positions = form.save(commit=False)
			positions.save()
			return redirect('demand_detail', id_demand=id_demand)
	else:
		form = PositionForm()
	return render(request, 'myapp/position_new.html', {'demand': demand, 'form': form})

#Редактирование позиции
@login_required
@permission_required('myapp.change_position', 'non' )
def position_edit(request, id_demand, id_position):
	position = Position.objects.get(id=id_position)
	demand = get_object_or_404(Demand, id=id_demand)
	if request.method == "POST":
		form = PositionForm(request.POST)
		if form.is_valid():
			position = form.save(commit=False)
			position.id = id_position
			position.id_demand = demand
			position.save()
			return redirect('demand_detail', id_demand=id_demand)
	else:
		form = PositionForm(instance=position)
	return render(request, 'myapp/position_edit.html', { 'form': form})


#Удаление позиции
@login_required
@permission_required('myapp.delete_position', 'non' )
def position_remove(request,id_demand, id_position):
	demand = get_object_or_404(Demand, id=id_demand)
	position = Position.objects.get(id=id_position)
	if demand.user == request.user or request.user.groups.filter(name="Начальники"):
	    if request.method == "POST":
	        position.id = id_position
	        position.id_demand = demand
	        position.delete()
	        return redirect('demand_detail', id_demand=demand.id)
	    else:
	        return render (request, 'myapp/position_remove.html', {'demand': demand})
	else:
	    return render (request, 'myapp/non.html')
	


#Создание PDF
@login_required
def create_pdf(request, id_demand, ):
	demand = get_object_or_404(Demand, id=id_demand)
	positions = Position.objects.filter(id_demand=id_demand)

#	Заявка
	demand_date ="%s" %demand.created_date.strftime('%d.%m.%Y')
	demand_number = "%s" %demand.id
	demand_description = "%s" %demand.description
	demand_quantity_pos = "%s" %demand.position_count()
	demand_quantity_prod = "%s" %demand.product_count()
	demand_price_all = "%s" %demand.price_all()
 

	filename = 'Demand_' + str(demand.id) +'_detail.pdf'
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="%s"' % filename

	myfont = ttfonts.TTFont('Times', '/home/marina/django/myapp/static/myapp/TIMES.TTF')
	pdfmetrics.registerFont(myfont)
	
	
	styles = getSampleStyleSheet()
	temp = BytesIO()
	p = canvas.Canvas(temp)

#   Стили
	style_par = ParagraphStyle("text", fontName="Times", 
									   fontSize=12, 
									   alignment = TA_LEFT, 
									   spaceAfter=5, 
									   spaceBefore=5)
	style_nametable = ParagraphStyle("text", fontName="Times", 
									  fontSize=14, 
									  alignment = TA_CENTER, 
									  spaceAfter=15, 
									  spaceBefore=30 )
	style_title = ParagraphStyle("text",fontName="Times", 
										fontSize=18, 
										alignment = TA_CENTER, 
										spaceAfter=30, 
										spaceBefore=10 )
	style_footer_p = ParagraphStyle("text", fontName="Times", 
										  fontSize=12, 
										  alignment = TA_LEFT, 
										  spaceAfter=0, 
										  spaceBefore=50,
										  bulletIndent = 100,
										  spaceShrinkage = 20 )
	style_footer_d = ParagraphStyle("text", fontName="Times", 
										  fontSize=12, 
										  alignment = TA_LEFT, 
										  spaceAfter=0, 
										  spaceBefore=15,
										  bulletIndent = 100,
										   )

	story = [Spacer(1,0.25*inch)]
#   Шапка документа
	header = Paragraph("Информация по заявке №{0}".format(demand_number), style= style_title)
	story.append(header)

#   Описание заявки
	a = Paragraph("Дата создания: {0}".format(demand_date), style= style_par)
	b = Paragraph("Описание: {0}".format(demand_description), style= style_par)
	c = Paragraph("Кол-во позиций: {0}".format(demand_quantity_pos), style= style_par)
	d = Paragraph("Кол-во товаров: {0}".format(demand_quantity_prod), style= style_par)
	e = Paragraph("Общая ст-ть (руб): {0}".format(demand_price_all), style= style_par)
	story.append(a)
	story.append(b)
	story.append(c)
	story.append(d)
	story.append(e)

	doc2 = SimpleDocTemplate(temp, rightMargin=20, leftMargin=20, topMargin=0, bottomMargin=0)
	blok_table = []
	title = Paragraph("Позиции в заявке №{0}".format(demand_number), style= style_nametable)
	story.append(title)
	if len(positions) == 0:
		no = Paragraph("Нет созданных позиций для данной заявки", style=style_nametable)
		story.append(no)
	else:
		tablehead =[[u'Наименование ',u'Артикул ', u'Кол-во', u'Цена за шт(руб)', u'Общая ст-ть (руб)']]
		tabhead=Table(tablehead, rowHeights=[1.25 * cm], colWidths=[7.5 * cm, 4 * cm, 1.5 * cm, 3.5 * cm, 3.5 * cm] )
		tabhead.setStyle(TableStyle([
				('FONT', (0, 0), (-1, -1), 'Times', 11),
				('ALIGN', (0, 0), (-1, -1), 'CENTER'),
				('GRID', (0, 0), (-1, -1), 0.25, colors.black),
				]))
		story.append(tabhead)
	for position in positions:
		tablebody = [["%s" %position.name_reduction(), "%s" %position.art_product, "%s" %position.quantity, "%s" %position.price_one, "%s" %position.cost()]]

		tabbody=Table(tablebody, colWidths=[7.5 * cm, 4 * cm, 1.5 * cm, 3.5 * cm, 3.5 * cm] )
		tabbody.setStyle(TableStyle([
			('FONT', (0, 0), (-1, -1), 'Times', 11),
			('ALIGN', (0, 0), (-1, -1), 'CENTER'),
			('GRID', (0, 0), (-1, -1), 0.25, colors.black),
			]))

		story.append(tabbody)

#   Оформление подвала
	date_created = datetime.datetime.today().strftime("%d.%m.%Y")
	user_created = request.user.last_name + ' ' + request.user.first_name + ' ' 
	tablefooter = [[u'Подписи:', u'Дата:      '],
		       [u'{0}'.format(user_created), u'{0}'.format(date_created)],
		      ]
	tabfoo = Table(tablefooter, rowHeights=30, colWidths=200, spaceBefore=50)
	tabfoo.setStyle(TableStyle([
	('FONT', (0, 0), (-1, -1), 'Times', 11),
	('ALIGN', (0, 0), (0, -1), 'LEFT'),
	('ALIGN', (1, 0), (1, -1), 'RIGHT'),
		]))

	story.append(tabfoo)

	p.showPage()
	p.save()

	doc2.build(story)
	pdf = temp.getvalue()
	temp.close()
	response.write(pdf)
	


	return response



