# Generated by Django 4.0.1 on 2022-01-27 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0002_poll_alter_candidate_party_num_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='candidate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elections.candidate'),
        ),
    ]
