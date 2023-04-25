import jinja2, sys, traceback, datetime
from python.html.text import *
from ..tests import test_ingest_workflow_report as t
#import html.text #Imports a text variable that stores our strings

def main():
    if sys.version_info < (3, 7):
        print("Code requires Python 3.7 or later for ordered dictionaries")
        print("Exiting...")
        sys.exit(1)

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader("python/html/")) #TODO: Figure out how to do paths better?
    environment.globals['index_with_default'] = index_with_default
    environment.globals['datetime'] = datetime.datetime
    template = environment.get_template("template.html")

    ingest_test = t.IngestWorkflowReportTestCase(do_screenshots=True, test_files=True)
    ingest_test.setUp()
    try:
        ingest_test.test_requirements()
        failure = False
    except Exception as e:
        failure = True
        traceback.print_exc()
    ingest_test.tearDown()

    with open('output.html', 'w') as f:
        #f.write(template.render(**text))
        # print(result)
        print("Last Req: " + ingest_test.req)
        print("Last Part: " + ingest_test.part)
        print("Was Failure: " + str(failure))
        f.write(template.render(text = text, 
                                screenshots = ingest_test.screenshots, 
                                start_times = ingest_test.start_times,
                                end_times = ingest_test.end_times,
                                info = ingest_test.info, 
                                last_req = int(ingest_test.req),
                                last_part = int(ingest_test.part),
                                test_order = ingest_test.test_order,
                                failure = failure)) #we want them in the dictionary for template iteration

    print("rendered")


# This custom function we add to jinja. It checks if an element is in a list, and if not returns a high number
# This is because our failed tests won't be added to the list, so functionally we consider them late enough that they failed
def index_with_default(alist, entry):
    try:
        return alist.index(entry)
    except Exception:
        return 99999
    

if __name__ == "__main__":
    #print(__package__)
    main()