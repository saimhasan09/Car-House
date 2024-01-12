# Generated by Django 5.0.1 on 2024-01-10 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('posts', '0002_post_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, related_name='posts', to='categories.category'),
        ),
    ]
