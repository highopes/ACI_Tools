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


def Query_Objs(class_name, wcard_str):
    """
    This function is to return object list that matches the classname and wcard str
    """
    class_query = cobra.mit.request.ClassQuery(class_name)
    class_query.propFilter = 'wcard({}.dn, "{}")'.format(class_name, wcard_str)
    # class_query.subtree = "full"
    # class_query.queryTarget = "subtree"

    return md.query(class_query)


def main():
    print_json(Query_Objs("fvAEPg", "hangwe-tn"))


if __name__ == '__main__':
    main()
