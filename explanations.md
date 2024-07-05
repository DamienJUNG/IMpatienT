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

## General architecture


```
.
├── app.py          <-------- The main script, use it to lauch the server
├── assets          <-------- Store the css and js files, **everything** inside this file is accessible by url
│   ├── app.css
│   ├── banner.png
│   ├── collapse_tree.css
│   ├── collapse_tree.js
│   ├── cross_to_down.png
│   └── cross_to_right.png
├── callbacks       <-------- Store the global callbacks and the auth callbacks
│   ├── auth_callback.py
│   ├── base.py
│   ├── callback_loader.py
│   └── layout_callback.py
├── components      <-------- Some components and scripts used inside the app
│   ├── collapse_tree_node.py
│   ├── collapse_tree_root.py
│   └── orphanet_parser.py
├── config.py       <-------- Used to config your project, contains the secret key **do not expose to others**
├── data            <-------- Contains all the data of the application 
│   ├── images
│   │   ├── 1012405.png
│   │   ├── 1101930.jpg
│   │   ├── 123_150521-oconnor-octopus-tease_zenfje.jpg
│   │   ├── 1322308.jpeg
│   │   ├── 149888.jpg
│   │   ├── 750953.jpg
│   │   ├── 794405.jpg
│   │   ├── 84348.jpg
│   │   ├── 851489.jpg
│   │   ├── 911910.jpg
│   │   ├── 946945.png
│   │   ├── 952541.png
│   │   ├── aaa_sample_image_histo.jpg
│   │   ├── aaa_sample_image_histo.jpg_blend_image.png
│   │   ├── aaa_sample_image_histo.jpg_mask_image.png
│   │   ├── abc_histo.jpg
│   │   ├── demodemodemo_sample_image_histo.jpg
│   │   ├── demodemodemo_sample_image_histo.jpg_blend_image.png
│   │   ├── demodemodemo_sample_image_histo.jpg_mask_image.png
│   │   ├── demodemo_sample_image_histo.jpg
│   │   ├── demodemo_sample_image_histo.jpg_blend_image.png
│   │   ├── demodemo_sample_image_histo.jpg_mask_image.png
│   │   ├── demo_patient_sample_image_histo.jpg
│   │   ├── demo_patient_sample_image_histo.jpg_blend_image.png
│   │   ├── demo_patient_sample_image_histo.jpg_mask_image.png
│   │   ├── demo_patient_Screenshot_470.jpg
│   │   ├── demo_sample_image_histo.jpg_blend_image.png
│   │   ├── demo_sample_image_histo.jpg_mask_image.png
│   │   ├── jjj_sample_image_histo.jpg
│   │   ├── jjj_sample_image_histo.jpg_blend_image.png
│   │   ├── jjj_sample_image_histo.jpg_mask_image.png
│   │   ├── teeeeeeeeeeeeeeeeeeeeeeeest.png
│   │   └── test_no_blend.png
│   ├── masks   <-------- Contains .masks files which represents annotation shapes  
│   │   ├── aaa_sample_image_histo.masks
│   │   ├── demodemo_sample_image_histo.masks
│   │   └── teeeeeeeeeeeeeeeeeeeeeeeest.masks
│   ├── ontology
│   │   ├── ontology_default.json
│   │   ├── ontology.json.demo
│   │   └── ontology.json.dvc
│   ├── text_reports.csv
│   └── vocab_list
│       ├── negex_en.txt
│       ├── negex_fr.txt
│       ├── negex_sep_en.txt
│       └── negex_sep_fr.txt
├── database    <-------- Contains everything which is related to database, from models to CRUDs operation
│   ├── db.py
│   ├── images.py
│   ├── models.py
│   ├── modules.py
│   ├── pages.py
│   ├── projects.py
│   ├── reports.py
│   ├── roles.py
│   ├── sqlite.db
│   └── users.py
├── Dockerfile      <-------- Used to set up docker images
├── en_product3_146.json
├── explanations.md
├── hp.json
├── makefile
├── ontology.json
├── package-lock.json
├── pages           <-------- Contains all python pages
│   ├── annotate_image.py
│   ├── create_image.py
│   ├── create_user.py
│   ├── home.py
│   ├── image_annotation.py
│   ├── log_in.py
│   ├── patient.py
│   ├── projects.py
│   ├── reports.py
│   ├── settings.py
│   ├── view_project.py
│   ├── visualisation_dashboard.py
│   └── vocabulary.py
├── pyproject.toml
├── README.md
├── requirements.txt
├── test.json
├── todo.md
└── utils           <-------- Contains all the utils functions used inside the app
    ├── common_func.py
    ├── ocr.py
    ├── plot_common.py
    ├── shapes_to_segmentations.py
    ├── shape_utils.py
    └── trainable_segmentation.py

```
