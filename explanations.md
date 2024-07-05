The purpose of this file is to explain and justify certain aspects of the project code.

## Pages model

The first thing you might notice is that pages all as the same model, they are classes containing a get_layout function and a registered_callbacks one.
This as been done in order to harmonise the pages and make them all identical.

The goal was to make page management really easy, and also because mutli-pages from Dash couldn't work with Flask-Login.
To add a new page you just have to put write it inside the pages folder and the page will be served.
The new page will also be registered inside sqlite database, but you won't be able to access to this page until you grant your role the right to access to it (you can do this in the settings page, while the server is running).

[This file](app.py) is the main of the application, it will set up all the configuration and save all pages, and use all the registered_callbacks functions, in order to work the Dash server ignore callbacks expections, so all callbacks of all pages are created.

This mean that you **can't** identify 2 different components with the exact same id. 

## Page loading

When a request is made to the application, it will look for the page with the corresponding name inside the pages folder.

You can see the code [here](callbacks/layout_callback.py) inside the first callback, this file contains all the general purpose callbacks related to general or components behaviour.

If you create a new page make sure to apply the same model, otherwise the loader will not find the layout and you won't be able to use your page.

## Authentication

In order to acces to the others pages you will have to authenticate, you will find the redirection code [here](callbacks/auth_callback.py)
