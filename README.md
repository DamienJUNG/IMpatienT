[![Build](https://github.com/lambda-science/IMPatienT/actions/workflows/docker-build-push.yml/badge.svg)](https://github.com/lambda-science/IMPatienT/actions/workflows/docker-build-push.yml) ![GitHub last commit](https://img.shields.io/github/last-commit/DamienJUNG/impatient) ![GitHub](https://img.shields.io/github/license/DamienJUNG/IMPatienT)

# IMPatienT 🗂️: an integrated web application to digitize, process and explore multimodal patient data.

<p align="center">
  <img src="https://i.imgur.com/iH7UeUs.png" alt="IMPatienT Banner" style="border-radius: 25px;" />
</p>

**IMPatienT 🗂️** (**I**ntegrated digital **M**ultimodal **PATIEN**t da**T**a) **is a web application developped in the MYO-xIA project for patient data digitization and exploration.**
It features a standard vocabulary creator, optical character recognition (OCR), natural language processing (NLP), image annotation and segmentation using machine learning, interactive visualizations and automatic diagnosis suggestion.

This project was carried out during my internship at [**CRBS**](https://crbs.unistra.fr).
It's based on [**Corentin Meyer**](https://cmeyer.fr)'s project, but has been entirely rewritten in Dash.

[**Corentin Meyer's repository**](https://github.com/lambda-science/IMPatienT/tree/main)

## Contact:

The main maintainer is:
[**Corentin Meyer** - PhD in Biomedical AI](https://cmeyer.fr) <contact@cmeyer.fr>


## IMPatienT🗂️ Abstract

**Background**  
Medical acts, such as imaging, generally lead to the production of several medical text reports that describe the relevant findings. Such processes induce multimodality in patient data by linking image data to free-text data and consequently, multimodal data have become central to drive research and improve diagnosis of patients. However, the exploitation of patient data is challenging as the ecosystem of available analysis tools is fragmented depending on the type of data (images, text, genetic sequences), the task to be performed (digitization, processing, exploration) and the domain of interest (clinical phenotype, histology…). To address the challenges, the analysis tools need to be integrated in a simple, comprehensive, and flexible platform.  
**Results**  
Here, we present IMPatienT (**I**ntegrated digital **M**ultimodal **PATIEN**t da**T**a), a free and open-source web application to digitize, process and explore multimodal patient data. IMPatienT has a modular architecture, including four components to: (i) create a standard vocabulary for a domain, (ii) digitize and process free-text data by mapping it to a set of standard terms, (iii) annotate images and perform image segmentation, and (iv) generate an automatic visualization dashboard to provide insight on the data and perform automatic diagnosis suggestions. Finally, we demonstrate the usefulness of IMPatienT on a corpus of 40 simulated muscle biopsy reports of congenital myopathy patients.  
**Conclusions**  
IMPatienT is a platform to digitize, process and explore patient data that can handle image and free-text data. As it relies on a user-designed vocabulary, it can be adapted to fit any domain of research and can be used as a patient registry for exploratory data analysis (EDA).

## Guide

[Explanations of project files]()

## Setup guides

### (DOCKER) Developper Mode Setup (to contribute)

[See the wiki page: Developper Mode Setup (DOCKER)](<https://github.com/lambda-science/IMPatienT/wiki/(DOCKER)-Developper-Mode-Setup-(to-contribute)>)