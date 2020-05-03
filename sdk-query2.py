#!/usr/bin/env python
###################################################################################
#                           Written by Wei, Hang                                  #
#                          weihang_hank@gmail.com                                 #
###################################################################################
"""
If you are looking for a few useful Mo Query functions, look here
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

# create a session
requests.packages.urllib3.disable_warnings()

ls = cobra.mit.session.LoginSession(URL, LOGIN, PASSWORD)
md = cobra.mit.access.MoDirectory(ls)
md.login()


def Query_Objs(class_name, wcard_str):
    """
    This function is to return object list that matches the classname and wcard str
    """
    class_query = cobra.mit.request.ClassQuery(class_name)
    class_query.propFilter = 'wcard({}.dn, "{}")'.format(class_name, wcard_str)
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
    This function is to return bdname
    """
    objs = Query_Objs("fvRsBd", "uni/tn-{}/ap-{}/epg-{}".format(_tenant, _aprofile, _epg))
    return objs[0].tnFvBDName

def get_VMM(_tenant, _aprofile, _epg):
    objs = Query_Objs("fvRsDomAtt", "uni/tn-{}/ap-{}/epg-{}".format(_tenant, _aprofile, _epg))
    return objs[0].tDn

def official_scoping(_tenant):
    """
    This function is using officially scoping method to return a obj list
    """
    app_query = cobra.mit.request.DnQuery('uni/tn-'+_tenant)
    app_query.queryTarget = 'children'
    # app_query.queryTarget = 'subtree'
    app_query.classFilter = 'fvAp'
    app_query.subtreeInclude = 'health'
    # app_query.subtreeInclude = 'health,stats'
    # app_query.subtree = 'full'

    apps = md.query(app_query)

    health_dict = {}

    for app in apps:
        # print(app.dn)
        for health in app.children:
            health_dict[app.name] = int(health.cur)
            # health_dict[app.name] = health.cur
            # print(health.__dict__)
    return health_dict


def main():
    # print(get_VMM("hangwe-tn", "hangwe-useg-ap", "cback-epg"))
    # print(get_BDname("hangwe-tn", "hangwe-useg-ap", "cback-epg"))
    # test_input("hangwe-tn", "hangwe-useg-ap", "cback-epg")
    # print(get_tenant_list())
    # print(get_ap_list("hangwe-tn"))
    # print(get_epg_list("hangwe-tn", "hangwe-useg-ap"))

    # get_ap_list("hangwe-tn")
    # objs = Query_Objs("fvAp", "tn-hangwe-tn")
    # objs = official_scoping('hangwe-tn')
    # for obj in objs:
    #     print(obj.dn)
    print(official_scoping('hangwe-tn'))
    # official_scoping('hangwe-tn')

if __name__ == '__main__':
    main()
