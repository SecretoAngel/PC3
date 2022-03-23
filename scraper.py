## IMPORTS
#import firebase_admin
#import functions_framework
import requests as req
from bs4 import BeautifulSoup
from datetime import datetime  

##VARIABLES

#@functions_framework.http
def hello(requests):

    listaCategorias=['https://www.elmundo.es/ciencia-y-salud/salud.html','https://www.elmundo.es/ciencia-y-salud/ciencia.html','https://elpais.com/noticias/delitos-odio/']
    nombreCategoria=['salud','ciencia','odio']
    contador=0

    for link in listaCategorias:
        rMundo = req.get(link)
        soup_Mundo= BeautifulSoup(rMundo.text, 'html.parser')   
        Enlaces_Noticias=[]                                                                           
        if contador==2:                                                                                     
            ElmundoBloqueEntero=soup_Mundo.find('div','b-b b-au_b')                                      
            Elmundo_odio_pagina=ElmundoBloqueEntero.find_all('article')                                    
            for i in Elmundo_odio_pagina:                                                                  
                enlace="https://elpais.com"+((((i.find('header')).find('h2','c_t')).find("a")))["href"]
                print(enlace)
                print("\n")
                Enlaces_Noticias.append(enlace)                                                       
            pasar_datos_ficheros_Odio(Enlaces_Noticias,'./webScraping/'+nombreCategoria[contador]+'/',nombreCategoria[contador]) 
        else: 
            Elmundo_noticias=soup_Mundo.find_all('div','ue-l-cover-grid__unit ue-l-cover-grid__unit--no-grow')      
                                                                                                                    
            for noticia in Elmundo_noticias:    
                atag=noticia.find("a")                                                                                    
                atag["href"]=atag["href"]                                                                           
                print(atag["href"])                                                                                 
                Enlaces_Noticias.append(atag["href"])

            pasar_datos_ficheros(Enlaces_Noticias,'./webScraping/NoOdio/',nombreCategoria[contador])
        contador=contador+1                                                                                        

    return f"Hello" 


def pasar_datos_ficheros(enlaces_titulares,ruta,catego):
    j=0
    for i in enlaces_titulares:
        crear_ficheros_noticiasMundo(i,j,ruta,catego)                                                               
        j+=1

def pasar_datos_ficheros_Odio(enlaces_titulares,ruta,catego):
    j=0
    for i in enlaces_titulares:
        crear_ficheros_noticiasMundoOdio(i,j,ruta,catego)
        j+=1

def crear_ficheros_noticiasMundoOdio(enlace,contador,ruta,catego):
    parrafos=""
    fecha = datetime.today().strftime('%Y-%m-%d')
    url_enlaces = req.get(enlace)
    soup_enlaces = BeautifulSoup(url_enlaces.text, 'html')
    
    try:
        Titulo=(soup_enlaces.find('div','a_e_txt _df')).find('h1','a_t').getText()
    except:
        Titulo=""                                                                                               
    try:                                                                                                          
        Entradilla=(soup_enlaces.find('div','a_e_txt _df')).find('h2','a_st').getText()                          
    except:                                                                                                      
        Entradilla=""                                                                                             
                                                                                                                 
    try:                                                                                                            
        Body=(soup_enlaces.find('div','a_c clearfix')).find_all('p')
        for p in Body:
            parrafos=parrafos+p.getText()
    except:
        parrafos=""
    try:
        LugarYFecha=(soup_enlaces.find('article','a _g _g-lg _g-o').find('div','a_md_txt')).find('span').getText()
    except:
        LugarYFecha=""

    ##with open(ruta + fecha + ".00."+catego+ str(contador) +".txt","w",encoding="utf-8") as temp:              
         

def crear_ficheros_noticiasMundo(enlace,contador,ruta,catego):                                                
    #obtener y parsear el enlace de noticia                                                                     
    parrafos=""
    fecha = datetime.today().strftime('%Y-%m-%d')
    url_enlaces = req.get(enlace)
    soup_enlaces = BeautifulSoup(url_enlaces.text, 'html')
    #obtener contenido de noticia
    Cuerpo_Noticia_Header=soup_enlaces.find('div','ue-l-article__header ue-c-article__header') #cabecera
    Cuerpo_Noticia_body=soup_enlaces.find('div','ue-l-article__body ue-c-article__body')
    Cuerpo_Noticia_Lugar=soup_enlaces.find('div','ue-c-article__bar ue-l-article--leftcol-width-from-desktop ue-l-article--float-left-from-desktop ue-l-article--move-to-leftcol-from-desktop ue-l-article--order-1-from-mobile')
    try:
        Titulo= (Cuerpo_Noticia_Header.find('div','ue-l-article__header-content')).find('h1','ue-c-article__headline js-headline').getText()
    except:
        Titulo=""
    try:
        Entradilla= (Cuerpo_Noticia_Header.find('p','ue-c-article__standfirst')).getText()
    except:
        Entradilla=""
    try:
        Cuerpo=Cuerpo_Noticia_body.find_all('p')
        for p in Cuerpo:
            parrafos=parrafos+p.getText()
    except:
        parrafos=""
    try:
        Lugar=(Cuerpo_Noticia_Lugar.find('ul','ue-c-article__byline ue-c-article__byline--boxed')).find('div','ue-c-article__byline-location').getText()
    except:
        Lugar=""
    try:
        Fecha=(Cuerpo_Noticia_Lugar.find('div','ue-c-article__publishdate')).find('time').getText()
    except:
        Fecha=""
    
    ##with open(ruta + fecha + ".00."+catego+ str(contador) +".txt","w",encoding="utf-8") as temp:                 
         