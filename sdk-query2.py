#!/usr/bin/env python
###################################################################################
#                           Written by Wei, Hang                                  #
#                          weihang_hank@gmail.com                                 #
###################################################################################
"""
This is a sample program for educational purposes ---- SDK Query section
"""
import cobra.mit.access
import cobra.mit.session
import cobra.mit.request
import cobra.model.pol
import cobra.model.fv
import cobra.model.vmm
import requests
import os
from credentials import *
from cobra.internal.codec.jsoncodec import toJSONStr

# create a session
requests.packages.urllib3.disable_warnings()

ls = cobra.mit.session.LoginSession(URL, LOGIN, PASSWORD)
md = cobra.mit.access.MoDirectory(ls)
md.login()


# blocking = input("process is blocking\n")
# print("input is " + blocking + "\n\n")


def Query_Objs(class_name, wcard_str):
    """
    This function is to return object list that matches the classname and wcard str
    """
    class_query = cobra.mit.request.ClassQuery(class_name)
    class_query.propFilter = 'wcard({}.dn, "{}")'.format(class_name, wcard_str)
    # class_query.subtree = "full"
    # class_query.queryTarget = "subtree"
    # class_query.queryTarget = "children"

    return md.query(class_query)


def get_tenant_list():
    """
    This function is to build query for existing tenants
    """
    tenants = Query_Objs("fvTenant", "tn")
    tn_list = [""]
    for tn in tenants:
        tn_list.append(tn.name)
    return tn_list


def get_ap_list(_tenant):
    aps = Query_Objs("fvAp", _tenant)
    ap_list = [""]
    for ap in aps:
        ap_list.append(ap.name)
    return ap_list


def get_epg_list(_tenant, _approfile):
    """

    """
    epgs = Query_Objs("fvAEPg", "tn-" + _tenant + "/ap-" + _approfile)
    epg_list = [""]
    for epg in epgs:
        epg_list.append(epg.name)
        # print(epg.dn)
    return epg_list


def test_input(_tenant, _aprofile, _epg):
    """
     This function is to return certain epg's existence
     """
    dn_query = cobra.mit.request.DnQuery("uni/tn-{}/ap-{}/epg-{}".format(_tenant, _aprofile, _epg))
    obj_list = md.query(dn_query)
    print(obj_list[0].dn)
    if obj_list:
        print("YES!!! It's here!!!!")
    else:
        print("It doesn't exist!!")


def get_BDname(_tenant, _aprofile, _epg):
    """
    This function is to return EPG's BD name
    """
    objs = Query_Objs("fvRsBd", "uni/tn-{}/ap-{}/epg-{}".format(_tenant, _aprofile, _epg))
    return objs[0].tnFvBDName


def get_VMM(_tenant, _aprofile, _epg):
    """
    This function is to return EPG's VMM Domain's Dn (Only return the first one)
    """
    objs = Query_Objs("fvRsDomAtt", "uni/tn-{}/ap-{}/epg-{}".format(_tenant, _aprofile, _epg))
    return objs[0].tDn


def ap_health(_tenant):
    """
    This function is using general query scoping method to return App Profiles and their Health Scores
    """
    ap_query = cobra.mit.request.DnQuery('uni/tn-' + _tenant)
    ap_query.queryTarget = 'children'
    # app_query.queryTarget = 'subtree'
    ap_query.classFilter = 'fvAp'
    ap_query.subtreeInclude = 'health'
    # ap_query.subtreeInclude = 'health,stats'

    aps = md.query(ap_query)

    health_dict = {}

    for ap in aps:
        for health in ap.children:
            health_dict[ap.name] = int(health.cur)

    return health_dict


def test_config(_obj):
    """
    This function is for test config
    """
    _newobj = cobra.model.fv.Ap(_obj, name="rogue_Ap", descr=u"test 8:57")
    c = cobra.mit.request.ConfigRequest()
    c.addMo(_obj)
    md.commit(c)
    return _newobj


def test_del(_obj):
    """
    This function is for test config
    """
    print(_obj.name)
    _obj.delete()
    c = cobra.mit.request.ConfigRequest()
    c.addMo(_obj)
    md.commit(c)


def print_json(_objs):
    """
    This function is to print objs
    """
    for _obj in _objs:
        print(toJSONStr(_obj))


def main():
    # ACI Program Training:   General Query method, and query health score
    print(ap_health('hangwe-tn'))

    # # ACI Program Training:   Query by DN wildcard filter
    # print_json(Query_Objs("fvTenant", "hangwe"))

    # # ACI Program Training:   Query Rs... Mo
    # print("The BD Name is " + get_BDname("hangwe-tn", "hangwe-outside-ap", "hangwe-DB-epg"))
    # print("The 1st VMM Domain DN is " + get_VMM("hangwe-tn", "hangwe-outside-ap", "hangwe-web-epg"))

    # # Config a Mo, but instead of building its father, querying its father
    # aps = Query_Objs("fvAp", "uni/tn-hangwe-rogue/")
    # print(toJSONStr(aps[0]))
    # tns = Query_Objs("fvTenant", "uni/tn-hangwe-rogue")
    # newobj = test_config(tns[0])
    # print(toJSONStr(newobj))

    # # Config a Mo, do not build anything, all by querying and modified its property
    # aps = Query_Objs("fvAp", "uni/tn-hangwe-rogue/")
    # print(toJSONStr(aps[0]))
    # aps[0].descr = u"test 9:17"
    # c = cobra.mit.request.ConfigRequest()
    # c.addMo(aps[0])
    # md.commit(c)
    # print(toJSONStr(aps[0]))

    # # toJSONStr can only print properties that necessary, but all properties inherent from Class still exist
    # aps = Query_Objs("fvAp", "uni/tn-company01-hangwe/")
    # print(toJSONStr(aps[0]))
    # print("dn = " + str(aps[0].dn))
    # print("modTs = " + aps[0].modTs)

    # # Other Testing
    # test_input("hangwe-tn", "hangwe-useg-ap", "cback-epg")
    # print(get_tenant_list())
    # print(get_ap_list("hangwe-tn"))
    # print(get_epg_list("hangwe-tn", "hangwe-useg-ap"))

    # get_ap_list("hangwe-tn")
    # objs = Query_Objs("fvTenant", "uni/tn-hangwe-tn")

    # newobj = test_config(objs[0])

    # test_del(objs[0])
    # objs = official_scoping('hangwe-tn')
    # for obj in objs:
    #     print(obj.dn)

    # official_scoping('hangwe-tn')


if __name__ == '__main__':
    main()
