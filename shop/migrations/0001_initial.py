# Generated by Django 4.2.5 on 2023-10-21 13:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProductStyle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='product_brands/')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('brands', models.IntegerField(verbose_name='International Brands')),
                ('quality', models.IntegerField(verbose_name='High-Quality Products')),
                ('customers', models.IntegerField(verbose_name='Happy customers')),
                ('twitter', models.URLField()),
                ('facebook', models.URLField()),
                ('instagram', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='ShopBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Brand Name')),
                ('img', models.FileField(upload_to='brands/', verbose_name='Brand Image (*.svg)')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=13)),
                ('address', models.CharField(max_length=150)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, editable=False)),
                ('title', models.CharField(max_length=140)),
                ('img1', models.ImageField(upload_to='products/img1/')),
                ('img2', models.ImageField(blank=True, null=True, upload_to='products/img2/')),
                ('img3', models.ImageField(blank=True, null=True, upload_to='products/img3/')),
                ('quantity', models.PositiveIntegerField()),
                ('gender', models.CharField(choices=[('M', 'Man'), ('WM', 'Woman'), ('ML', 'Multiple')], default='ML', verbose_name='Product Gender')),
                ('stars', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Current Price')),
                ('discount', models.PositiveIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(100)], verbose_name='Price Discount (%)')),
                ('is_available', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brand_products', to='shop.productbrand')),
                ('size', models.ManyToManyField(blank=True, related_name='size_products', to='shop.size')),
                ('style', models.ManyToManyField(related_name='styles_products', to='shop.productstyle')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_products', to='shop.producttype')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_orders', to='shop.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_wishlist', to='shop.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_wishlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.DecimalField(decimal_places=1, max_digits=2)),
                ('body', models.TextField()),
                ('posted_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_reviews', to='shop.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reviews', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['-posted_date'], name='shop_review_posted__953c65_idx')],
            },
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['-timestamp'], name='shop_produc_timesta_e88c71_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('user', 'product')},
        ),
    ]
