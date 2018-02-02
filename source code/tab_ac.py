# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.draw
import cobra.model.fv
import cobra.model.pol
import cobra.model.vz
from cobra.internal.codec.xmlcodec import toXMLStr
from tabulate import tabulate

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
 

def table(i): 

# It's an Atomic Counter viewer app
# log into an APIC and create a directory object
  ls = cobra.mit.session.LoginSession('https://10.75.53.131', 'admin', 'Nbv!2345')
  md = cobra.mit.access.MoDirectory(ls)
  md.login()   


  clAcPath = cobra.mit.access.ClassQuery('dbgAcPath')
  
  dbgAcPathA_objlist = md.query(clAcPath)
  dbgAclist = []

  for mo in dbgAcPathA_objlist:
#      if int(mo.dropPkt) !=0:
       row = {   
           "Path":mo.dn,    
           "DropPackets":mo.dropPkt,    
           "DropPacketsPercentage":mo.dropPktPercentage,    
#           "ExcessPakets":mo.excessPkt,    
#           "ExcessPaketsPercentage":mo.excessPktPercentage,    
#           "TransceivePakets":mo.txPkt,    
#           "ReceivePakets":mo.rxPkt,    
#           "TotalDropPackets":mo.totDropPkt,    
#           "TotalDropPacketsPercentage":mo.totDropPktPercentage,
       }
       dbgAclist.append(row)
  print tabulate(sorted(dbgAclist,),tablefmt='grid',headers="keys")
  return





def main():
#   for i in range (1,2):       
#	if i <= 2:        
#           time.sleep(5)
#	y = i + 1      
	table(1)



if __name__ == '__main__':
  main()

