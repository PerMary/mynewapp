# Generated by Django 2.0.10 on 2019-01-24 06:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Demand',
            fields=[
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания:')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=200, verbose_name='Описание заявки:')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name_product', models.CharField(max_length=50, verbose_name='Наименование позиции:')),
                ('art_product', models.CharField(max_length=15, verbose_name='Артикул:')),
                ('quantity', models.PositiveSmallIntegerField(verbose_name='Количество:')),
                ('price_one', models.FloatField(verbose_name='Цена за 1 шт:')),
                ('id_demand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.Demand', verbose_name='Номер заявки: ')),
            ],
        ),
    ]
