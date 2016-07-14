import urllib,re
import urllib2
from bs4 import BeautifulSoup
import json
import webbrowser

url="http://10.141.2.20:8080/cgi-bin/alarmas.cgi"
req=urllib2.Request(url)
response=urllib2.urlopen(req)
page=response.read()

celdas_A6=['0101AV','0101AV','0204VA','0204VA','0204VA','0205VA','0205VA','0306SG','0306SG','0316AV','0316AV','0320VA','0320VA','0324VA','0324VA','1025LE','1025LE','1025LE','1031LE','1031LE','1031LE','AV05WU','AV05WU','LE14RU','LE14RU','LE14RU','LE41RU','LE41RU','LE41RU','SG06WU','SG06WU','SG16WU','SG16WU','VA01RU','VA01RU','VA01WU','VA01WU','VA01WU','VA02RU','VA02RU','VA02RU','VA03KU','VA03KU','VA03WU','VA03WU','VA03WU','VA04KU','VA04KU','VA07WU','VA07WU','VA54WU','VA54WU','ZA19RU','ZA19RU','ZA19RU']


cell_file = open("/home/pablo/cell.json","r")
cell_dict = json.load(cell_file)
def extrae_nombre(celda):
	name=cell_dict[celda]
	return name




soup = BeautifulSoup(page)
soup.prettify()

links= soup.find_all("td")


i=0

dial=[]
horal=[]
rncl=[]
celdal=[]
alarmal=[]
valorl=[]
repeticionesl=[]
cesadal=[]
nombrel=[]


for link in links:
	try:
		i=i+1
		#print link
		if (re.search("VA",str(link)) or re.search("LE",str(link)) or re.search("BU",str(link)) or re.search("SA",str(link)) or re.search("ZA",str(link)) or re.search("PX",str(link)) or re.search("SX",str(link))or re.search("NA",str(link))or re.search("LX",str(link)) or re.search("SO",str(link)) or re.search("SG",str(link)) or re.search("AV",str(link))) :
			dia=links[i-4]
		        dia=str(dia).replace("</td>","")
		        dia=dia.replace("<td>","")
		        hora=links[i-3]
		        hora=str(hora).replace("</td>","")
		        hora=hora.replace("<td>","")
		        rnc=links[i-2]
		        rnc=str(rnc).replace("</td>","")
		        rnc=rnc.replace("<td>","")
			celda=links[i-1]
		        celda=str(celda).replace("</td>","")
	       		celda=celda.replace("<td>","")
		        alarma=links[i]
		        alarma=str(alarma).replace("</td>","")
	        	alarma=alarma.replace("<td>","")
		        valor=links[i+1]
	        	valor=str(valor).replace("</td>","")
		        valor=valor.replace("<td>","")
		        repeticiones=links[i+3]
		        repeticiones=str(repeticiones).replace("</td>","")
		        repeticiones=repeticiones.replace("<td>","")
		        cesada=links[i+4]
		        cesada=str(cesada).replace("</td>","")
		        cesada=cesada.replace("<td>","")
		        nombre=extrae_nombre(celda)
			#print dia,hora,rnc,celda,nombre,alarma,valor,"REPETICIONES",repeticiones,cesada
		        dial.append(dia)
		        horal.append(hora)
	        	rncl.append(rnc)
	        	celdal.append(celda)
	        	nombrel.append(nombre)
	        	alarmal.append(alarma)
	        	valorl.append(valor)
	        	repeticionesl.append(repeticiones)
	        	cesadal.append(cesada)

	except:pass

cabecera = """<html> <head>
<meta http-equiv='refresh' content='30'>
</head>  <body> <h4>Alarmas</h4>
<table border="1">
<tr>
 <td>FECHA</td>
  <td>HORA</td>
  <td>RNC</td>
  <td>CELDA</td>
  <td>NOMBRE</td>
  <td>ALARMA</td>
  <td>VALOR</td>
  <td>REPETICIONES</td>
  <td>CESADA</td>
</tr>
"""

cuerpo=[]
cuerpot=""


for n in range(0,len(dial)):
    if celdal[n] in celdas_A6:nombrel[n]='<font color="red">'+nombrel[n]+'  *** CELDA A6  ***'+'</font>'	
    cuerpo.append("""
    <tr>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    </tr>
     """ %(dial[n],horal[n],rncl[n],celdal[n],nombrel[n],alarmal[n],valorl[n],repeticionesl[n],cesadal[n]))
    try:
    	cuerpo[n]=str(cuerpo[n])
    except: 
	pass


cuerpot="".join(cuerpo)

cuerpot=cuerpot.replace('\n','')
cuerpot=cuerpot.replace(', ','')

fin="</table> </body></html>"

web=cabecera+cuerpot+fin
print web

f = open('/var/www/html/alarmas.html','w')
f.write(web)
f.close()
#webbrowser.open_new_tab('/var/www/html/alarmas.html')


