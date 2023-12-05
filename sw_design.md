# Diseño software

<!-- ## Notas para el desarrollo de este documento
En este fichero debeis documentar el diseño software de la práctica.

> :warning: El diseño en un elemento "vivo". No olvideis actualizarlo
> a medida que cambia durante la realización de la práctica.

> :warning: Recordad que el diseño debe separar _vista_ y
> _estado/modelo_.
	 

El lenguaje de modelado es UML y debeis usar Mermaid para incluir los
diagramas dentro de este documento. Por ejemplo:
run(application_id: str, on_activate: Callable)
	clear_grid(grid: Grid)
	create_button_with_image(pixbuf, nombre: str)
-->
```mermaid
classDiagram
    class Model {
		__init__(): None
		get_catalog(): list
		download_image(url: str): bytes
		dividir_texto_en_lineas(texto: str,tamaño_de_linea: int): str
		get_info_ingredient(name: str): list
		get_info_drink(name: str, type): list
		get_details_product(id: str): list
		get_details_ingredient(id: str): list

	}
	class ViewHandler {
		on_search_clicked(name: str): None
    	on_random_clicked(): None
    	on_product_clicked(name: str): None
    	on_ingredient_clicked(name: str): None
    	on_letter_clicked(name: str): None
    	get_catalog(): None
	}
	class View {
		box_alc_cat: Box
		box_filters1: Box
		box_filters2: Box
		box_filtros: Box
		box_titulo_spinner: Box
		handler: ViewHandler 
		window: ApplicationWindow
		search_bar: SearchEntry
		box_catalog: Box
		image: Image
		image2: Image
		image3: Image
		image4: Image
		search_button: Button
		random_button: Button 
		home_button: Button 
		grid_global: Grid
		grid_search_bar: Grid
		grid_catalog: Grid
		grid_catalog_mini: Grid
		grid_letters: Grid
		label_box1: Label
		label_box2: Label
		label_box3: Label
		label_box4: Label
		spinner: Spinner
		scroll: ScrolledWindow
		scroll_description_mini: ScrolledWindow
		scroll_catalog_mini: ScrolledWindow
		scroll_image: ScrolledWindow
		scroll_filtros: ScrolledWindow

		__init__(): None
		on_activate(app: Gtk.Application): None
		set_handler(handler: ViewHandler): None
		set_grid_with_products(grid: Grid, detalles_productos: list): None
		set_grid_with_ingredients(grid: Grid, detalles_ingredientes: list): None
		update(detalles_productos: list): None
		see_details_products(detalles_producto: list): None
		see_details_ingredient(detalles_ingrediente: list): None
		build(app: Gtk.Application): None
		add_filter_button(label, func, filter_buttons, num, len, var): None
		buttons_sensitive(): None
		cat_to_var(name: str): str
		do_filtros(): None
		error_conexion(): None
		error_servidor(): None
		letters_sensitive(set): None
		on_toggled(num, len, state, array, var): None
		products_not_found(): None
		products_sensitive(grid, set): None
	}
	View o-- ViewHandler
	View ..> Gtk : << uses >>
	class Gtk
	<<package>> Gtk
	class Presenter {
		model: Model
		view: View

		__init__(model: Model, view: View): None
		run(application_id: str): None
		get_catalog(): None
		on_search_clicked(name: str): None
		on_letter_clicked(name: str): None
		on_random_clicked(): None
		on_product_clicked(id: str): None
		on_ingredient_clicked(id: str): None
		filter_list(name: str, op: int): list
		th_get_catalog(): None
		th_on_ingredient_clicked(id: str): None
		th_on_letter_clicked(name: str): None
		th_on_product_clicked(id: str): None
		th_on_random_clicked(): None
		th_on_search_clicked(name: str): None
	}
	Presenter o-- Model
	Presenter o-- View
```
```mermaid
sequenceDiagram
    actor User as User
    participant View as View
    participant Presenter as Presenter
    participant Model as Model
	participant TheCocktailDB
	autonumber

    User->>View: Introduce una palabra y pulsa buscar
    View->>Presenter: on_search_clicked()
    Presenter->>Model: get_info_drink()
    Model->>TheCocktailDB: requests.get(...)	
	TheCocktailDB-->>Model: Devuelve datos del producto
	Model-->>Presenter: return [...]
    Presenter-->>View: update()
	View-->>User: Ve los resultados

	alt Error de conexión
		Model--xTheCocktailDB: requests.exceptions.RequestException
        Model-->>Presenter: return 400
        Presenter-->>View: error_conexion()
		View-->>User: Ve mensaje error
    else Error en la respuesta del servicio
        TheCocktailDB-->>Model: requests.exceptions.HTTPError
        Model-->>Presenter: return 500
        Presenter-->>View: error_servidor()
		View-->>User: Ve mensaje error
	else Error de no encontrado
		TheCocktailDB-->>Model: No se encuentra en BBDD
		Model-->>Presenter: return []
        Presenter-->>View: update()
		View-->>User: Ve mensaje error
    end
```

