import time, unittest, os, requests, re
from io import BytesIO
from urllib import parse
from python.tests.mixins.dataverse_testing_mixin import *
from python.tests.mixins.dataset_testing_mixin import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from webdriver_manager.chrome import ChromeDriverManager

#NOTE: Our use of step in the code is for screenshot taking. Sometimes the code to confirm a step happens after another step has been done.

#Note: I was seeing duplicate templates early into porting the code. I think its resolved but be aware
class IngestWorkflowReportTestCase(unittest.TestCase, DataverseTestingMixin, DatasetTestingMixin):
    def __init__(self, *args, **kwargs):
        self.capture = kwargs.pop('capture', False)
        super(IngestWorkflowReportTestCase, self).__init__( *args, **kwargs)

    def setUp(self):
        self.username = os.getenv('DATAVERSE_TEST_USER_USERNAME_BUILTIN')
        self.password = os.getenv('DATAVERSE_TEST_USER_PASSWORD_BUILTIN')
        self.dv_url = os.getenv('DATAVERSE_SERVER_URL')
        self.default_wait = 2
        #self.failed = False #TODO: Delete?
        self.api_token = None

        options = Options()
        #options.add_experimental_option("detach", True) #To keep browser window open. Trying this to get closer to writing test code without rerunning the full test
        self.sesh = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        if self.capture:
            self.sesh.set_window_size(1200,827) #675 should be the height with the screenshot not including the top/bottom bar. At least with chrome v111
        
        # #after starting, open a new one to an old one https://stackoverflow.com/questions/8344776/
        # self.sesh = webdriver.Remote(command_executor='http://localhost:54570', desired_capabilities={})
        # self.sesh.close()
        # self.sesh.session_id = 'a79265e4e877361e9a3b36ded43e3f7d'
        # time.sleep(999999)
        # print(f"Selenium command_executor url: {self.sesh.command_executor._url}")
        # print(f"Selenium session id: {self.sesh.session_id}")

        self.sesh.implicitly_wait(20) #Set high for dataset publish. Maybe we should keep it low normally and set it up when needed?

    def tearDown(self):
        self.delete_dv_resources(self.dataset_id, self.dataverse_id)

    #TODO: Maybe add some options to these functions to slim down some of the tests. For example, dataset template instructions which take forever. 
    def test_requirements(self):
        screenshots = {}
        screenshots.update(self.r01alt_mainpath_builtin_auth())
        self.get_api_token()
        screenshots.update(self.r03_mainpath_create_sub_dataverse())
        # screenshots.update(self.r04_mainpath_edit_dataverse())
        # screenshots.update(self.r05_mainpath_create_metadata_template())
        # screenshots.update(self.r06_mainpath_edit_metadata_template())
        # screenshots.update(self.r09_mainpath_create_dataset())
        # screenshots.update(self.r10_mainpath_edit_dataset())
        print("Tests Complete")

        #TODO: We may need to sort the screenshots by key if we have to add any out of order

        return screenshots

    #Written to allow calling these deletes directly for cleanup outside of the normal test run
    def delete_dv_resources(self, ds_id=None, dv_id=None):
        headers = {'X-Dataverse-key': self.api_token}
        if ds_id is not None:
            try:
                resp_ds_destroy = requests.delete(f'{self.dv_url}/api/datasets/{ds_id}/destroy', headers=headers)
                # print(resp_ds_destroy)
            except Exception as e:
                print("Unable to destroy dataset on tearDown. Error: " + e)
        if dv_id is not None:
            try:
                #resp_dv_delete = requests.delete(f'{self.dv_url}/api/dataverses/{self.dataverse_name}', headers=headers)
                resp_dv_delete = requests.delete(f'{self.dv_url}/api/dataverses/{dv_id}', headers=headers)
                # print(resp_dv_delete)
            except Exception as e:
                print("Unable to delete dataverse on tearDown. Error: " + e)

    ######################
    ### SUB-TEST CALLS ###
    ######################

    def r01alt_mainpath_builtin_auth(self):
        results = {}
        req = 'r01alt'

        part = '01'

        print(self.dv_url)
        self.sesh.get(f'{self.dv_url}/loginpage.xhtml?redirectPage=%2Fdataverse.xhtml')
        self.sesh.find_element('xpath', '//*[@id="loginForm:credentialsContainer:0:credValue"]').send_keys(self.username)
        self.sesh.find_element('xpath', '//*[@id="loginForm:credentialsContainer:1:sCredValue"]').send_keys(self.password)
        self.sesh.find_element('xpath', '//*[@id="loginForm:login"]').click()
        
        self.sesh.find_element('xpath', '//*[@id="dataverseDesc"]') #Find element to wait for load
        self.assertEqual(f'{self.dv_url}/dataverse.xhtml', self.sesh.current_url)

        #if self.screenshots: results['screenshot1'] = self.sesh.get_screenshot_as_base64()

        return results

    def get_api_token(self):
        #Note: This code assumes you have already clicked "Create Token" with this account.
        self.sesh.get(f'{self.dv_url}/dataverseuser.xhtml?selectTab=apiTokenTab')
        self.api_token = self.sesh.find_element('xpath', '//*[@id="apiToken"]/pre/code').text


        return {}
    
    def r03_mainpath_create_sub_dataverse(self):
        results = {}
        req = 'r03'
        shot = 0

        part = '01'

        ### Main Landing Page ###
        self.sesh.get(self.dv_url)

        self.sesh.find_element('xpath', '//*[@id="addDataForm"]/div/button').click() #click add data
        take_screenshot(self.capture, self.sesh, results, req, part, shot:=1)

        part = '02'
        self.sesh.find_element('xpath', '//*[@id="addDataForm"]/div/ul/li[1]/a').click() #click new dataverse
        take_screenshot(self.capture, self.sesh, results, req, part, shot:=1)

        ### Create Dataverse Page ###
        part = '03'
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:selectHostDataverse_input"]').clear()
        take_screenshot(self.capture, self.sesh, results, req, part, shot:=1)
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:selectHostDataverse_input"]').send_keys(self.dv_props["host_dataverse"])
        time.sleep(2) # wait for host list to load
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:selectHostDataverse_input"]').send_keys(Keys.ENTER)
        time.sleep(1) # wait after click for ui to be usable
        self.set_dataverse_metadata(add_string="create") #Metadata that is same for create/edit
        if self.capture:
            for i in range(3):
                self.sesh.execute_script(f"window.scrollTo(0, {i*500})") 
                take_screenshot(self.capture, self.sesh, results, req, part, shot:=shot+1)
        part = '04'
        self.sesh.find_element('xpath','//*[@id="dataverseForm:save"]').click() #create dataverse

        ### Test Save ###
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div').get_attribute("class"), "alert alert-success") #confirm success alert
        self.assertEqual(self.dv_url+'/dataverse/'+self.dataverse_name+'/', self.sesh.current_url) #confirm page
        take_screenshot(self.capture, self.sesh, results, req, part, shot:=1)

        self.confirm_dataverse_metadata(add_string="create")
        self.sesh.get(self.dv_url+'/dataverse/'+self.dataverse_name)
        
        ### Dataverse Page - Publish ###
        part = '05'
        self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div/div/div[2]/button').click() #click publish
        take_screenshot(self.capture, self.sesh, results, req, part, shot:=1)
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:j_idt431"]').click() #confirm publish
        take_screenshot(self.capture, self.sesh, results, req, part, shot:=shot+1)
        
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div').get_attribute("class"), "alert alert-success") #confirm success alert
        take_screenshot(self.capture, self.sesh, results, req, part, shot:=shot+1)

        self.dataverse_id = re.sub(".*=", "", self.sesh.find_element('xpath', '//*[@id="dataverseForm:themeWidgetsOpts"]').get_attribute("href")) 

        return results

    def r04_mainpath_edit_dataverse(self):
        results = {}
        req = 'r04'

        part = '01'

        self.sesh.get(self.dv_url+'/dataverse/'+self.dataverse_name)
        time.sleep(self.default_wait)
        self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div/div/div[2]/div[2]/button').click()
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:editInfo"]').click()
        
        self.set_dataverse_metadata()
        self.sesh.find_element('xpath','//*[@id="dataverseForm:save"]').click() #create dataverse
        time.sleep(self.default_wait) # I think our code is picking up on the previous page div, so we wait before getting the div
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div').get_attribute("class"), "alert alert-success") #confirm success alert

        #print(self.dv_url + '/dataverse/' + self.dataverse_name + '/')
        # self.sesh.get(self.dv_url + '/dataverse/' + self.dataverse_name + '/')
        # time.sleep(self.default_wait)
        self.confirm_dataverse_metadata()
        
        time.sleep(1) #wait before switching pages in r05

        return results
    
    def r05_mainpath_create_metadata_template(self):
        results = {}
        req = 'r05'

        part = '01'

        self.sesh.get(self.dv_url+'/dataverse/'+self.dataverse_name)
        time.sleep(self.default_wait)
    
        self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div/div/div[2]/div[2]/button').click() #click dataverse edit button
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:manageTemplates"]').click() #click manage templates
        time.sleep(self.default_wait)
        self.sesh.find_element('xpath', '//*[@id="manageTemplatesForm"]/div[1]/div/a').click() #click create dataset template
        time.sleep(self.default_wait)
        self.sesh.find_element('xpath', '//*[@id="templateForm:templateName"]').send_keys("test template create") #Create template title
        self.set_dataset_metadata_template_instructions(add_string='create')
        #This chunk of code is weird. We were having issues with a page click being intercepted, so to handle that we are clicking a dropdown twice
        #We use javascript for this as it allows us to not care about the click interception.
        #I've tried clicking non dropdown elements and it doesn't clear the capture
        time.sleep(1)
        self.sesh.execute_script('document.evaluate(\'//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:2:cvv"]/div[3]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        time.sleep(1)
        self.sesh.execute_script('document.evaluate(\'//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:2:cvv"]/div[3]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        time.sleep(1)
        #self.sesh.find_element('xpath', '//*[@id="templateForm:editMetadataFragement"]').click() #click background to clear any open dropdowns
        self.set_dataset_metadata_edit(add_string='create', xpath_dict=self.ds_template_xpaths)

        # self.sesh.find_element('xpath', '//*[@id="templateForm:j_idt892"]').click()
        # time.sleep(.2)
        # #TODO: What?
        # self.sesh.switch_to.active_element.send_keys("test"+"WOWOWOWOW")
        # time.sleep(999999)
        
        #TODO: I think here it where I was setting license but didn't finish?
        
        self.sesh.find_element('xpath', '//*[@id="templateForm:j_idt892"]').click() #click "Save + Add Terms"
    
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") #confirm success alert
        
        #TODO: Replace param_get with a new way to get the query params from a url
        self.template_id = parse.parse_qs(parse.urlparse(self.sesh.current_url).query)['id'][0]#<<- param_get(self.sesh.current_url, "id")
    
        self.set_template_license(add_string='create')
        self.sesh.find_element('xpath', '//*[@id="templateForm:j_idt893"]').click() #click "Save Dataset Template" (which actually just saves the license)
        
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") #confirm success alert
        time.sleep(self.default_wait) #not sure why I have to do this but ok? Shouldn't confirming the alert work?
        
        self.sesh.get(self.dv_url+'/template.xhtml?id='+self.template_id+'&ownerId='+self.dataverse_id+'&editMode=METADATA')
        self.confirm_dataset_metadata(add_string='create', xpath_dict=self.ds_template_xpaths)
        self.confirm_dataset_metadata_template_instructions(add_string='create')

        self.sesh.get(self.dv_url+'/template.xhtml?id='+self.template_id+'&ownerId='+self.dataverse_id+'&editMode=LICENSE')
        self.confirm_template_license(add_string='create')

        return results
    
    def r06_mainpath_edit_metadata_template(self):
        results = {}
        req = 'r06'

        part = '01'

        self.sesh.get(self.dv_url+'/template.xhtml?id='+self.template_id+'&ownerId='+self.dataverse_id+'&editMode=METADATA')
        self.set_dataset_metadata_template_instructions(add_string='edit')
        #See note in R05 about the similar code
        time.sleep(1)
        self.sesh.execute_script('document.evaluate(\'//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:2:cvv"]/div[3]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        time.sleep(1)
        self.sesh.execute_script('document.evaluate(\'//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:2:cvv"]/div[3]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        time.sleep(1)        
        self.set_dataset_metadata_edit(add_string='edit', xpath_dict=self.ds_template_xpaths)
        self.sesh.find_element('xpath', '//*[@id="templateForm:j_idt893"]').click() #click "Save + Add Terms"
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") #confirm success alert
        
        self.sesh.get(self.dv_url+'/template.xhtml?id='+self.template_id+'&ownerId='+self.dataverse_id+'&editMode=LICENSE')
        self.set_template_license(add_string='edit')
        self.sesh.find_element('xpath', '//*[@id="templateForm:j_idt893"]').click() #click "Save Changes"
        time.sleep(self.default_wait) #not sure why I have to do this but ok? Shouldn't confirming the alert work?
        
        self.sesh.get(self.dv_url+'/template.xhtml?id='+self.template_id+'&ownerId='+self.dataverse_id+'&editMode=METADATA')
        self.confirm_dataset_metadata(add_string='edit', xpath_dict=self.ds_template_xpaths)
        self.confirm_dataset_metadata_template_instructions(add_string='edit')

        self.sesh.get(self.dv_url+'/template.xhtml?id='+self.template_id+'&ownerId='+self.dataverse_id+'&editMode=LICENSE')
        self.confirm_template_license(add_string='edit')

        return results
    
    def r09_mainpath_create_dataset(self):
        results = {}
        req = 'r09'

        part = '01'
        
        self.sesh.get(self.dv_url+'/dataverse/'+self.dataverse_name)
        
        self.sesh.find_element('xpath', '//*[@id="addDataForm"]/div/button').click() #click add data
        self.sesh.find_element('xpath', '//*[@id="addDataForm"]/div/ul/li[2]/a').click() #click new dataset
        
        self.set_dataset_metadata_create(add_string='create')
        
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") #confirm success alert
        
        ### Get dataset id from permissions page url for later uses ###
        self.dataset_id = re.sub(".*=", "", self.sesh.find_element('xpath', '//*[@id="datasetForm:manageDatasetPermissions"]').get_attribute("href")) 
        # print(dataset_id)
        
        self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div[1]/div/a').click() #click publish
    
        self.sesh.find_element('xpath', '//*[@id="datasetForm:j_idt2547"]').click() #click publish confirm
    
        self.sesh.find_element('class name', 'label-default') #Find element to wait for load. May trigger prematurely with files added.
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="title-label-block"]/span').text, "Version 1.0") #Test dataset published
        
        self.sesh.find_element('xpath', '//*[@id="editDataSet"]').click() #click add data
        self.sesh.find_element('xpath', '//*[@id="datasetForm:editMetadata"]').click() #click edit dataset
        
        self.confirm_dataset_metadata(add_string='create', is_update=False, xpath_dict=self.ds_edit_xpaths)
        
        self.sesh.find_element('xpath', '//*[@id="datasetForm:cancel"]').click() #click out after testing data
        
        time.sleep(self.default_wait)

        return results
    
    def r10_mainpath_edit_dataset(self):
        results = {}
        req = 'r10'

        part = '01'
        
        self.sesh.find_element('xpath', '//*[@id="editDataSet"]').click() #click add data
        self.sesh.find_element('xpath', '//*[@id="datasetForm:editMetadata"]').click() #click new dataset
    
        self.set_dataset_metadata_edit(add_string='edit', xpath_dict=self.ds_edit_xpaths)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:saveBottom"]').click() #click to create dataset
    
        self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div[1]/div/a').click() #click publish
    
        self.sesh.find_element('xpath', '//*[@id="datasetForm:j_idt2547"]').click() #click publish confirm
        
        self.sesh.find_element('class name', 'label-default') #Find element to wait for load. May trigger prematurely with files added.
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="title-label-block"]/span').text, "Version 1.1") #Test dataset published
        
        self.sesh.find_element('xpath', '//*[@id="editDataSet"]').click() #click add data
        self.sesh.find_element('xpath', '//*[@id="datasetForm:editMetadata"]').click() #click new dataset
        
        self.confirm_dataset_metadata(add_string='edit', is_update=True, xpath_dict=self.ds_edit_xpaths) 
    
        self.sesh.find_element('xpath', '//*[@id="datasetForm:cancelTop"]').click() #click cancel out of edit after testing

        return results

#NOTE: Maybe this should be switched back to a class function, but I find it a bit more readable in the code to be separate. 
def take_screenshot(enable, sesh, dict, req, part, shot):
    if enable: 
        dict[f'{req}_p{part}_s{"%02d" % (shot)}'] = sesh.get_screenshot_as_base64()

