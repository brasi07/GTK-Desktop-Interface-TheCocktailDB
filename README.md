# Graphic Desktop App for TheCocktailDB API

This is a small graphic desktop application built with Python and utilizing the GTK library. It uses TheCocktailDB API in its free version and is designed based on the Model-View-Presenter (MVP) pattern to effectively manage the application state.

<h1> Features </h1>

- Utilizes TheCocktailDB API to fetch cocktail-related information.

- Follows the *MVP* pattern for a clear and organized structure.

- Implements _concurrent_ operations management for optimizing critical processes and prevent the app from crashing.

- The application is internationalized and adapts to the user's _locale_ settings. An English translation is provided.

<h1> Getting started </h1>

- Run the app by using this command:
  ```bash
  python3 App.py
  ```
- Test internationalization by using this command:
  ```bash
  LC_ALL=en_US.utf8 python3 App.py
  ```
