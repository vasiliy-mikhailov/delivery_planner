# Generated by Django 3.1.4 on 2020-12-22 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_planner_app', '0002_auto_20201222_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externaltaskmodel',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery_planner_app.externaltaskmodel'),
        ),
    ]
