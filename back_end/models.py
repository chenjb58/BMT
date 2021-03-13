from django.db import models


# Create your models here.
class BussinessObject(models.Model):
    version = models.CharField(max_length=32)
    name = models.CharField(max_length=64, primary_key=True)
    initial = models.CharField(max_length=64)
    xmlns = models.CharField(max_length=128)
    # datamodel = models.ManyToManyField("Data")
    # operations = models.ManyToManyField("Task")
    # lifecycle = models.ManyToManyField("State")


class Data(models.Model):
    data_id = models.CharField(max_length=64, primary_key=True)
    expr = models.CharField(max_length=64)
    bussiness_object = models.ForeignKey("BussinessObject", on_delete=models.CASCADE)


class Task(models.Model):
    task_id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64)
    brole = models.CharField(max_length=64)
    principle_method = models.CharField(max_length=64)
    principle_distributor = models.CharField(max_length=64)
    callback_on = models.CharField(max_length=64)
    callback_event = models.CharField(max_length=64)
    documentation = models.CharField(max_length=256)
    bussiness_object = models.ForeignKey("BussinessObject", on_delete=models.CASCADE)


class TaskParam(models.Model):
    name = models.CharField(max_length=64)
    task = models.ForeignKey("Task", on_delete=models.CASCADE)


class State(models.Model):
    state_id = models.CharField(max_length=64, primary_key=True)
    is_initial = models.BooleanField()
    is_final = models.BooleanField()
    onentry = models.OneToOneField("Entry", on_delete=models.CASCADE)
    onexit = models.OneToOneField("Exit", on_delete=models.CASCADE)
    # tansitions = models.ManyToManyField("Transition")
    bussiness_object = models.ForeignKey("BussinessObject", on_delete=models.CASCADE)


class Entry(models.Model):
    log_label = models.CharField(max_length=64)
    log_expr = models.CharField(max_length=64)
    # assigns = models.ManyToManyField("EntryAssign")


class Exit(models.Model):
    log_label = models.CharField(max_length=64)
    log_expr = models.CharField(max_length=64)
    # assigns = models.ManyToManyField("ExitAssign")


class EntryAssign(models.Model):
    location = models.CharField(max_length=64)
    expr = models.CharField(max_length=64)
    entry = models.ForeignKey("Entry", on_delete=models.CASCADE)


class ExitAssign(models.Model):
    location = models.CharField(max_length=64)
    expr = models.CharField(max_length=64)
    exit = models.ForeignKey("Exit", on_delete=models.CASCADE)


class Transition(models.Model):
    event = models.CharField(max_length=64)
    target = models.CharField(max_length=64)
    # calls = models.ManyToManyField("TransitionCall")
    # assigns = models.ManyToManyField("TransitionAssign")
    # newbos = models.ManyToManyField("Newbo")
    # sends = models.ManyToManyField("Send")
    state = models.ForeignKey("State", on_delete=models.CASCADE)


class TransitionAssign(models.Model):
    event = models.CharField(max_length=64)
    target = models.CharField(max_length=64)
    transition = models.ForeignKey("Transition", on_delete=models.CASCADE)


class Call(models.Model):
    name = models.CharField(max_length=64)
    instancesExpr = models.CharField(max_length=64)
    # params = models.ManyToManyField("CallParam")
    transition = models.ForeignKey("Transition", on_delete=models.CASCADE)


class CallParam(models.Model):
    name = models.CharField(max_length=64)
    expr = models.CharField(max_length=64)
    call = models.ForeignKey("Call", on_delete=models.CASCADE)


class Newbo(models.Model):
    src = models.CharField(max_length=64)
    instancesExpr = models.CharField(max_length=64)
    # params = models.ManyToManyField("NewboParam")
    transition = models.ForeignKey("Transition", on_delete=models.CASCADE)


class NewboParam(models.Model):
    name = models.CharField(max_length=64)
    expr = models.CharField(max_length=64)
    newbo = models.ForeignKey("Transition", on_delete=models.CASCADE)


class Send(models.Model):
    event = models.CharField(max_length=64)
    stype = models.CharField(max_length=64)
    messageMode = models.CharField(max_length=64)
    transition = models.ForeignKey("Transition", on_delete=models.CASCADE)
