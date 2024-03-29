# Generated by Django 2.0.13 on 2019-11-15 03:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Users', '0002_add_roles'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.People')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_receiver', to='Users.People')),
                ('transmitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_transmitter', to='Users.People')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.People')),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.People')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reportType', models.CharField(max_length=255)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.People')),
            ],
        ),
        migrations.CreateModel(
            name='ResidencePublication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('photo', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('address', models.CharField(max_length=64)),
                ('rules', models.CharField(max_length=1024)),
                ('neighborhood', models.CharField(max_length=255)),
                ('locality', models.CharField(max_length=16)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Owner')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('description', models.CharField(max_length=1024)),
                ('publication', models.ManyToManyField(to='StudentHousing.ResidencePublication')),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudentHousing.ResidencePublication'),
        ),
        migrations.AddField(
            model_name='qualification',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudentHousing.ResidencePublication'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudentHousing.ResidencePublication'),
        ),
        migrations.AddField(
            model_name='notification',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudentHousing.ResidencePublication'),
        ),
        migrations.AddField(
            model_name='comment',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudentHousing.ResidencePublication'),
        ),
    ]
