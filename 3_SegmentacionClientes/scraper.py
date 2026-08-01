"""
Este archivo creara un scraper para poder sacar el precio de ingreso a cada sitio turistico en peru
"""

#########################################
##### Setup general
#### Importando modulos
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import pandas as pd
import os

#### Cargando datos
os.chdir('3_SegmentacionClientes')
datos = os.path.join('Datos', 'InventorioRecursosTuristicos', 'Inventario_recursos_turisticos.csv')
df = pd.read_csv(datos, sep=';', encoding='latin-1', header=0)
urls = df['URL'].values.tolist()


#########################################
##### Web scrapping precios de ingreso
#### Setup
filas = []
start = 2614
#### Bucle 
for i, url in enumerate(urls[start:]):
    print(i + start)
    ### SEtup
        # Cada pagina tiene su "tipo" y "observacion"
    tipo = []
    observacion = []
    ### Cargando pagina
    driver = webdriver.Edge()
    driver.get(url)
    WebDriverWait(driver, 120).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#accordionContent"))
    )  

    ### Encontrando lista principal
    acordion = driver.find_element(By.CSS_SELECTOR, "#accordionContent")
        # Lista principal
    categorias_tags = acordion.find_elements(By.CSS_SELECTOR, ":scope > h3")
        # Hijos de lista - muestra los nombres de las categorias
    categorias = [categoria.text.lower() for categoria in categorias_tags]
        # Transformando las categorias en miniscula

    ### Casos si/no existe "ingreso" en categorias
    if "tipo de ingreso" in categorias:
        idx = categorias.index('tipo de ingreso')
            # Buscando la categoria de "tipo de ingreso"
        ingreso_div = acordion.find_element(By.CSS_SELECTOR, f'#ui-accordion-accordionContent-panel-{idx}')
            # Buscando el div asociado
        driver.execute_script("arguments[0].setAttribute('style', 'display: block;');", ingreso_div)
            # Activando el javascript del div asociado; haciendo el click 
        ingreso_table = ingreso_div.find_elements(By.XPATH, ".//td[@align='left']")
            # Buscando los elementos de la table de ingreso
        impar = True
        for itm in ingreso_table: 
            if impar: tipo.append(itm.text)
            else: observacion.append(itm.text)
            impar = not impar
        filas.append(["#".join(tipo), "#".join(observacion)])
    else:
        filas.append(['NA','NA'])
    driver.quit()

##########################################
##### Finalizando web scrapping
#### Transformando filas en dataframe
tmp = pd.DataFrame(filas, columns=['TIPO','OBSERVACION'])
tmp_path = os.path.join('Datos', 'Limpios', 'tmp.csv')
tmp.to_csv(tmp_path, index=False, encoding='utf-8')

#### Uniendo ambos dataframes
df_final = pd.concat([df, tmp], ignore_index=False, axis=1)

#### Guardando DF final
limpio_path = os.path.join('Datos', 'Limpios', 'web_scrapped_inventario_recursos_turisticos.csv')
df_final.to_csv(limpio_path, index=False, encoding='utf-8')
