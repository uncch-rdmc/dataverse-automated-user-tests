import jinja2
from text import * #Imports a text variable that stores our strings
environment = jinja2.Environment(loader=jinja2.FileSystemLoader("python/html/")) #TODO: Figure out how to do paths better?
template = environment.get_template("template.html")

#print(template.render(**text))

with open('output.html', 'w') as f:
    f.write(template.render(**text))

print("rendered")