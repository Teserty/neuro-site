# Generated by Django 2.2.7 on 2019-11-22 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewDialog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_text', models.TextField(blank=True, default='')),
                ('our_text', models.TextField(blank=True, default='')),
                ('result', models.TextField(blank=True, default='')),
                ('is_good_result', models.BooleanField(default=False)),
                ('stage', models.IntegerField(default=0)),
            ],
        ),
    ]