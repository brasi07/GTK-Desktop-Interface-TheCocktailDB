import locale
import requests

    

class Model:
    
    def __init__(self):
        default_locale, _ = locale.getdefaultlocale()
        if default_locale is None:
            default_locale = 'es_Es'

        self.idioma = default_locale[:-3].upper()
        if self.idioma != "ES":
            self.idioma = ""

    def get_catalog(self) -> list:
        catalog_default = []
        for i in range(15) :
            
            random_drink = self.get_info_drink(None, "random", "", "", None)
            
            if random_drink != 400:
                catalog_default.append(random_drink[0])
            else:
                return 400

        return catalog_default
    
    def download_image(self, url) -> bytes:
        try:
            response = requests.get(url, stream=True)

            if response.status_code == 200:
                image_data= response.content
                return image_data
            
        except Exception as e:
            print(f"Error al cargar la imagen desde la URL: {e}")
        return None
    
    def dividir_texto_en_lineas(self, texto, tamaño_de_linea) -> str:
        if(texto):
            lineas = []
            palabras = texto.split()  # Dividir el texto en palabras
            linea_actual = ""
    
            for palabra in palabras:
                if len(linea_actual) + len(palabra) + 1 <= tamaño_de_linea:  # +1 para el espacio
                    if linea_actual:
                        linea_actual += " "
                    linea_actual += palabra
                else:
                    lineas.append(linea_actual)
                    linea_actual = palabra

            if linea_actual:
                lineas.append(linea_actual)

            return "\n".join(lineas)
        return ""

    def get_info_ingredient(self, name) -> list:
        try:
            response = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?i={name}")
            
            if response.status_code == 200:
                info_ingrediente = []
                data = response.json()["ingredients"][0]

                nombre_ingrediente = data["strIngredient"]
                imagen_ingrediente = self.download_image(f"https://www.thecocktaildb.com/images/ingredients/{nombre_ingrediente}.png")
                id_ingrediente = data["idIngredient"]

                info_ingrediente = [nombre_ingrediente, imagen_ingrediente, id_ingrediente]   

                return info_ingrediente
            else:
                print("Error en la solicitud:", response.status_code)
        except requests.exceptions.HTTPError as he:
            return 500
        except requests.exceptions.RequestException as re:
            return 400
        except ValueError as ve:
            return []
        except Exception as e:
            return []
        return []
    
    def get_info_drink(self, name, type, alc, cat, op) -> list:
        try:
            if type == "search":
                response = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}")
            elif type == "random":
                response = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/random.php")
            elif type == "category":
                response = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/list.php?{name}=list")
            elif type == "letter":
                response=requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={name}")
            else:
                print("Error en la llamada a la función")
                return []
            
            if response.status_code == 200:

                info_bebidas = []
                data = response.json()["drinks"]
                
                for product_data in data:
                    if(type=="category"):
                        if op==0:
                            op_filter="strAlcoholic"
                        else:
                            op_filter="strCategory"
                        nombre_bebida = product_data[op_filter]
                        info_bebida=[nombre_bebida]
                        info_bebidas.append(info_bebida)
                    elif(type=="random"):
                        nombre_bebida = product_data["strDrink"]
                        imagen_bebida = self.download_image(product_data["strDrinkThumb"] + "/preview")
                        id_bebida = product_data["idDrink"]

                        info_bebida = [nombre_bebida, imagen_bebida, id_bebida]
                        info_bebidas.append(info_bebida)
                    else:
                        if(alc=="" or product_data["strAlcoholic"]==alc):
                            if (cat=="" or product_data["strCategory"]==cat):
                                nombre_bebida = product_data["strDrink"]
                                imagen_bebida = self.download_image(product_data["strDrinkThumb"] + "/preview")
                                id_bebida = product_data["idDrink"]

                                info_bebida = [nombre_bebida, imagen_bebida, id_bebida]
                                info_bebidas.append(info_bebida)
                        else:
                            continue
                return info_bebidas
            else:
                print("Error en la solicitud:", response.status_code)
        except requests.exceptions.HTTPError as he:
            return 500
        except requests.exceptions.RequestException as re:
            return 400
        except ValueError as ve:
            return []
        except Exception as e:
            return []
        return []
        
    def get_details_product(self, id: str) -> list:
        print(f"Id bebida: {id}")
        try:
            
            response = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={id}")
            
            if response.status_code == 200:
                
                data = response.json()["drinks"][0]
                nombre_producto = data["strDrink"]               
                imagen_producto = self.download_image(data["strDrinkThumb"] + "/preview")               
                vaso_cocktail = data["strGlass"]    
                alcoholic_producto = data["strAlcoholic"]        
                categoria_producto = data["strCategory"]   
                instrucciones_producto = self.dividir_texto_en_lineas(data[f"strInstructions{self.idioma}"],150)
                
                ingredientes_producto = []
                for i in range(1, 16):  # El API numera los ingredientes del 1 al 15
                    nombre_ingrediente = data[f"strIngredient{i}"]
                    if nombre_ingrediente == None:
                        return [nombre_producto, imagen_producto, instrucciones_producto, ingredientes_producto, vaso_cocktail, alcoholic_producto, categoria_producto]
                    else:
                        info = self.get_info_ingredient(nombre_ingrediente)
                        imagen_ingrediente = info[1]
                        id_ingrediente = info[2]
                        medida_ingrediente = data[f"strMeasure{i}"]
                        medida_nombre_ingrediente = f"{medida_ingrediente} {nombre_ingrediente}"

                        print(f"Nombre ingrediente: {nombre_ingrediente}, Id: {id_ingrediente}")
                        info_ingrediente = [medida_nombre_ingrediente, imagen_ingrediente, id_ingrediente]   
                        ingredientes_producto.append(info_ingrediente)
                    
                return [nombre_producto, imagen_producto, instrucciones_producto, ingredientes_producto, vaso_cocktail, alcoholic_producto, categoria_producto]
                
            else:
                print("Error en la solicitud:", response.status_code)
        except requests.exceptions.HTTPError as he:
            return 500
        except requests.exceptions.RequestException as re:
            return 400
        except ValueError as ve:
            return []
        except Exception as e:
            return []
        return []
    
    
    def get_details_ingredient(self, id: str) -> list:
        print(f"Id ingrediente: {id}")
        try:
            response = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?iid={id}")

            if response.status_code == 200:

                data = response.json()["ingredients"][0]
                nombre_ingrediente = data["strIngredient"]
                imagen_ingrediente = self.download_image(f"https://www.thecocktaildb.com/images/ingredients/{nombre_ingrediente}.png")
                descripcion_ingrediente = self.dividir_texto_en_lineas(data["strDescription"], 150)
                productos_ingrediente = self.get_info_drink(nombre_ingrediente, "search", None, None, None)
                tipo_ingrediente = data["strType"]
                alcohol_ingrediente = data["strAlcohol"]

                response2 = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={nombre_ingrediente}")
                if response2.status_code == 200:
                    productos_ingrediente = []
                    data = response2.json()["drinks"]
                    for product_data in data:
                        nombre_bebida = product_data["strDrink"]
                        imagen_bebida = self.download_image(product_data["strDrinkThumb"] + "/preview")
                        id_bebida = product_data["idDrink"]

                        info_bebida = [nombre_bebida, imagen_bebida, id_bebida]
                        print(f"Nombre bebida: {nombre_bebida}, Id: {id_bebida}")
                        productos_ingrediente.append(info_bebida)
                                        
                    return [nombre_ingrediente, imagen_ingrediente, descripcion_ingrediente, productos_ingrediente, tipo_ingrediente, alcohol_ingrediente]
                else:
                    print("Error en la solicitud:", response2.status_code)
            else:
                print("Error en la solicitud:", response.status_code)
        except requests.exceptions.HTTPError as he:
            return 500
        except requests.exceptions.RequestException as re:
            return 400
        except ValueError as ve:
            return []
        except Exception as e:
            return []
        return []