from model import Model
from view import View
from presenter import Presenter

import locale
import gettext

if __name__ == "__main__":

    locale.setlocale(locale.LC_ALL, '')
    LOCALE_DIR = "./locales"
    locale.bindtextdomain('App', LOCALE_DIR)
    gettext.bindtextdomain('App', LOCALE_DIR)
    gettext.textdomain('App')

    presenter = Presenter(model=Model(), view=View())
    presenter.run(application_id="es.udc.fic.ipm.App")
