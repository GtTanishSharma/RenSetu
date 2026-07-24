from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0003_category_updated_at_guide_updated_at_faq'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealer',
            name='address',
            field=models.TextField(blank=True, help_text='Full street address. Shows on dealer profile for credibility.'),
        ),
    ]