    Although this still works, the better approach would now be use a static site generator 
    (I also built one called Sitegen) and host it at Netlify, Github Pages, S3, or
    any web server.
    
 Go to [sitegen](https://github.com/altlimit/sitegen)

app-engine-static
==================

This project will help you create static websites quickly with the power of jinja2 templating system you can
build your sites with layouts/macros and anything that jinja supports then generate your static html files.

Summary of things::

    gen/ - this will contain all your html generated files
    static/ - put your styles/images/javascript and any other static files here
    templates/ - jinja2 templates goes here and will also generate site structure base on your folders here
    generate.py - execute this to update your static site

On development you access your dynamic site at http://localhost:8080/dev/ and all template files/folder starting
with _ are skipped, useful for layouts.


Demo: http://static.altlimit-test.appspot.com/
