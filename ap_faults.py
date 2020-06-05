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
# from credentials import *
from cobra.internal.codec.jsoncodec import toJSONStr

URL = 'https://sandboxapicdc.cisco.com'
LOGIN = 'admin'
PASSWORD = 'ciscopsdt'

# create a session
requests.packages.urllib3.disable_warnings()


def print_json(_objs):
    """
    This function is to print objs
    """
    for _obj in _objs:
        # print(toJSONStr(_obj))
        print(_obj.dn)


def get_faults(app_name):
    session = aci_login()

    fault_query = cobra.mit.request.DnQuery('uni/tn-SnV/ap-{}'.format(app_name))
    fault_query.queryTarget = 'subtree'
    fault_query.subtreeInclude = 'faults,no-scoped'
    # fault_query.queryTarget = 'children'
    # fault_query.subtreeInclude = 'faults'

    fault_query.orderBy = 'faultInfo.severity|desc'
    fault_query.page = 0
    fault_query.pageSize = 15

    faults = session.query(fault_query)
    print_json(faults)
    print("==============================\n\n\n")
    faults_dict = {'faults': []}

    for fault in faults:
        if fault.lc == 'retaining':
            fault_dict = {
                'Acknowledged': fault.ack,
                'Affected': 'Issue No Longer Exists',
                'Description': fault.descr,
                'Time': fault.created,
                'Life Cycle': fault.lc
            }
        else:
            fault_dict = {
                'Acknowledged': fault.ack,
                'Affected': fault.affected,
                'Description': fault.descr,
                'Time': fault.created,
                'Life Cycle': fault.lc
            }

        faults_dict['faults'].append(fault_dict)

    return faults_dict


def aci_login():
    ls = cobra.mit.session.LoginSession(URL, LOGIN, PASSWORD)
    md = cobra.mit.access.MoDirectory(ls)
    md.login()

    return md


def main():
    print(get_faults("Chaos"))


if __name__ == '__main__':
    main()
