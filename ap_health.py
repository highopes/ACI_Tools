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
from cobra.internal.codec.jsoncodec import toJSONStr

# create a session
requests.packages.urllib3.disable_warnings()

ls = cobra.mit.session.LoginSession(URL, LOGIN, PASSWORD)
md = cobra.mit.access.MoDirectory(ls)
md.login()


def print_json(_objs):
    """
    This function is to print objs
    """
    for _obj in _objs:
        print(toJSONStr(_obj))


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
        # print_json(ap.children)
        for health in ap.children:
            health_dict[ap.name] = int(health.cur)

    return health_dict


def main():
    print(ap_health('hangwe-tn'))


if __name__ == '__main__':
    main()
