from __future__ import annotations
from typing import Any, Callable, Protocol

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, GObject, Adw, GdkPixbuf

import gettext

_ = gettext.gettext
N_ = gettext.ngettext

def run(application_id: str, on_activate: Callable) -> None:
    app = Gtk.Application(application_id = application_id)
    app.connect('activate', on_activate)
    app.run()

def clear_grid(grid):
    for i in range(5, 0, -1):
        grid.remove_column(i-1)

def create_button_with_image(pixbuf, nombre):
    button = Gtk.Button()
    image = Gtk.Image()
    image.set_from_pixbuf(pixbuf)
    image.set_property("width-request", 200)
    image.set_property("height-request", 200)   

    text_label = Gtk.Label(label= nombre)

    grid = Gtk.Grid()

    grid.attach(image, 0, 0, 1, 1)
    grid.attach(text_label, 0, 1, 1, 1)
    
    button.set_child(grid)

    return button

def create_pixbuff(imagen_data):
    loader = GdkPixbuf.PixbufLoader.new()
    loader.write(imagen_data)
    loader.close()
    return loader.get_pixbuf()

class ViewHandler(Protocol):
    def on_search_clicked(name) -> None: pass
    def on_random_clicked() -> None: pass
    def on_product_clicked(name) -> None: pass
    def on_ingredient_clicked(name) -> None: pass
    def on_letter_clicked(name) -> None: pass
    def get_catalog() -> None: pass

class View:
    def __init__(self):
        self.handler = None

    def on_activate(self, app: Gtk.Application) -> None:
        self.build(app)
    
    def set_handler(self, handler: ViewHandler) -> None:
        self.handler = handler

    def buttons_sensitive(self):
        self.search_button.set_sensitive(True)
        self.search_bar.set_sensitive(True)
        self.random_button.set_sensitive(True)
        self.home_button.set_sensitive(True)
        self.filter_button.set_sensitive(True)
        self.letters_sensitive(True)
        self.products_sensitive(self.grid_catalog, True)
        self.products_sensitive(self.grid_catalog_mini, True)

    def letters_sensitive(self, set):
        i = 0
        for letra in 'abcdefghijklmnopqrstuvwxyz': 
            child = self.grid_letters.get_child_at(0, i)
            child.set_sensitive(set)
            i+=1

    def products_sensitive(self, grid, set):
        row = 0
        child = ""
        while child != None:
            for col in range(5): 
                child = grid.get_child_at(col, row)
                if child != None:
                    child.set_sensitive(set)  
            row+=1

    def error_conexion(self):
        clear_grid(self.grid_catalog)
        self.grid_catalog.set_halign(Gtk.Align.CENTER)
        error_red = Gtk.Label(label = _("No hay conexión a internet"))
            
        image = Gtk.Image.new_from_file("./error.png")
        image.set_size_request(200, 200)

        self.grid_catalog.attach(error_red, 0, 0, 1, 1)
        self.grid_catalog.attach(image, 0, 1, 1, 1)
        self.spinner.stop()
        self.buttons_sensitive()

    def error_servidor(self):
        clear_grid(self.grid_catalog)
        self.grid_catalog.set_halign(Gtk.Align.CENTER)
        error_servidor = Gtk.Label(label = _("Error de servidor, vuelva a intentarlo más tarde"))
            
        image = Gtk.Image.new_from_file("./servidor.png")
        image.set_size_request(200, 200)

        self.grid_catalog.attach(error_servidor, 0, 0, 1, 1)
        self.grid_catalog.attach(image, 0, 1, 1, 1)
        self.spinner.stop()
        self.buttons_sensitive()

    def product_not_found(self):
        clear_grid(self.grid_catalog)
        self.grid_catalog.set_halign(Gtk.Align.CENTER)
        not_found = Gtk.Label(label = _("No se han encontrado resultados, pruebe con otra búsqueda"))
            
        image = Gtk.Image.new_from_file("./triste.png")
        image.set_size_request(200, 200)

        self.grid_catalog.attach(not_found, 0, 0, 1, 1)
        self.grid_catalog.attach(image, 0, 1, 1, 1)

    def set_grid_with_products(self, grid, detalles_productos: list) -> None:
        clear_grid(grid)
        grid.set_halign(Gtk.Align.CENTER)
        
        if detalles_productos:
            i = 1
            for product in detalles_productos:
                button = create_button_with_image(create_pixbuff(product[1]), product[0])
                button.connect('clicked', lambda _wg, id=product[2]: self.handler.on_product_clicked(id))
                
                grid.attach(button, (i - 1) % 5, (i - 1) // 5, 1, 1)
                i += 1
        else:
            self.product_not_found()

    def update(self, detalles_productos: list) -> None:
        self.label_box1.set_label(_("Catálogo"))
        self.set_grid_with_products(self.grid_catalog, detalles_productos)
        self.spinner.stop()
        self.buttons_sensitive()

    def do_filtros(self):
        current_visibility = self.box_filtros.get_visible()
        self.box_filtros.set_visible(not current_visibility)

   
    #FUNCIONES VER DETALLES

    def set_grid_with_ingredients(self, grid, detalles_ingredientes: list) -> None:
        clear_grid(grid)
        grid.set_halign(Gtk.Align.CENTER)

        if detalles_ingredientes:
            i = 1
            for ingredient in detalles_ingredientes:
                button = create_button_with_image(create_pixbuff(ingredient[1]), ingredient[0])
                button.connect('clicked', lambda _wg, id=ingredient[2]: self.handler.on_ingredient_clicked(id))
            
                grid.attach(button, (i - 1) % 5, (i - 1) // 5, 1, 1)
                i += 1
        else:
            self.product_not_found()

    def see_details_product(self, detalles_producto: list) -> None:

        clear_grid(self.grid_catalog)
        self.grid_catalog.set_halign(Gtk.Align.START)
        self.label_box1.set_label(_("Detalles"))

        image = Gtk.Image()
        image.set_from_pixbuf(create_pixbuff(detalles_producto[1]))
        image.set_size_request(300, 300)

        nombre = Gtk.Label(label= detalles_producto[0])

        titulo_instrucciones = Gtk.Label(label = _("Instrucciones:"), hexpand= False)
        titulo_instrucciones.set_halign(Gtk.Align.CENTER)

        instructiones = Gtk.Label(
            label = detalles_producto[2],
            hexpand= False,
            margin_top= 10,
            margin_end= 10,
            margin_bottom= 10,
            margin_start= 10
        )

        self.scroll_description_mini.set_child(instructiones)

        self.grid_catalog.attach(nombre, 0, 0, 1, 1)
        self.grid_catalog.attach(image, 0, 1, 1, 1)
        self.grid_catalog.attach(titulo_instrucciones, 1, 2, 1, 1)
        self.grid_catalog.attach(self.scroll_description_mini, 1, 3, 1, 1)

        titulo_grid = Gtk.Label(label = _("Ingredientes"), hexpand= False)
        titulo_grid.set_halign(Gtk.Align.CENTER)
        
        self.set_grid_with_ingredients(self.grid_catalog_mini, detalles_producto[3])
        self.scroll_catalog_mini.set_child(self.grid_catalog_mini)

        titulo_caracteristicas = Gtk.Label(label = _("Características:"), hexpand= False)

        grid_caracteristicas = Gtk.Grid(
            column_spacing= 14,
            row_spacing= 12,
            hexpand= False,
            halign=Gtk.Align.CENTER
        )

        titulo_vaso = Gtk.Label(label = _("Vaso:"), hexpand= False)
        vaso = Gtk.Label(label = detalles_producto[4], hexpand= False)
        titulo_tipo = Gtk.Label(label = _("Tipo:"), hexpand= False)
        tipo = Gtk.Label(label = detalles_producto[5], hexpand= False)
        titulo_categoria = Gtk.Label(label = _("Categoria:"), hexpand= False)
        categoria = Gtk.Label(label = detalles_producto[6], hexpand= False)

        grid_caracteristicas.attach(titulo_vaso, 0, 0, 1, 1)
        grid_caracteristicas.attach(vaso, 1, 0, 1, 1)
        grid_caracteristicas.attach(titulo_tipo, 0, 1, 1, 1)
        grid_caracteristicas.attach(tipo, 1, 1, 1, 1)
        grid_caracteristicas.attach(titulo_categoria, 0, 2, 1, 1)
        grid_caracteristicas.attach(categoria, 1, 2, 1, 1)

        self.grid_catalog.attach(titulo_grid, 1, 0, 1, 1)
        self.grid_catalog.attach(self.scroll_catalog_mini, 1, 1, 1, 1)
        self.grid_catalog.attach(titulo_caracteristicas, 0, 2, 1, 1)
        self.grid_catalog.attach(grid_caracteristicas, 0, 3, 1, 1)

        self.spinner.stop()
        self.buttons_sensitive()

    def see_details_ingredient(self, detalles_ingrediente: list) -> None:

        clear_grid(self.grid_catalog)
        self.grid_catalog.set_halign(Gtk.Align.START)
        self.label_box1.set_label(_("Detalles"))

        image = Gtk.Image()
        image.set_from_pixbuf(create_pixbuff(detalles_ingrediente[1]))
        image.set_size_request(300, 300)

        nombre = Gtk.Label(label= detalles_ingrediente[0])

        titulo_descripcion = Gtk.Label(label = _("Descripción:"), hexpand= False)
        titulo_descripcion.set_halign(Gtk.Align.START)

        descripcion = Gtk.Label(
            label = detalles_ingrediente[2],
            hexpand= False,
            margin_top= 10,
            margin_end= 10,
            margin_bottom= 10,
            margin_start= 10
        )

        self.scroll_description_mini.set_child(descripcion)

        self.grid_catalog.attach(nombre, 0, 0, 1, 1)
        self.grid_catalog.attach(image, 0, 1, 1, 1)
        self.grid_catalog.attach(titulo_descripcion , 1, 2, 1, 1)
        self.grid_catalog.attach(self.scroll_description_mini, 1, 3, 1, 1)

        titulo_grid = Gtk.Label(label = _("Cócteles"), hexpand= False)
        titulo_grid.set_valign(Gtk.Align.CENTER)
        
        self.set_grid_with_products(self.grid_catalog_mini, detalles_ingrediente[3])
        self.scroll_catalog_mini.set_child(self.grid_catalog_mini)

        titulo_caracteristicas = Gtk.Label(label = _("Características:"), hexpand= False)

        grid_caracteristicas = Gtk.Grid(
            column_spacing= 14,
            row_spacing= 12,
            hexpand= False,
            halign=Gtk.Align.CENTER
        )

        titulo_tipo = Gtk.Label(label = _("Tipo:"), hexpand= False)
        tipo = Gtk.Label(label = detalles_ingrediente[4], hexpand= False)
        titulo_alcohol = Gtk.Label(label = _("Alcohol:"), hexpand= False)
        alcohol = Gtk.Label(label = detalles_ingrediente[5], hexpand= False)

        grid_caracteristicas.attach(titulo_tipo, 0, 0, 1, 1)
        grid_caracteristicas.attach(tipo, 1, 0, 1, 1)
        grid_caracteristicas.attach(titulo_alcohol, 0, 1, 1, 1)
        grid_caracteristicas.attach(alcohol, 1, 1, 1, 1)

        self.grid_catalog.attach(titulo_grid, 1, 0, 1, 1)
        self.grid_catalog.attach(self.scroll_catalog_mini, 1, 1, 1, 1)
        self.grid_catalog.attach(titulo_caracteristicas, 0, 2, 1, 1)
        self.grid_catalog.attach(grid_caracteristicas, 0, 3, 1, 1)

        self.spinner.stop()
        self.buttons_sensitive()

    #---------------------------------------------------
    #FUNCIONES BOTONES ALCOHOL
    def on_toggled(self, num, len, state, array, var):
        if var=="alc":
            if self.alc!=state:
                for i in range (len):
                    array[i].set_active(False)
                self.alc=state
                array[num].set_active(True)
            else:
                self.alc=""
                for i in range (len):
                        array[i].set_active(False)
        else:
            if self.cat!=state:
                for i in range (len):
                    array[i].set_active(False)
                self.cat=state
                array[num].set_active(True)
            else:
                self.cat=""
                for i in range (len):
                        array[i].set_active(False)


    def add_filter_button(self, label, func, filter_buttons, num, len, var):
        but=Gtk.ToggleButton(label=label)
        but.set_active(False)
        but.connect('toggled', lambda _: getattr(self, func)(num, len, label, filter_buttons, var))
        filter_buttons.append(but)
    
    def cat_to_var(self, name) -> str:
        return name.replace(" ", "_")
    #---------------------------------------------------

    def build(self, app: Gtk.Application) -> None:
        self.window = win = Gtk.ApplicationWindow(title="App")
        app.add_window(win)
        win.set_title("The Cocktail DB")
        win.connect("destroy", lambda win: win.close())
        self.spinner = Gtk.Spinner()
        self.alc=""
        self.cat=""

        #BARRA DE BUSQUEDA
        self.search_bar = Gtk.SearchEntry(
            placeholder_text = (_("Busca aqui...")),
            hexpand = True,
        )
        self.search_bar.connect("activate", lambda _wg: self.handler.on_search_clicked(self.search_bar.get_text().strip()))

        #IMAGENES
        self.image = Gtk.Image.new_from_file("./lupa.png")
        self.image2 = Gtk.Image.new_from_file("./dado.png")
        self.image3 = Gtk.Image.new_from_file("./filtros.png")
        self.image4 = Gtk.Image.new_from_file("./home.png")

        #BOTON DE BUSQUEDA
        self.search_button = Gtk.Button(label="Search", hexpand = False)
        self.search_button.set_child(self.image)
        self.search_button.connect('clicked', lambda _wg: self.handler.on_search_clicked(self.search_bar.get_text().strip()))
        
        #BOTON RANDOM
        self.random_button=Gtk.Button(label="Random Cocktail", hexpand = False, halign=Gtk.Align.START)
        self.random_button.set_child(self.image2)
        self.random_button.connect('clicked', lambda _wg: self.handler.on_random_clicked())

        #BOTON FILTROS
        self.filter_button=Gtk.Button(label="Filters", hexpand = False, halign=Gtk.Align.START)
        self.filter_button.set_child(self.image3)
        self.filter_button.connect('clicked', lambda _wg: self.do_filtros())

        #BOTON VOLVER AL MENU
        self.home_button = Gtk.Button(label ="Home Button", hexpand = False)
        self.home_button.set_child(self.image4)
        self.home_button.connect('clicked', lambda _wg: self.handler.get_catalog())

        #BOTONES ALCOHOL
        self.filter_buttons1=[]
        categories1=self.handler.filter_list("a", 0)
        if categories1 is None:
            len1 = 0 
        else:
            len1 = len(categories1)
            i=0
            for cat in categories1:
                name=cat[0]
                func_name="on_toggled"
                self.add_filter_button(name, func_name, self.filter_buttons1, i, len1, "alc")
                i+=1
            
        #BOTONES CATEGORÍA
        self.filter_buttons2=[]
        categories2=self.handler.filter_list("c", 1)
        if categories2 is None:
            len2 = 0 
        else:
            len2 = len(categories2)
            i=0
            for cat in categories2:
                name=cat[0]
                func_name="on_toggled"
                self.add_filter_button(name, func_name, self.filter_buttons2, i, len2, "cat")
                i+=1

        #BARRA DE BUSQUEDA
        self.grid_search_bar = Gtk.Grid(
            column_spacing= 12,
            row_spacing= 12,
            margin_start= 12,
            margin_end= 12,
            margin_top= 12,
            margin_bottom= 12
        )
        self.grid_search_bar.attach(self.search_bar, 0, 0, 1, 1)
        self.grid_search_bar.attach(self.random_button, 1, 0, 1, 1)
        self.grid_search_bar.attach(self.filter_button, 2, 0, 1, 1)
        self.grid_search_bar.attach(self.search_button, 3, 0, 1, 1)
        self.grid_search_bar.attach(self.home_button, 4, 0, 1, 1)

        #CUADRICULA PRODUCTOS
        self.grid_catalog = Gtk.Grid(
            column_spacing= 14,
            row_spacing= 12,
            margin_start= 12,
            margin_end= 12,
            margin_top= 12,
            margin_bottom= 12,
            hexpand= False,
            halign=Gtk.Align.CENTER
        )

        #CUADRÍCULA INGREDIENTES/PRODUCTOS
        self.grid_catalog_mini = Gtk.Grid(
            column_spacing= 14,
            row_spacing= 12,
            margin_start= 12,
            margin_end= 12,
            margin_top= 12,
            margin_bottom= 12,
            hexpand= False
        )

        #CUADRÍCULA BOTONES LETRAS
        self.grid_letters= Gtk.Grid(
            column_spacing= 12,
            row_spacing= 12,
            margin_start= 12,
            margin_end= 12,
            margin_bottom= 12,
            halign=Gtk.Align.CENTER
        )
        i = 0
        for letra in 'abcdefghijklmnopqrstuvwxyz': 
            button_letters = Gtk.Button(label= letra.upper())
            button_letters.connect('clicked', lambda _wg, letter=letra: self.handler.on_letter_clicked(letter))
            self.grid_letters.attach(button_letters, 0, i, 1, 1)
            i += 1

        #SCROLL CUADRICULA PRODUCTOS
        self.scroll = Gtk.ScrolledWindow(
            hexpand= True,
            vexpand= True,
            has_frame = True,
            halign= Gtk.Align.BASELINE,
            window_placement = Gtk.CornerType.TOP_LEFT,
            margin_top= 10,
            margin_end= 10,
            margin_bottom= 10,
            margin_start= 10,
        )
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_child(self.grid_catalog)

        #SCROLL CUADRÍCULA INGREDIENTES/PRODUCTOS
        self.scroll_catalog_mini = Gtk.ScrolledWindow(
            hexpand= False,
            vexpand= True,
            has_frame = True,
            halign= Gtk.Align.BASELINE,
            window_placement = Gtk.CornerType.TOP_RIGHT,
        )
        self.scroll_catalog_mini.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        #SCROLL DESCRIPCION/INSTRUCCIONES
        self.scroll_description_mini = Gtk.ScrolledWindow(
            hexpand= True,
            vexpand= True,
            has_frame = False,
            halign= Gtk.Align.BASELINE,
            window_placement = Gtk.CornerType.TOP_LEFT
        )
        self.scroll_description_mini.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        #TITULOS
        self.label_box1 = Gtk.Label(label= _("Catálogo"))
        self.label_box2 = Gtk.Label(label= _("Filtrar por contenido de alcohol\n"))
        self.label_box3 = Gtk.Label(label= _("\nFiltrar por categoría\n"))
        self.label_box4 = Gtk.Label(label= _("\nBuscar por Letra\n"))    

        #BOX FILTROS ALCOHOL
        self.box_filters1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, halign=Gtk.Align.CENTER)        
        self.box_filters1.set_property("halign", Gtk.Align.CENTER)
        for bot in self.filter_buttons1:
            self.box_filters1.append(bot)
        
        #BOX FILTROS CATEGORIA
        self.box_filters2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, halign=Gtk.Align.CENTER)        
        self.box_filters2.set_property("halign", Gtk.Align.CENTER)
        for bot in self.filter_buttons2:
            self.box_filters2.append(bot)
        
        #BOX TITULO/SPINNER       
        self.box_titulo_spinner = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, halign=Gtk.Align.CENTER)        
        self.box_titulo_spinner.append(self.label_box1)
        self.box_titulo_spinner.append(self.spinner)

        #BOX ALCOHOLI/CATEGORIA
        self.box_alc_cat = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=40, halign=Gtk.Align.CENTER)        
        self.box_alc_cat.append(self.box_filters1)
        self.box_alc_cat.append(self.box_filters2)

        #BOX TODOS LOS FILTROS
        self.box_filtros = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, halign=Gtk.Align.CENTER)        
        self.box_filtros.append(self.box_alc_cat)
        self.box_filtros.append(self.grid_letters)
        self.box_filtros.set_visible(False)

        #SCROLL FILTROS
        self.scroll_filtros = Gtk.ScrolledWindow(
            hexpand= False,
            vexpand= True,
            has_frame = False,
            halign= Gtk.Align.BASELINE,
            window_placement = Gtk.CornerType.TOP_LEFT
        )
        self.scroll_filtros.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll_filtros.set_child(self.box_filtros)

        #BOX CATALOGO
        self.box_catalog = Gtk.Box(orientation=Gtk.Orientation.VERTICAL) 
        self.box_catalog.append(self.box_titulo_spinner)
        self.box_catalog.append(self.scroll)

        #CUADRÍCULA DE LA VENTANA
        self.grid_global = Gtk.Grid()
        self.grid_global.attach(self.grid_search_bar, 0, 0, 2, 1)
        self.grid_global.attach(self.box_catalog, 0, 1, 1, 1)
        self.grid_global.attach(self.scroll_filtros, 1, 1, 1, 1)

        win.set_child(self.grid_global)
        self.handler.get_catalog()
        win.present()