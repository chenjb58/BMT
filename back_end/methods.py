from back_end import models


# from rest_framework.views import APIView
# from rest_framework.response import Response
# Create your views here.

# 新建业务对象
def addBussinessObject(b_version, b_name, b_initial, b_xmlns):
    newb = models.BussinessObject(version=b_version, name=b_name, initial=b_initial, xmlns=b_xmlns)
    newb.save()


# 新建任务
def addTask(t_id, t_name, t_brole, p_method, p_distributor, c_on, c_event, t_doc, b_id):
    task = models.Task.objects.create(task_id=t_id, name=t_name, brole=t_brole, principle_method=p_method,
                                      principle_distributor=p_distributor, callback_on=c_on, callback_event=c_event,
                                      documentation=t_doc, bussiness_object_id=b_id)
    task.save()
    # newt = models.Task(task_id=t_id, name=t_name, brole=t_brole, principle_method=p_method,principle_distributor=p_distributor,callback_on=c_on,callback_event=c_event,documentation=t_doc)


# newt.save()

# 新建任务参数
def addTaskParam(p_name, t_id):
    # task = models.Task.objects.filter(pk=t_id).first()
    param = models.TaskParam.objects.create(name=p_name, task_id=t_id)
    param.save()


# 添加状态
def addState(s_id, is_ini=False, is_fin=False):
    state = models.State.objects.create(state_id=s_id, is_initial=is_ini, is_fin=is_fin)
    state.save()


# 添加State的onentry标签
def addOnEntry(l_label, l_expr, s_id):
    s = models.State.objects.filter(pk=s_id).first()
    entry = models.Entry.objects.create(log_label=l_label, log_expr=l_expr, state=s)
    entry.save()


def addEntryAssign(ea_location, ea_expr, entry_obj):
    ea = models.EntryAssign.objects.create(location=ea_location, expr=ea_expr, entry_id=entry_obj.pk)
    ea.save()


# 添加State的onexit标签
def addOnExit(l_label, l_expr, s_id):
    s = models.State.objects.filter(pk=s_id).first()
    exit = models.Exit.objects.create(log_label=l_label, log_expr=l_expr, state=s)
    exit.save()


def addEntryAssign(ea_location, ea_expr, exit_obj):
    ea = models.ExitAssign.objects.create(location=ea_location, expr=ea_expr, entry_id=exit_obj.pk)
    ea.save()


def addTransition(t_event, t_target, s_id):
    transition = models.Transition.objects.create(event=t_event, target=t_target, state_id=s_id)
    transition.save()


def addTransitionAssign(ta_location, ta_expr, transition_obj):
    assign = models.TransitionAssign.objects.create(location=ta_location, expr=ta_location,
                                                    transition_id=transition_obj.pk)
    assign.save()


def addNewbo(n_src, n_ins, transition_obj):
    newbo = models.Newbo.objects.create(src=n_src, instancesExpr=n_ins, transition_id=transition_obj.pk)
    newbo.save()


def addNewboParam(p_name, p_expr, newbo_obj):
    nbp = models.NewboParam.objects.create(name=p_name, expr=p_expr, newbo_id=newbo_obj.pk)
    nbp.save()


def addSend(s_event, s_type, s_messagemode, transition_obj):
    send = models.Send.objects.create(event=s_event, stype=s_type, messageMode=s_messagemode,transition_id=transition_obj.pk)
    send.save()


def addCall(c_name, c_expr, transition_obj):
    call = models.Call.objects.create(name=c_name, expr=c_expr, transition_id=transition_obj.pk)


def addCallParam(p_name, p_expr, call_obj):
    param = models.CallParam.objects.create(name=p_name, expr=p_expr, call_id=call_obj.pk)
    param.save()


from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import ElementTree

from xml.dom import minidom


def generateXML(bussinessobject_id):
    bussinessobject = models.BussinessObject.objects.filter(pd=bussinessobject_id).first()
    root = Element("businessclass",
                   dict(version=bussinessobject.version, name=bussinessobject.name, xmlns=bussinessobject.xmlns))
    datas = bussinessobject.data_set.all()
    data_num = len(datas)
    if data_num > 0:
        datamodel = SubElement(root, "datamodel")
        for data in datas:
            SubElement(datamodel, "data", dict(id=data.data_id, expr=data.expr))
    tasks = bussinessobject.task_set.all()
    if len(tasks) > 0:
        operations = SubElement(root, "operations")
        for task in tasks:
            tmp_task_node = SubElement(operations, "task", dict(id=task.task_id, name=task.name, brole=task.brole))
            SubElement(tmp_task_node, "principle",
                       dict(method=task.principle_method, distributor=task.principle_distributor))
            SubElement(tmp_task_node, "callback", dict(on=task.callback_on, event=task.callback_event))
            doc_node = SubElement(tmp_task_node, "documentation")
            doc_node.text = task.documentation
            params = task.taskparam_set.all()
            if len(params) > 0:
                for param in params:
                    SubElement(tmp_task_node, "param", dict(name=param.name))
    init_state = bussinessobject.state_set.filter(is_initial=True).first()
    init_node = SubElement(root,"state",dict(id=init_state.state_id))
    init_entry = init_state.onentry
    init_exit = init_state.onexit
    init_transitions = init_state.transition_set.all()
    init_entry_node = SubElement(init_node,"onentry")
    SubElement(init_entry_node,"log",dict(label=init_entry.log_label, expr=init_entry.log_expr))
    entry_assigns = init_entry.entryassign_set.all()
    if len(entry_assigns) > 0:
        for assign in entry_assigns:
            SubElement(init_entry_node,"param",dict(location=assign.location, expr=assign.expr))
    if len(init_transitions) > 0:
        for transition in init_transitions:
            SubElement(init_node,"transition",dict(event=transition.event, target=transition.target))

    init_exit_node = SubElement(root, "state", dict(id=init_state.state_id))
    SubElement(init_exit_node, "log", dict(label=init_exit.log_label, expr=init_exit.log_expr))
    entry_assigns = init_exit.entryassign_set.all()
    if len(entry_assigns) > 0:
        for assign in entry_assigns:
            SubElement(init_exit, "param", dict(location=assign.location, expr=assign.expr))


    final_state = bussinessobject.state_set.filter(is_final=True).first()
    final_node = SubElement(root, "state", dict(id=init_state.state_id))
    final_entry = final_state.onentry
    final_exit = final_state.onexit
    final_transitions = final_state.transition_set.all()
    final_entry_node = SubElement(final_node, "onexit")
    SubElement(final_entry_node, "log", dict(label=final_entry.log_label, expr=final_entry.log_expr))
    entry_assigns = final_entry.entryassign_set.all()
    if len(entry_assigns) > 0:
        for assign in entry_assigns:
            SubElement(init_entry_node, "param", dict(location=assign.location, expr=assign.expr))




# elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
def prettyXml(element, indent, newline, level=0):
    # 判断element是否有子元素
    if element:
        # 如果element的text没有内容
        if element.text == None or element.text.isspace():
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
    # 此处两行如果把注释去掉，Element的text也会另起一行
    # else:
    # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将elemnt转成list
    for subelement in temp:
        # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
        if temp.index(subelement) < (len(temp) - 1):
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        # 对子元素进行递归操作
        prettyXml(subelement, indent, newline, level=level + 1)
