# Generated by Django 3.0.6 on 2020-06-18 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0006_auto_20200618_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='QuestionGroup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polling.QuestionGroup'),
        ),
    ]