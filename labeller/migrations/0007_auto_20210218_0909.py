# Generated by Django 3.1.6 on 2021-02-18 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('labeller', '0006_auto_20210218_0123'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluated_snippet',
            name='entity',
            field=models.CharField(default='', max_length=63),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='evaluated_snippet',
            name='evaluator',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.RESTRICT, related_name='evaluated_snippets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='evaluated_snippet',
            name='snippet',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.RESTRICT, related_name='evaluated_snippets', to='labeller.snippet'),
        ),
    ]
