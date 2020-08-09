# CORRER POR PARTES , VEAN WEB SCRAPY , CHROME
# LA IDEA ES MOSTRAR LOS ARTICULOS , SUS CITACIONES Y TOTAL DE CITACIONES SACARLO DE LA WEB
# YA CON JAVA O C# DIGITO EL NOMBRE , APELLIDO Y QUE SALGA SUS ARTICULOS Y SU TOTAL DE CITACIONES


from conexion_mysql import Database
from models.perfil import Perfil
from models.articulo import Articulo

from urllib.request import urlopen
from bs4 import BeautifulSoup


def user_scrapping():    
    nombre = [i.text for i in soup.find_all(id="gsc_prf_in") ]
    print('Nomnbre: ', nombre[0])
    perfil.nombre = nombre[0]

    institucion = [i.text for i in soup.find_all(class_="gsc_prf_ila") ]
    print('Institucion: ', institucion[0])
    perfil.institucion = institucion[0]

    foto = [i['src'] for i in soup.find_all(id="gsc_prf_pup-img") ]
    print('URL Foto: ', foto[0])
    perfil.foto = foto[0]



def insert_perfil(perfil):
    database = Database()
    sql = "INSERT INTO PERFIL(nombre, institucion, foto) VALUES ('{}','{}','{}')".format(perfil.nombre, perfil.institucion, perfil.foto)

    try:
        database.cursor.execute(sql)
        database.connection.commit()
    except Exception as e:
        raise
    
    print("Perfil registrado exitosamente!!")
    perfil.id_perfil = database.cursor.lastrowid
    print("id_perfil: ", database.cursor.lastrowid)
    database.connection.close()



def articulo_scrapping():
    titulo = [i.text for i in soup.find_all(class_="gsc_a_at") ]
    print('Titulo: ', titulo)

    nro_citas = [i.text for i in soup.find_all(class_="gsc_a_ac gs_ibl") ]
    print("Nro citas: ", nro_citas)

    anio_pub = [i.text for i in soup.find_all(class_="gsc_a_h gsc_a_hc gs_ibl") ]
    print("Año de publicación: ", anio_pub)
    
    for i in range(len(titulo)):
        articulo = Articulo(None, perfil.id_perfil, titulo[i], nro_citas[i], anio_pub[i])
        # print("Articulo [{}]: Titulo: {}, Numero Citas: {}, Año: {}".format(i, articulo.titulo, articulo.nro_citas, articulo.anio)
        insert_articulo(articulo)


def insert_articulo(articulo):
    database = Database()
    if articulo.anio == '': articulo.anio = 0
    if articulo.nro_citas == '': articulo.nro_citas = 0
    sql = "INSERT INTO ARTICULO(id_perfil, titulo, nro_citas, anio) VALUES ({},'{}',{},{})".format(articulo.id_perfil, articulo.titulo, articulo.nro_citas, articulo.anio)

    try:
        database.cursor.execute(sql)
        database.connection.commit()
    except Exception as e:
        raise
    
    print("Articulo registrado exitosamente!!")
    database.connection.close()



# MAIN
url = input("Inserte URL del perfil Google Scholar: ")
# url = "https://scholar.google.com/citations?user=CDt8mKsAAAAJ&hl=es&oi=ao"
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')

perfil = Perfil(None, None, None, None) # Crea un perfil vacio

user_scrapping()    # Scrapea el perfil del investigador
insert_perfil(perfil)   #Inserta el perfil a la base de datos 
# print(perfil.id_perfil)

articulo_scrapping()    #Scrappea e inserta cada articulo en la base de datos

