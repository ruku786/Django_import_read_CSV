# Generated by Django 3.0.6 on 2020-10-15 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20201014_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person_detail',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Person'),
        ),
    ]
