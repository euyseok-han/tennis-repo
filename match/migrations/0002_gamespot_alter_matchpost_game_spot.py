# Generated by Django 4.2.7 on 2023-11-04 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameSpot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='matchpost',
            name='game_spot',
            field=models.ForeignKey(help_text='게임 장소', null=True, on_delete=django.db.models.deletion.SET_NULL, to='match.gamespot'),
        ),
    ]
