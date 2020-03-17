# Generated by Django 2.2 on 2020-03-17 12:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0003_articlemodel_render'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleimagemodel',
            name='user',
            field=models.IntegerField(blank=True, null=True, verbose_name='上传图片的用户'),
        ),
        migrations.AlterField(
            model_name='specialmanagermodel',
            name='special',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_list', to='article.SpecialModel', verbose_name='专题'),
        ),
        migrations.AlterField(
            model_name='specialmanagermodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='special_list', to=settings.AUTH_USER_MODEL, verbose_name='管理员'),
        ),
        migrations.CreateModel(
            name='ArticlePostLogModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='标题')),
                ('orders', models.IntegerField(verbose_name='显示顺序')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否上架')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='结束时间')),
                ('status', models.IntegerField(choices=[(0, '未审核'), (1, '审核通过'), (2, '审核未通过')], default=0, verbose_name='审核状态')),
                ('manager', models.IntegerField(blank=True, default=None, null=True, verbose_name='审核人')),
                ('post_time', models.DateTimeField(blank=True, default=None, null=True, verbose_name='审核时间')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.ArticleModel', verbose_name='文章')),
                ('special', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.SpecialModel', verbose_name='专题')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='投稿人')),
            ],
            options={
                'verbose_name': '文章的投稿记录',
                'verbose_name_plural': '文章的投稿记录',
                'db_table': 'rr_article_post_log',
            },
        ),
    ]