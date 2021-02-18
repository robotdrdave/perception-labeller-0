# Generated by Django 3.1.6 on 2021-02-17 10:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('labeller', '0002_auto_20210216_1759'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snippet',
            name='evaluator',
        ),
        migrations.RemoveField(
            model_name='snippet',
            name='extracted_span',
        ),
        migrations.RemoveField(
            model_name='snippet',
            name='is_fact',
        ),
        migrations.RemoveField(
            model_name='snippet',
            name='is_harmful',
        ),
        migrations.RemoveField(
            model_name='snippet',
            name='is_opinion',
        ),
        migrations.AddField(
            model_name='snippet',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='snippet',
            name='entity',
            field=models.CharField(default=None, max_length=63),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='snippet',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.CreateModel(
            name='Evaluated_Snippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_harmful', models.BooleanField()),
                ('is_opinion', models.BooleanField()),
                ('is_fact', models.BooleanField()),
                ('extracted_span', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('evaluator', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='evaluated_snippets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
