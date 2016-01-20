# Overview

This is the main repo for Advoclik, a TGG Company.

# Technical description

## Overview

Our stack looks as follows:

* Back-end: Django
* Database: MySQL
* Front-end:
  * Styling using Bootstrap
  * We add functionality with JQuery and other JS helpers
* Hosting: Not yet decided
* Virtual machine: Vagrant

## Folder organization

* The main folder contains the files to set up Vagrant
* The Django project is contained in [www-source/advoclik](www-source/advoclik). The folder organization in this folder follows the general Django conventions.

## Setting up the stack

The stack is set up through Vagrant. We follow the template laid out in [our Vagrant documentation](https://github.com/TGGgroup/TGG-tech/blob/master/vagrant/Vagrant%20on%20laptops.md). The only difference is that, instead of using the app `django_polls`, we use `advoclik`.
