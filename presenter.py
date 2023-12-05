from view import View, run
from model import Model

import threading
from gi.repository import GLib


class Presenter:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view

    def run(self, application_id) -> None:
        self.view.set_handler(self)
        run(application_id=application_id, on_activate=self.view.on_activate)

    def get_catalog(self) -> None:
        threading.Thread(target = self.th_get_catalog, daemon=True).start()
    def th_get_catalog(self) -> None:
        GLib.idle_add(self._waiting)
        result = self.model.get_catalog()
        if result != 400:
            GLib.idle_add(self.view.update, result)
        elif result == 400:
            GLib.idle_add(self.view.error_conexion)
        else:
            GLib.idle_add(self.view.error_servidor)

    def on_search_clicked(self, name) -> None:
        threading.Thread(target = self.th_on_search_clicked, args=(name, ), daemon=True).start()
    def th_on_search_clicked(self, name: str) -> None:
        GLib.idle_add(self._waiting)
        result = self.model.get_info_drink(name, "search", self.view.alc, self.view.cat, None)
        if result != 400:
            GLib.idle_add(self.view.update, result)
        elif result == 400:
            GLib.idle_add(self.view.error_conexion)
        else:
            GLib.idle_add(self.view.error_servidor)

    def on_letter_clicked(self, name) -> None:
        threading.Thread(target = self.th_on_letter_clicked, args=(name, ), daemon=True).start()
    def th_on_letter_clicked(self, name: str) -> None:
        GLib.idle_add(self._waiting)
        result = self.model.get_info_drink(name, "letter", self.view.alc, self.view.cat, None)
        if result != 400:
            GLib.idle_add(self.view.update, result)
        elif result == 400:
            GLib.idle_add(self.view.error_conexion)
        else:
            GLib.idle_add(self.view.error_servidor)
    

    def on_random_clicked(self) -> None:
        threading.Thread(target = self.th_on_random_clicked, daemon=True).start()
    def th_on_random_clicked(self) -> None:
        GLib.idle_add(self._waiting)
        for bot in self.view.filter_buttons1:
            bot.set_active(False)
        for bot in self.view.filter_buttons2:
            bot.set_active(False)
        self.view.alc=""
        self.view.cat=""
        info_drink = self.model.get_info_drink(None, "random", "", "", None)
        if info_drink != 400:
            result = self.model.get_details_product(info_drink[0][2])
        elif info_drink == 400:
            GLib.idle_add(self.view.error_conexion)
        else:
            GLib.idle_add(self.view.error_servidor)

        if result != 400:
            GLib.idle_add(self.view.see_details_product, result)
        elif result == 400:
            GLib.idle_add(self.view.error_conexion)
        else:
            GLib.idle_add(self.view.error_servidor)
    
    def on_product_clicked(self, id) -> None:
        threading.Thread(target = self.th_on_product_clicked, args=(id, ), daemon=True).start()
    def th_on_product_clicked(self, id: str) -> None:
        GLib.idle_add(self._waiting)
        result = self.model.get_details_product(id)
        if result != 400:
            GLib.idle_add(self.view.see_details_product, result)
        elif result == 400:
            GLib.idle_add(self.view.error_conexion)
        else:
            GLib.idle_add(self.view.error_servidor)

    def on_ingredient_clicked(self, id) -> None:
        threading.Thread(target = self.th_on_ingredient_clicked, args=(id, ), daemon=True).start()
    def th_on_ingredient_clicked(self, id: str) -> None:
        GLib.idle_add(self._waiting)
        result = self.model.get_details_ingredient(id)
        if result != 400:
            GLib.idle_add(self.view.see_details_ingredient, result)
        elif result == 400:
            GLib.idle_add(self.view.error_conexion)
        else:
            GLib.idle_add(self.view.error_servidor)

    def filter_list(self, name, op) -> list:
        result = self.model.get_info_drink(name, "category", None, None, op)
        return result

    def _waiting(self) -> None:
        self.view.spinner.start()
        self.view.search_button.set_sensitive(False)
        self.view.search_bar.set_sensitive(False)
        self.view.random_button.set_sensitive(False)
        self.view.home_button.set_sensitive(False)
        self.view.filter_button.set_sensitive(False)
        self.view.letters_sensitive(False)
        self.view.products_sensitive(self.view.grid_catalog, False)
        self.view.products_sensitive(self.view.grid_catalog_mini, False)
        