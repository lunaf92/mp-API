# Generated by Django 3.2.18 on 2023-02-16 21:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_auto_20230216_2141"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=50, null=True, verbose_name="Username"),
        ),
    ]
