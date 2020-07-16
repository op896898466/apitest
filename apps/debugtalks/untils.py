from debugtalks.models import DebugTalks
from projects.models import Projects


def get_projects(datas):
    datas_list = []
    for item in datas:
        projects = DebugTalks.objects.get(id=item["id"]).projects.all()
        if projects:
            item["project"] = "，".join([project.name for project in projects])
        else:
            item["project"] = "无所属项目"
        datas_list.append(item)
    return datas_list
