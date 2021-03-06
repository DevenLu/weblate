# Generated by Django 2.2.1 on 2019-07-21 18:10

from django.db import migrations, models

import weblate.trans.validators


class Migration(migrations.Migration):

    dependencies = [('trans', '0030_vote_value')]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='check_flags',
            field=models.TextField(
                blank=True,
                default='',
                help_text='Additional comma-separated flags to influence quality checks. Possible values can be found in the documentation.',
                validators=[weblate.trans.validators.validate_check_flags],
                verbose_name='Translation flags',
            ),
        ),
        migrations.AlterField(
            model_name='component',
            name='suggestion_autoaccept',
            field=models.PositiveSmallIntegerField(
                default=0,
                help_text='Automatically accept suggestions with this number of votes, use 0 to turn it off.',
                validators=[weblate.trans.validators.validate_autoaccept],
                verbose_name='Autoaccept suggestions',
            ),
        ),
    ]
