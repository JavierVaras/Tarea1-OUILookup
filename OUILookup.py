from getmac import get_mac_address
import subprocess
import getopt
import sys
import os 

def main():
	try:
		options, args = getopt.getopt(sys.argv[1:],"i:m:", ["ip=", "mac="])
	except:
		print("Error: parametros incorrectos")
		uso()
	install = subprocess.call(["pip", "install", "getmac"])
	IP=None
	MAC=None
	for opt, arg in options:
		if(opt in ('--ip')):
			IP=arg
		elif(opt in('--mac')):
			MAC=arg

	if(IP == None and MAC == None):
		print("Error: Faltan parametros.")
		uso()

	#Si ingresa al programa con la opcion --ip	
	if(IP!=None):
		if(check_ip(IP)):
			ip_a_mac=get_mac_address(ip=IP)
			print(ip_a_mac)
			if(ip_a_mac!=None):
				print("MAC address: ",ip_a_mac)
				print("Fabricante: ", consultarFabricante(ip_a_mac))
			else:
				print("\nError: la ip no se encuentra dentro de la red.")
				exit(1)

		else:
			print("\nError: La ip ingresada no es valida.")
			exit(1)
	
	#Si ingresa al programa con la opcion --mac
	if(MAC!=None):
		print("MAC address:",MAC)
		if(MAC.count('-')>0):
			MAC=MAC.replace('-',':')
			print(MAC)
		if(consultarFabricante(MAC)!=None):
			print("Fabricante:",consultarFabricante(MAC))
		else:
			print("Fabriacante: Not found.")


def check_ip(ip):
	try:
		ip_concatenada = ip.split('.')
		validar=0
		for i in ip_concatenada:
			if int(i) >=0 and int(i) <=255:
				validar+=1
		if(validar==4):
			return True	
		else:
			return False
				
	except:
		return False

def consultarFabricante(direccionMAC):
	if(os.path.isfile("OUI.txt")==False):
		print("Dercargando OUI.txt..")
		os.system('curl https://gitlab.com/wireshark/wireshark/-/raw/master/manuf >OUI.txt')
	archivo =  open('OUI.txt', 'r', encoding='utf-8')
	respuesta=""
	for linea in archivo:
		if(linea[0]=='#'):
			continue
		cambiar=""		#Aqui solo hay ajustes para leer el documento "OUI.txt"
		cambio=[]
		for w in linea:
			if(w!=" "):
				cambiar=cambiar+w
			if(w==" " or w=="\t"):
				if(len(cambio)==3):
					cambio[2]=cambio[2]+" "+cambiar
				else:
					cambio.append(cambiar)
				cambio=[c.replace("\t","") for c in cambio]
				cambiar=""
		if(len(cambio)>1):
			if(cambio[0][len(cambio[0])-3])=="/":
				continue
			if(direccionMAC.upper()==cambio[0] or direccionMAC.upper().find(cambio[0])==0):
				respuesta=cambio[2]
				return respuesta
				break

def uso():
    print("Formas de uso")
    print(" Consulta con ip:")
    print("     ",sys.argv[0],"--ip <Ip>")
    print("\n Consulta con Mac address:")
    print("     ",sys.argv[0],"--mac <Mac address>")
    exit(1)


if __name__ == '__main__':
    main()
    
