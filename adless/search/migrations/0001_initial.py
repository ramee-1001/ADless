# Generated by Django 4.0.3 on 2022-07-27 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='blogList',
            fields=[
                ('keyword', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('blogurl', models.CharField(max_length=50)),
            ],
        ),
    ]