# Generated by Django 2.2.2 on 2019-06-17 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restApi', '0004_comment_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='data',
            field=models.DateField(auto_now_add=True),
        ),
    ]