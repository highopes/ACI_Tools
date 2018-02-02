# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.draw
import cobra.model.fv
import cobra.model.pol
import cobra.model.vz
from cobra.internal.codec.xmlcodec import toXMLStr

#eliminate the warning message
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession('https://10.75.53.131', 'admin', 'Nbv!2345')
md = cobra.mit.access.MoDirectory(ls)
md.login()

# the top level object on which operations will be made
polUni = cobra.model.pol.Uni('')

# build the request using cobra syntax
fvTenant = cobra.model.fv.Tenant(polUni, ownerKey='', name='hangwe-apitest', descr='', ownerTag='')
vzBrCP = cobra.model.vz.BrCP(fvTenant, ownerKey='', name='CTR-hangwe-web2app', descr='', targetDscp='unspecified', ownerTag='', prio='unspecified')
vzSubj = cobra.model.vz.Subj(vzBrCP, revFltPorts='yes', name='Subject', prio='unspecified', targetDscp='unspecified', descr='', consMatchT='AtleastOne', provMatchT='AtleastOne')
vzRsSubjFiltAtt = cobra.model.vz.RsSubjFiltAtt(vzSubj, tnVzFilterName='default')
vzBrCP2 = cobra.model.vz.BrCP(fvTenant, ownerKey='', name='CTR-hangwe-app2db', descr='', targetDscp='unspecified', ownerTag='', prio='unspecified')
vzSubj2 = cobra.model.vz.Subj(vzBrCP2, revFltPorts='yes', name='Subject', prio='unspecified', targetDscp='unspecified', descr='', consMatchT='AtleastOne', provMatchT='AtleastOne')
vzRsSubjFiltAtt2 = cobra.model.vz.RsSubjFiltAtt(vzSubj2, tnVzFilterName='default')
drawCont = cobra.model.draw.Cont(fvTenant)
drawInst = cobra.model.draw.Inst(drawCont, info="{'{fvAp/epg}-{EPG-hangwe-web}':{'x':714.5,'y':333.5},'{fvAp/epg}-{EPG-hangwe-app}':{'x':834.5,'y':333.5},'{fvAp/epg}-{EPG-hangwe-db}':{'x':954.5,'y':333.5},'{fvAp/contract}-{CTR-hangwe-app2db}':{'x':1041.5,'y':10},'{fvAp/contract}-{CTR-hangwe-web2app}':{'x':921.5,'y':10}}", oDn='uni/tn-hangwe-apitest/ap-ANP-hangwe-test01')
fvCtx = cobra.model.fv.Ctx(fvTenant, ownerKey='', name='VRF-hangwe-all', descr='', knwMcastAct='permit', pcEnfDir='ingress', ownerTag='', pcEnfPref='enforced')
fvRsCtxToExtRouteTagPol = cobra.model.fv.RsCtxToExtRouteTagPol(fvCtx, tnL3extRouteTagPolName='')
fvRsBgpCtxPol = cobra.model.fv.RsBgpCtxPol(fvCtx, tnBgpCtxPolName='')
vzAny = cobra.model.vz.Any(fvCtx, matchT='AtleastOne', name='', descr='')
fvRsOspfCtxPol = cobra.model.fv.RsOspfCtxPol(fvCtx, tnOspfCtxPolName='')
fvRsCtxToEpRet = cobra.model.fv.RsCtxToEpRet(fvCtx, tnFvEpRetPolName='')
fvBD = cobra.model.fv.BD(fvTenant, ownerKey='', vmac='not-applicable', name='BD-hangwe-all', descr='', arpFlood='no', unkMacUcastAct='proxy', multiDstPktAct='bd-flood', limitIpLearnToSubnets='yes', llAddr='::', mac='00:22:BD:F8:19:FF', epMoveDetectMode='', unicastRoute='yes', ownerTag='', unkMcastAct='flood')
fvRsBDToNdP = cobra.model.fv.RsBDToNdP(fvBD, tnNdIfPolName='')
fvRsCtx = cobra.model.fv.RsCtx(fvBD, tnFvCtxName='VRF-hangwe-all')
fvRsIgmpsn = cobra.model.fv.RsIgmpsn(fvBD, tnIgmpSnoopPolName='')
fvSubnet = cobra.model.fv.Subnet(fvBD, name='', descr='', ctrl='', ip='201.1.32.1/24', preferred='no', virtual='no')
fvSubnet2 = cobra.model.fv.Subnet(fvBD, name='', descr='', ctrl='', ip='202.1.32.1/24', preferred='no', virtual='no')
fvRsABDPolMonPol = cobra.model.fv.RsABDPolMonPol(fvBD, tnMonEPGPolName='default')
fvRsBdToEpRet = cobra.model.fv.RsBdToEpRet(fvBD, resolveAct='resolve', tnFvEpRetPolName='')
fvRsTenantMonPol = cobra.model.fv.RsTenantMonPol(fvTenant, tnMonEPGPolName='default')
fvAp = cobra.model.fv.Ap(fvTenant, ownerKey='', prio='unspecified', name='ANP-hangwe-test01', descr='', ownerTag='')
fvRsApMonPol = cobra.model.fv.RsApMonPol(fvAp, tnMonEPGPolName='default')
fvAEPg = cobra.model.fv.AEPg(fvAp, isAttrBasedEPg='no', matchT='AtleastOne', name='EPG-hangwe-app', prio='unspecified', descr='', pcEnfPref='unenforced')
fvRsCons = cobra.model.fv.RsCons(fvAEPg, tnVzBrCPName='CTR-hangwe-app2db', prio='unspecified')
fvRsCustQosPol = cobra.model.fv.RsCustQosPol(fvAEPg, tnQosCustomPolName='')
fvRsBd = cobra.model.fv.RsBd(fvAEPg, tnFvBDName='BD-hangwe-all')
fvRsProv = cobra.model.fv.RsProv(fvAEPg, tnVzBrCPName='CTR-hangwe-web2app', matchT='AtleastOne', prio='unspecified')
fvAEPg2 = cobra.model.fv.AEPg(fvAp, isAttrBasedEPg='no', matchT='AtleastOne', name='EPG-hangwe-db', prio='unspecified', descr='', pcEnfPref='unenforced')
fvRsCustQosPol2 = cobra.model.fv.RsCustQosPol(fvAEPg2, tnQosCustomPolName='')
fvRsBd2 = cobra.model.fv.RsBd(fvAEPg2, tnFvBDName='BD-hangwe-all')
fvRsProv2 = cobra.model.fv.RsProv(fvAEPg2, tnVzBrCPName='CTR-hangwe-app2db', matchT='AtleastOne', prio='unspecified')
fvAEPg3 = cobra.model.fv.AEPg(fvAp, isAttrBasedEPg='no', matchT='AtleastOne', name='EPG-hangwe-web', prio='unspecified', descr='', pcEnfPref='unenforced')
fvRsCons2 = cobra.model.fv.RsCons(fvAEPg3, tnVzBrCPName='CTR-hangwe-web2app', prio='unspecified')
fvRsCustQosPol3 = cobra.model.fv.RsCustQosPol(fvAEPg3, tnQosCustomPolName='')
fvRsBd3 = cobra.model.fv.RsBd(fvAEPg3, tnFvBDName='BD-hangwe-all')


# commit the generated code to APIC
# print toXMLStr(polUni)
c = cobra.mit.request.ConfigRequest()
c.addMo(fvTenant)
md.commit(c)
