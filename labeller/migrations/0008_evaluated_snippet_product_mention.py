# Generated by Django 3.1.6 on 2021-02-18 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labeller', '0007_auto_20210218_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluated_snippet',
            name='product_mention',
            field=models.BooleanField(default=False),
        ),
    ]