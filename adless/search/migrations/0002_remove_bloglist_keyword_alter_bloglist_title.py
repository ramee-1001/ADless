# Generated by Django 4.0.3 on 2022-07-27 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloglist',
            name='keyword',
        ),
        migrations.AlterField(
            model_name='bloglist',
            name='title',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]