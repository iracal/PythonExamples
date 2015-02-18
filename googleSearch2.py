
import urllib
import urllib2
import sys
from bs4 import BeautifulSoup
import urlparse 

listURLComplete=[]
listURLpartial=[]

myfile =open("output/c8.csv","w+")
myfile.close()


def converLinkObj(links,parent):
	listLinks=[]

	for url in links:
			if 'http' not in url['href'] :
				
				if(url['href'].count('/')>1):
					r3=url['href'].split('/')
					pattern=url['href'][:-len(r3[len(r3)-1])]
							
					if( pattern not in parent):
						listLinks.append(urlparse.urljoin(parent,url['href']))
						
			else:
				listLinks.append(url['href'])
	return listLinks



def calculo(url):
	try:
		
		r1=urlparse.urlsplit(url)
		if url not in listURLComplete and r1[2] not in listURLpartial:
			listURLComplete.append(url)
			if r1[2].count('/')>2:
				listURLpartial.append(r1[2])
			htmlfile= urllib.urlopen(url)
			htmltext=htmlfile.read()
			total=len(htmltext)
			soup = BeautifulSoup(htmltext)
			language =soup.find('html',lang=True)
			code =htmlfile.getcode()
			
			if(code<>200):
				return 0
			code=str(code)
			if language is not None:
				language=language['lang']
			else:
				language=''
			typeFile=htmlfile.info()['Content-Type']
			
			
			
			if urlRoot not in url:
				print(code, url,str(total),typeFile,language,'outer')
				myfile.write(code+","+url+","+str(total)+","+typeFile+','+language+', outer\n')
				return total
			else:
				
				links = soup.findAll('a', href=True)
				parent=url
				if(url.count('/')>2):
					r3=url.split('/')
					parent=url[:-len(r3[len(r3)-1])]
				links=converLinkObj(links, parent)
				print(code, url,str(total),typeFile,language,'intern')
				myfile.write(code+","+url+","+str(total)+","+typeFile+','+language+', intern \n')
				
				
				try:
					for link in links:
								#totalLista=calculo([link['href'],url])
						totalLista=calculo(link)
						if(totalLista==None):
								totalLista=0
						total=total+int(totalLista)
					return total
				except Exception, err:
					print(err)
					return total
		return 0
	except Exception, err:
		print(err)
		return 0




sys.setrecursionlimit(3000)
myfile =open("output/c8.csv","a") 
urlRoot='www.threesl'
print("----------------------START---------------------------")
myfile.write("Total"+","+str(calculo('http://www.threesl.com')))
myfile.close()
print("----------------------END---------------------------")
