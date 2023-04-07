import jinja2, sys
from python.html.text import *
from ..tests import test_ingest_workflow_report as t
#import html.text #Imports a text variable that stores our strings

def main():
    if sys.version_info < (3, 7):
        print("Code requires Python 3.7 or later for ordered dictionaries")
        print("Exiting...")
        sys.exit(1)

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader("python/html/")) #TODO: Figure out how to do paths better?
    template = environment.get_template("template.html")


    ingest_test = t.IngestWorkflowReportTestCase(screenshots=True)
    ingest_test.setUp()
    result = ingest_test.test_requirements()
    ingest_test.tearDown()

    #print(template.render(**text))

    with open('output.html', 'w') as f:
        #f.write(template.render(**text))
        # print(result)
        f.write(template.render(text=text, screenshots=result)) #we want them in the dictionary for template iteration

    print("rendered")

if __name__ == "__main__":
    print(__package__)
    main()