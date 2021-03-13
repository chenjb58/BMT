# Generated by Django 2.2.5 on 2021-03-12 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessObject',
            fields=[
                ('version', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('initial', models.CharField(max_length=64)),
                ('xmlns', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('instancesExpr', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_label', models.CharField(max_length=64)),
                ('log_expr', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Exit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_label', models.CharField(max_length=64)),
                ('log_expr', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('state_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('is_initial', models.BooleanField()),
                ('is_final', models.BooleanField()),
                ('bussiness_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.BusinessObject')),
                ('onentry', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='back_end.Entry')),
                ('onexit', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='back_end.Exit')),
            ],
        ),
        migrations.CreateModel(
            name='TaskParamName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('param', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(max_length=64)),
                ('target', models.CharField(max_length=64)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.State')),
            ],
        ),
        migrations.CreateModel(
            name='TransitionAssign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(max_length=64)),
                ('target', models.CharField(max_length=64)),
                ('transition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.Transition')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('brole', models.CharField(max_length=64)),
                ('principle_method', models.CharField(max_length=64)),
                ('principle_distributor', models.CharField(max_length=64)),
                ('callback_on', models.CharField(max_length=64)),
                ('callback_event', models.CharField(max_length=64)),
                ('documentation', models.CharField(max_length=256)),
                ('bussiness_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.BusinessObject')),
            ],
        ),
        migrations.CreateModel(
            name='Send',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(max_length=64)),
                ('stype', models.CharField(max_length=64)),
                ('messageMode', models.CharField(max_length=64)),
                ('transition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.Transition')),
            ],
        ),
        migrations.CreateModel(
            name='NewboParam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('expr', models.CharField(max_length=64)),
                ('newbo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.Transition')),
            ],
        ),
        migrations.CreateModel(
            name='Newbo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.CharField(max_length=64)),
                ('instancesExpr', models.CharField(max_length=64)),
                ('transition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.Transition')),
            ],
        ),
        migrations.CreateModel(
            name='ExitAssign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=64)),
                ('expr', models.CharField(max_length=64)),
                ('exit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.Exit')),
            ],
        ),
        migrations.CreateModel(
            name='EntryAssign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=64)),
                ('expr', models.CharField(max_length=64)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.Entry')),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('data_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('expr', models.CharField(max_length=64)),
                ('bussiness_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.BusinessObject')),
            ],
        ),
        migrations.CreateModel(
            name='CallParam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('expr', models.CharField(max_length=64)),
                ('call', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.Call')),
            ],
        ),
        migrations.AddField(
            model_name='call',
            name='transition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.Transition'),
        ),
    ]
