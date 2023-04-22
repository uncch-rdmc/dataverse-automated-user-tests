import time, unittest, os, requests, re
from datetime import datetime
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
        self.do_screenshots = kwargs.pop('do_screenshots', False)
        self.test_files = kwargs.pop('test_files', True) #NOTE: Disabling files will currently change the requirements for some test parts
        super(IngestWorkflowReportTestCase, self).__init__( *args, **kwargs)

    def setUp(self):
        self.username = os.getenv('DATAVERSE_TEST_USER_USERNAME')
        self.password = os.getenv('DATAVERSE_TEST_USER_PASSWORD_BUILTIN')
        self.dv_url = os.getenv('DATAVERSE_SERVER_URL')
        self.perm_test_username = os.getenv('DATAVERSE_USERNAME_FOR_PERM_TEST')
        self.sso_option_value = os.getenv('DATAVERSE_SSO_OPTION_VALUE')
        self.default_wait = 2
        self.scroll_height = 600 #For scrolling with screenshots
        #self.failed = False #TODO: Delete?
        self.api_token = None
        self.templates_exist = False
        self.browser_type = "Chrome"
        self.req = None
        self.part = None
        self.screenshots = {}
        self.start_times = {}
        self.end_times = {}
        self.info = {}
        self.test_order = []

        self.test_file_1_md5 = 'MD5: a5890ace30a3e84d9118196c161aeec2'
        self.test_file_1_replace_md5 = 'MD5: 07436de69e3283065a2453322ee22ba3'
        self.test_file_2_md5 = 'MD5: c7803e4497be4984e41102e1b2ef64cc'

        self.role_alias = "test_role_auto"

        options = Options()
        #options.add_experimental_option("detach", True) #To keep browser window open. Trying this to get closer to writing test code without rerunning the full test
        if self.browser_type == "Chrome":
            self.sesh = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        if self.do_screenshots:
            self.sesh.set_window_size(1200,827) #675 should be the height with the screenshot not including the top/bottom bar. At least with chrome v111
        
        # #after starting, open a new one to an old one https://stackoverflow.com/questions/8344776/
        # self.sesh = webdriver.Remote(command_executor='http://localhost:54570', desired_capabilities={})
        # self.sesh.close()
        # self.sesh.session_id = 'a79265e4e877361e9a3b36ded43e3f7d'
        # time.sleep(999999)
        # print(f"Selenium command_executor url: {self.sesh.command_executor._url}")
        # print(f"Selenium session id: {self.sesh.session_id}")

        self.sesh.implicitly_wait(10)

    def tearDown(self):
        self.delete_dv_resources(self.dataset_id, self.dataverse_id, self.role_alias)


    #TODO: Maybe add some options to these functions to slim down some of the tests. For example, dataset template instructions which take forever. 
    def test_requirements(self):
        # I am assuming I'll have to give date-time and time-elapsed for each test, even if I'm not doing it to start
        # We need to show in the test exactly where the failure happened and then fail for everything after
        # - I am assuming that someday we may want to report in a more fine-tuned way, so maybe we should return failures for each step?

        self.info = self.get_testing_info()

        tests = [
            self.r01alt_mainpath_builtin_auth,
            self.get_api_token,
            #self.r01_mainpath_test_sso_auth,
            # self.r02_mainpath_add_user_group_role,
            # self.r03_mainpath_create_sub_dataverse,
            # self.r04_mainpath_edit_dataverse,
            # self.r05_mainpath_create_metadata_template,
            # self.r06_mainpath_edit_metadata_template,
            # self.r09r11r13r20_mainpath_create_dataset,
            # self.r10r12r15r16r17_mainpath_edit_dataset,
            self.r21_mainpath_search_dataset,
        ]
        for test in tests:
            test()
                
        
        print("Tests Complete")

    #Written to allow calling these deletes directly for cleanup outside of the normal test run
    def delete_dv_resources(self, ds_id=None, dv_id=None, role_alias=None):
        print("API TOKEN: " + self.api_token)
        headers = {'X-Dataverse-key': self.api_token}
        if ds_id is not None:
            try:
                resp_ds_destroy = requests.delete(f'{self.dv_url}/api/datasets/{ds_id}/destroy', headers=headers)
                print(resp_ds_destroy.__dict__)
            except Exception as e:
                print("Unable to destroy dataset on tearDown. Error: " + e)
        if dv_id is not None:
            try:
                #resp_dv_delete = requests.delete(f'{self.dv_url}/api/dataverses/{self.dataverse_name}', headers=headers)
                resp_dv_delete = requests.delete(f'{self.dv_url}/api/dataverses/{dv_id}', headers=headers)
                print(resp_dv_delete.__dict__)
            except Exception as e:
                print("Unable to delete dataverse on tearDown. Error: " + e)
        if role_alias is not None:
            try:
                resp_role_delete = requests.delete(f'{self.dv_url}/api/roles/:alias?alias={role_alias}', headers=headers)
                print(resp_role_delete.__dict__)
            except Exception as e:
                print("Unable to delete role on tearDown. Error: " + e)

    def get_dataverse_version(self):
        # $ curl http://localhost:8080/api/info/version
        # {"status":"OK","data":{"version":"5.13","build":"1244-79d6e57"}}
        try:
            dataverse_version = requests.get(f'{self.dv_url}/api/info/version')#, headers=headers)
            return dataverse_version.json()['data']['version']
        except Exception as e:
            print("Unable to get version of Dataverse install. Error: " + e)

    # We set the req this way so we can populate our real req order list for rendering.
    # We need to keep track of the actual order of the reqs to correctly fail tests that happened after a failure
    # This doesn't handle the edge case of requirements that have their parts broken up, but that's minor enough to ignore currently
    def set_req(self, r_num):
        self.req = r_num
        if r_num not in self.test_order:
            self.test_order.append(int(r_num))

    ######################
    ### SUB-TEST CALLS ###
    ######################

    def get_testing_info(self):
        info = {}
        info['dv_url'] = self.dv_url
        info['dv_version'] = self.get_dataverse_version()
        info['browser_version'] = self.browser_type + " " + self.sesh.capabilities['browserVersion']
        info['test_user'] = self.username
        info['test_date'] = datetime.now().strftime("%A, %B %d, %Y")

        return info

    def r01_mainpath_test_sso_auth(self):
        self.set_req('01')
        self.set_start_time()
        shot = 0

        self.part = '01'
        self.sesh.get(f'{self.dv_url}/loginpage.xhtml?redirectPage=%2Fdataverse.xhtml')
        self.sesh.find_element('xpath', '//*[@id="idpSelectIdPListTile"]/a')
        self.take_screenshot(shot:=1)

        self.part = '02'
        #self.sesh.find_element('xpath', '//*[@id="idpSelectSelector"]/option[2]').click()
        #print(self.sso_option_value)
        self.sesh.find_element('xpath', f"//option[@value='{self.sso_option_value}']").click() 
        #time.sleep(.1)
        self.take_screenshot(shot:=1)
        
        self.part = '03'
        self.sesh.find_element('xpath', '//*[@id="idpSelectListButton"]').click()
        time.sleep(2)
        self.take_screenshot(shot:=1)

        self.part = '04'
        self.sesh.implicitly_wait(3600)
        self.sesh.find_element('xpath', '//*[@id="dataverseDesc"]') #Find element to wait login to complete
        self.assertEqual(f'{self.dv_url}/dataverse.xhtml', self.sesh.current_url)
        self.take_screenshot(shot:=1)
        self.sesh.implicitly_wait(10)

        self.set_end_time()
            
    #TODO: This test doesn't actually fufill a req, should I rename it and stop doing req stuff?
    def r01alt_mainpath_builtin_auth(self):
        self.set_req('01')

        self.part = '01'

        #print(self.dv_url)
        self.sesh.get(f'{self.dv_url}/loginpage.xhtml?redirectPage=%2Fdataverse.xhtml')
        self.sesh.find_element('xpath', '//*[@id="loginForm:credentialsContainer:0:credValue"]').send_keys(self.username)
        self.sesh.find_element('xpath', '//*[@id="loginForm:credentialsContainer:1:sCredValue"]').send_keys(self.password)
        self.sesh.find_element('xpath', '//*[@id="loginForm:login"]').click()
        
        self.sesh.find_element('xpath', '//*[@id="dataverseDesc"]') #Find element to wait for load
        self.assertEqual(f'{self.dv_url}/dataverse.xhtml', self.sesh.current_url)

        
    def get_api_token(self):
        #We confirm we are the user we think we are. This is mostly for reporting purproses
        self.sesh.get(f'{self.dv_url}/dataverseuser.xhtml?selectTab=accountInfo')
        self.assertEqual(self.sesh.find_element('xpath', '/html/body/div[1]/form/div/div/div[3]/div[2]/table/tbody/tr[1]/td').text, self.username) 
        
        #Note: This code assumes you have already clicked "Create Token" with this account.
        self.sesh.get(f'{self.dv_url}/dataverseuser.xhtml?selectTab=apiTokenTab')
        self.api_token = self.sesh.find_element('xpath', '//*[@id="apiToken"]/pre/code').text 

        return {}

    #TODO: Maybe make this test act upon our created sub-dataverse instead. Clean up is slightly easier, but then the test relies on other tests
    def r02_mainpath_add_user_group_role(self):
        self.set_req('02')
        self.set_start_time()
        shot = 0

        self.part = '01'
        self.sesh.get(f'{self.dv_url}')
        time.sleep(1)
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div/div[2]/div[2]/div/button').click() #click edit
        time.sleep(.5)
        self.take_screenshot(shot:=shot+1)

        self.part = '02'
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:managePermissions"]').click()
        time.sleep(1)
        self.take_screenshot(shot:=1)

        self.part = '03'
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm"]/div[1]/div[3]').click()
        time.sleep(.5)
        self.take_screenshot(shot:=1)

        self.part = '04'
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:rolesAdd"]').click()
        time.sleep(1)
        self.take_screenshot(shot:=1)

        self.part = '05'
        self.sesh.find_element('xpath','//*[@id="rolesPermissionsForm:roleName"]').send_keys("Test Role Automated")
        self.sesh.find_element('xpath','//*[@id="rolesPermissionsForm:roleAlias"]').send_keys(self.role_alias)
        self.sesh.find_element('xpath','//*[@id="rolesPermissionsForm:roleDescription"]').send_keys("This is an automated test role.")
        self.take_screenshot(shot:=1)

        self.part = '06'
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:j_idt406:0"]').click()
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:j_idt406:1"]').click()
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:j_idt406:2"]').click()
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:j_idt406:3"]').click()
        self.take_screenshot(shot:=1)

        self.part = '07'
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:j_idt409"]').click()
        time.sleep(1)
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:roleMessages"]/div/div').get_attribute("class"), "alert alert-success") #confirm success alert
        self.take_screenshot(shot:=1)

        self.part = '08'
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm"]/div[1]/div[2]/div[1]').click()
        time.sleep(.5)
        self.take_screenshot(shot:=1)

        self.part = '09'
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:userGroupsAdd"]').click()
        time.sleep(1.5)
        self.take_screenshot(shot:=1)

        self.part = '10'
        self.sesh.find_element('xpath','//*[@id="rolesPermissionsForm:userGroupNameAssign_input"]').send_keys(self.perm_test_username)
        time.sleep(2)
        self.sesh.find_element('xpath','//*[@id="rolesPermissionsForm:userGroupNameAssign_input"]').send_keys(Keys.RETURN)

        self.part = '11'
        self.sesh.find_element('xpath', "//label[text()='Test Role Automated']").click()
        time.sleep(1)
        self.take_screenshot(shot:=1)

        self.part = '12'
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:j_idt385"]/span').click()
        time.sleep(1)
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:assignmentMessages"]/div/div').get_attribute("class"), "alert alert-success") #confirm success alert
        self.take_screenshot(shot:=1)
        self.set_end_time()
            
    def r03_mainpath_create_sub_dataverse(self):
        self.set_req('03')
        self.set_start_time()
        shot = 0

        self.part = '01'

        ### Main Landing Page ###
        self.sesh.get(self.dv_url)

        self.sesh.find_element('xpath', '//*[@id="addDataForm"]/div/button').click() #click add data
        self.take_screenshot(shot:=1)

        self.part = '02'
        self.sesh.find_element('xpath', '//*[@id="addDataForm"]/div/ul/li[1]/a').click() #click new dataverse
        self.take_screenshot(shot:=1)

        ### Create Dataverse Page ###
        self.part = '03'
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:selectHostDataverse_input"]').clear()
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:selectHostDataverse_input"]').send_keys(self.dv_props["host_dataverse"])
        time.sleep(2) # wait for host list to load
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:selectHostDataverse_input"]').send_keys(Keys.ENTER)
        time.sleep(1) # wait after click for ui to be usable
        self.set_dataverse_metadata(add_string="create") #Metadata that is same for create/edit
        if self.do_screenshots:
            #shot = 1
            for i in range(3):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)
        self.part = '04'

        self.sesh.find_element('xpath','//*[@id="dataverseForm:save"]').click() #create dataverse

        ### Test Save ###
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div').get_attribute("class"), "alert alert-success") #confirm success alert
        self.assertEqual(self.dv_url+'/dataverse/'+self.dataverse_name+'/', self.sesh.current_url) #confirm page
        self.take_screenshot(shot:=1)

        self.confirm_dataverse_metadata(add_string="create")
        self.sesh.get(self.dv_url+'/dataverse/'+self.dataverse_name)
        
        ### Dataverse Page - Publish ###
        self.part = '05'
        self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div/div/div[2]/button').click() #click publish
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:j_idt431"]').click() #confirm publish
        self.take_screenshot(shot:=shot+1)
        self.sesh.implicitly_wait(30)
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div').get_attribute("class"), "alert alert-success") #confirm success alert
        self.sesh.implicitly_wait(10)
        self.take_screenshot(shot:=shot+1)

        self.dataverse_id = re.sub(".*=", "", self.sesh.find_element('xpath', '//*[@id="dataverseForm:themeWidgetsOpts"]').get_attribute("href")) 

        self.set_end_time()
        
    def r04_mainpath_edit_dataverse(self):
        self.set_req('04')
        self.set_start_time()

        self.part = '01'
        self.sesh.get(self.dv_url+'/dataverse/'+self.dataverse_name)
        time.sleep(self.default_wait)
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div/div/div[2]/div[2]/button').click()
        self.part = '02'
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:editInfo"]').click()

        self.part = '03'
        self.take_screenshot(shot:=1)
        self.set_dataverse_metadata()
        self.take_screenshot(shot:=shot+1)
        ## For some reason this scroll is breaking our find_element (back when self.part 4 was after this) call. I switched to taking a single screenshot as all the metadata fits on there.
        # if self.do_screenshots:
        #     #shot = 1
        #     for i in range(3):
        #         self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
        #         self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath','//*[@id="dataverseForm:save"]').click() #save dataverse

        # We do self.part 10 before the other parts because we don't want any of the facet/search changes to stick
        self.part = '10'
        time.sleep(self.default_wait) # I think our code is picking up on the previous page div, so we wait before getting the div
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div').get_attribute("class"), "alert alert-success") #confirm success alert
        self.take_screenshot(shot:=1)
        
        #print(self.dv_url + '/dataverse/' + self.dataverse_name + '/')
        # self.sesh.get(self.dv_url + '/dataverse/' + self.dataverse_name + '/')
        # time.sleep(self.default_wait)
        time.sleep(1)
        self.confirm_dataverse_metadata()

        self.part = '04' #Select metadata facets
        self.sesh.get(self.dv_url+'/dataverse/'+self.dataverse_name)
        self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div/div/div[2]/div[2]/button').click()
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:editInfo"]').click()
        #time.sleep(1)
        #We force a click here to handle another element intercepting
        #self.sesh.execute_script('document.evaluate(\'//*[@id="dataverseForm:description"]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')

        self.sesh.execute_script(f"window.scrollTo(0, {2*self.scroll_height})") #scroll down some so we can see our changes better
        self.sesh.find_element('xpath','//*[@id="dataverseForm:metadataRoot"]').click()
        self.take_screenshot(shot:=1)
        time.sleep(1)

        self.part = '05'
        self.sesh.find_element('xpath','//*[@id="2"]').click()
        self.take_screenshot(shot:=1)
        time.sleep(.5)
        self.sesh.find_element('xpath','//*[@id="3"]').click()
        self.take_screenshot(shot:=shot+1)
        time.sleep(.5)
        self.sesh.find_element('xpath','//*[@id="4"]').click()
        self.take_screenshot(shot:=shot+1)
        time.sleep(.5)
        self.sesh.find_element('xpath','//*[@id="5"]').click()
        self.take_screenshot(shot:=shot+1)
        time.sleep(.5)
        self.sesh.find_element('xpath','//*[@id="6"]').click()
        self.take_screenshot(shot:=shot+1)
        time.sleep(.5)

        self.part = '06'
        self.sesh.find_element('xpath','//*[@id="dataverseForm:facetsRoot"]').click()
        self.take_screenshot(shot:=1)
        time.sleep(.5)

        self.part = '07' #Browse/search facets
        self.sesh.find_element('xpath','//*[@id="dataverseForm:j_idt330"]').click()
        time.sleep(.2)
        self.take_screenshot(shot:=1)
        time.sleep(.5)
        self.sesh.find_element('xpath','//*[@id="dataverseForm:j_idt330_1"]').click()
        self.take_screenshot(shot:=shot+1)
        time.sleep(.5)

        self.part = '08'
        self.sesh.find_element('xpath','//*[@id="dataverseForm:facetPickListCreate"]/div[1]/ul/li[4]').click()
        self.take_screenshot(shot:=1)

        self.part = '09'
        self.sesh.find_element('xpath','//*[@id="dataverseForm:facetPickListCreate"]/div[2]/div/button[1]').click()
        self.sesh.find_element('xpath','//*[@id="dataverseForm:facetPickListCreate"]/div[1]/ul/li[6]').click()
        self.sesh.find_element('xpath','//*[@id="dataverseForm:facetPickListCreate"]/div[2]/div/button[1]').click()
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath','//*[@id="dataverseForm:cancel"]/span').click()

        time.sleep(1) #wait before switching pages in r05

        self.set_end_time()
            
    def r05_mainpath_create_metadata_template(self):
        self.set_req('05')
        self.set_start_time()

        self.part = '01'
        self.sesh.get(self.dv_url+'/dataverse/'+self.dataverse_name)
        time.sleep(self.default_wait)
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div/div/div[2]/div[2]/button').click() #click dataverse edit button
        self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:manageTemplates"]').click() #click manage templates
        time.sleep(self.default_wait)
        self.take_screenshot(shot:=shot+1)
        self.part = '02'
        self.sesh.find_element('xpath', '//*[@id="manageTemplatesForm"]/div[1]/div/a').click() #click create dataset template
        time.sleep(self.default_wait)
        self.take_screenshot(shot:=1)
        self.part = '03'
        self.sesh.find_element('xpath', '//*[@id="templateForm:templateName"]').send_keys("test template create") #Create template title
        self.take_screenshot(shot:=1)
        self.part = '05'
        self.part = '06'
        self.set_dataset_metadata_template_instructions(add_string='create')
        if self.do_screenshots:
            shot = 0
            for i in range(9):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)
        #This chunk of code is weird. We were having issues with a page click being intercepted, so to handle that we are clicking a dropdown twice
        #We use javascript for this as it allows us to not care about the click interception.
        #I've tried clicking non dropdown elements and it doesn't clear the capture
        time.sleep(1)
        self.sesh.execute_script('document.evaluate(\'//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:2:cvv"]/div[3]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        time.sleep(1)
        self.sesh.execute_script('document.evaluate(\'//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:2:cvv"]/div[3]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        time.sleep(1)
        self.part = '04'
        #self.sesh.find_element('xpath', '//*[@id="templateForm:editMetadataFragement"]').click() #click background to clear any open dropdowns
        self.set_dataset_metadata_edit(add_string='create', xpath_dict=self.ds_template_xpaths)
        if self.do_screenshots:
            shot = 0
            for i in range(9):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)
        
        #TODO: I think here it where I was setting license but didn't finish?

        self.part = '07'
        self.sesh.find_element('xpath', '//*[@id="templateForm:j_idt892"]').click() #click "Save + Add Terms"
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") #confirm success alert
        self.take_screenshot(shot:=1)

        #TODO: Replace param_get with a new way to get the query params from a url
        self.template_id = parse.parse_qs(parse.urlparse(self.sesh.current_url).query)['id'][0]#<<- param_get(self.sesh.current_url, "id")
    
        self.part = '08'
        #TODO: show selected terms in a screenshot later?
        self.part = '09'

        self.sesh.find_element('xpath','//*[@id="templateForm:licenses_label"]').click() #click license dropdown
        time.sleep(.2)
        self.sesh.find_element('xpath','//*[@id="templateForm:licenses_1"]').click() #click "cc-by 4.0" inside dropdown
        time.sleep(.2)
        self.set_license(add_string='create', xpath_dict=self.ds_license_template_xpaths)
        if self.do_screenshots:
            shot = 0
            for i in range(3):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)

        self.part = '10'
        self.sesh.find_element('xpath', '//*[@id="templateForm:j_idt893"]').click() #click "Save Dataset Template" (which actually just saves the license)
        
        time.sleep(self.default_wait) #For some reason we are getting a reference error below without waiting. Maybe its getting the div for the previous page?
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") #confirm success alert
        self.take_screenshot(shot:=1)
        time.sleep(self.default_wait) #not sure why I have to do this but ok? Shouldn't confirming the alert work?
        
        self.sesh.get(self.dv_url+'/template.xhtml?id='+self.template_id+'&ownerId='+self.dataverse_id+'&editMode=METADATA')
        self.confirm_dataset_metadata(add_string='create', xpath_dict=self.ds_template_xpaths)
        self.confirm_dataset_metadata_template_instructions(add_string='create')

        self.sesh.get(self.dv_url+'/template.xhtml?id='+self.template_id+'&ownerId='+self.dataverse_id+'&editMode=LICENSE')
        self.confirm_license(add_string='create', xpath_dict=self.ds_license_template_xpaths)

        self.set_end_time()
            
    def r06_mainpath_edit_metadata_template(self):
        self.set_req('06')
        self.set_start_time()

        self.part = '01'
        self.part = '02'
        #TODO: probably change this to actually click the buttons. Put some above in self.part 1
        self.sesh.get(self.dv_url+'/template.xhtml?id='+self.template_id+'&ownerId='+self.dataverse_id+'&editMode=METADATA')
        time.sleep(self.default_wait) #added for screenshot
        self.take_screenshot(shot:=1)
        self.part = '04'
        self.part = '05'
        self.set_dataset_metadata_template_instructions(add_string='edit')
        if self.do_screenshots:
            shot = 0
            for i in range(9):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)
        #See note in R05 about the similar code
        time.sleep(1)
        self.sesh.execute_script('document.evaluate(\'//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:2:cvv"]/div[3]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        time.sleep(1)
        self.sesh.execute_script('document.evaluate(\'//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:2:cvv"]/div[3]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        time.sleep(1)    
        self.part = '03'    
        self.set_dataset_metadata_edit(add_string='edit', xpath_dict=self.ds_template_xpaths)
        if self.do_screenshots:
            shot = 0
            for i in range(9):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath', '//*[@id="templateForm:j_idt893"]').click() #click "Save + Add Terms"
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") #confirm success alert
        self.take_screenshot(shot:=shot+1)

#TODO: Are we suppose to be doing screenshots editing the license template
        self.sesh.get(self.dv_url+'/template.xhtml?id='+self.template_id+'&ownerId='+self.dataverse_id+'&editMode=LICENSE')

        self.sesh.find_element('xpath','//*[@id="templateForm:licenses_label"]').click() #click license dropdown
        time.sleep(.2)
        self.sesh.find_element('xpath','//*[@id="templateForm:licenses_0"]').click() #click "cc-by 1.0" inside dropdown
        time.sleep(.2)
        self.set_license(add_string='edit', xpath_dict=self.ds_license_template_xpaths)

        self.part = '06'  
        self.sesh.find_element('xpath', '//*[@id="templateForm:j_idt893"]').click() #click "Save Changes"
        time.sleep(self.default_wait) #not sure why I have to do this but ok? Shouldn't confirming the alert work?
        self.take_screenshot(shot:=1)
        
        self.sesh.get(self.dv_url+'/template.xhtml?id='+self.template_id+'&ownerId='+self.dataverse_id+'&editMode=METADATA')
        self.confirm_dataset_metadata(add_string='edit', xpath_dict=self.ds_template_xpaths)
        self.confirm_dataset_metadata_template_instructions(add_string='edit')

        self.sesh.get(self.dv_url+'/template.xhtml?id='+self.template_id+'&ownerId='+self.dataverse_id+'&editMode=LICENSE')
        self.confirm_license(add_string='edit', xpath_dict=self.ds_license_template_xpaths)

        self.set_end_time()
            
    def r09r11r13r20_mainpath_create_dataset(self): #
        self.set_req('09')
        self.set_start_time()

        self.part = '01'
        self.sesh.get(self.dv_url+'/dataverse/'+self.dataverse_name)
        self.sesh.find_element('xpath', '//*[@id="addDataForm"]/div/button').click() #click add data
        self.take_screenshot(shot:=1)

        self.part = '02'
        self.sesh.find_element('xpath', '//*[@id="addDataForm"]/div/ul/li[2]/a').click() #click new dataset
        self.take_screenshot(shot:=1)

        self.set_end_time()

        #TODO: set host dataverse (self.part 3) first

        self.set_req('11')
        self.set_start_time()
        self.part = '01'
    
        self.set_dataset_metadata_create(add_string='create')
        if self.do_screenshots:
            shot = 0
            for i in range(4):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)

        self.set_end_time()

        if self.test_files:
            self.set_req('13')
            self.set_start_time()
            self.part = '01' #click add button

            self.sesh.find_element('xpath', '//*[@id="datasetForm:fileUpload"]/div[1]/span').click()
            self.take_screenshot(shot:=1)

            self.part = '02' #file system dialog
            # NOTE: We can't screenshot the file dialog via selenium because its not actually in the browser.
            #       Instead we do a find element that will show up after upload and wait for the test-user to do the upload
            #       We may be able to do this via robot later https://robotframework.org/robotframework/latest/libraries/Screenshot.html#Take%20Screenshot
            self.sesh.implicitly_wait(3600)
            self.sesh.find_element('xpath', '//*[@id="filesHeaderCount"]') 
            self.sesh.implicitly_wait(10)
            print("upload completed")
            self.take_screenshot(shot:=1)
            self.set_end_time()

            # self.part = '03' # We do not currently test drag & Drop

            self.set_req('20')
            self.set_start_time()
            self.part = '01' #confirm md5
            self.sesh.find_element('xpath', '//*[@id="datasetForm:fileUpload"]/div[1]/span')
            self.assertEqual(self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileChecksum"]').text, self.test_file_1_md5)

            self.part = '02' #update name and path
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileName"]').clear()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileName"]').send_keys('test_file_1_renamed.txt')
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDirectoryName"]').clear()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDirectoryName"]').send_keys('/testfolder/')
            self.take_screenshot(shot:=1)

            self.part = '03' #add description
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDescription"]').clear()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDescription"]').send_keys('test_file_description')
            self.take_screenshot(shot:=1)

        self.part = '04' #NOTE: This is part of req 20 even though with test_files disabled it won't be a part of it
        self.sesh.find_element('xpath','//*[@id="datasetForm:saveBottom"]').click() #create dataset
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") #confirm success alert
        self.take_screenshot(shot:=1) #TODO: probalby a different R#, check shot+1

        ### Get dataset id from permissions page url for later uses ###
        self.dataset_id = re.sub(".*=", "", self.sesh.find_element('xpath', '//*[@id="datasetForm:manageDatasetPermissions"]').get_attribute("href")) 

#TODO: Add additional metadata here (R11)
#TODO: Add screenshots to code below after adding other requirements
#TODO: We should be doing our tests BEFORE publishing
#TODO: I'm not sure what to do for R19 (sign document) but it should be here

        # self.set_req('14')
        # self.set_start_time()

        if self.test_files:
            self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div[2]/div/a').click() #click publish
        else:
            self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div[1]/div/a').click() #click publish

        self.sesh.find_element('xpath', '//*[@id="datasetForm:publishDataset_content"]/div[4]/button[1]').click() #click publish confirm

        self.sesh.implicitly_wait(30)
        self.sesh.find_element('class name', 'label-default') #Find element to wait for load. May trigger prematurely with files added.
        self.sesh.implicitly_wait(10)
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="title-label-block"]/span').text, "Version 1.0") #Test dataset published
        
        self.sesh.find_element('xpath', '//*[@id="editDataSet"]').click() #click add data
        self.sesh.find_element('xpath', '//*[@id="datasetForm:editMetadata"]').click() #click edit dataset

        self.sesh.implicitly_wait(3)
        try: 
            self.confirm_dataset_metadata(add_string='create', is_update=False, xpath_dict=self.ds_edit_xpaths_notemplate)
        except Exception:
            self.templates_exist = True
            self.confirm_dataset_metadata(add_string='create', is_update=False, xpath_dict=self.ds_edit_xpaths_yestemplate)
        self.sesh.implicitly_wait(10)
        
        self.sesh.find_element('xpath', '//*[@id="datasetForm:cancel"]').click() #click out after testing data
        
        time.sleep(self.default_wait)

            
    def r10r12r15r16r17_mainpath_edit_dataset(self):
        # It seems like there are no actual screenshots or steps for r10?
        # I think we are using this as a catch-all for the editing that is not covered by other requirements
        self.set_req('12')
        self.set_start_time()

        self.part = '01'
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="editDataSet"]').click() #click add data
        self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:editMetadata"]').click() #click edit dataset
        time.sleep(self.default_wait) #added for screenshot
        self.take_screenshot(shot:=shot+1)

        self.part = '02'

        if not self.templates_exist:
            self.set_dataset_metadata_edit(add_string='edit', xpath_dict=self.ds_edit_xpaths_notemplate)
        else:
            self.set_dataset_metadata_edit(add_string='edit', xpath_dict=self.ds_edit_xpaths_yestemplate)

        if self.do_screenshots:
            shot = 0
            for i in range(8):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)

        self.set_req('17')
        self.set_start_time()
        self.part = '01'
        self.sesh.execute_script(f"window.scrollTo(0, {3 * self.scroll_height})") 
        self.take_screenshot(shot:=1)
        self.set_end_time()

        self.set_req('12') #We switch back and forth between reqs
        self.part = '03'
        self.sesh.find_element('xpath', '//*[@id="datasetForm:saveBottom"]').click() #click to save dataset
        time.sleep(self.default_wait) #added for screenshot
        self.take_screenshot(shot:=1)

        self.set_end_time()

        self.set_req('10')
        self.set_start_time()

        if self.test_files:
            # File-level metadata
            self.part = '01'
            self.take_screenshot(shot:=1)
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable_data"]/tr/td[1]/div').click()
            self.take_screenshot(shot:=shot+1)

            self.part = '02'
            time.sleep(.5)
            if not self.templates_exist:
                self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:j_idt1295"]/span/div/button').click()
            else:
                self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:j_idt1292"]/span/div/button').click()
            self.take_screenshot(shot:=1)
            time.sleep(.5)
            if not self.templates_exist:
                self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:j_idt1300"]').click()
            else:
                self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:j_idt1297"]').click()
            time.sleep(1)
            self.take_screenshot(shot:=shot+1)

            self.part = '03'
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileName"]').clear()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileName"]').send_keys('test_file_1_renamed_again.txt')
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDirectoryName"]').clear()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDirectoryName"]').send_keys('/testfolder_renamed/')
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDescription"]').clear()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDescription"]').send_keys('test_file_description_renamed')
            self.take_screenshot(shot:=1)

            self.part = '04'
            self.sesh.find_element('xpath', '//*[@id="datasetForm:savebutton"]').click()
            time.sleep(2)
            self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success")
            self.take_screenshot(shot:=1)
    
        # Dataset-terms
        self.part = '05'
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView"]/ul/li[3]/a').click()
        self.take_screenshot(shot:=shot+1)

        self.part = '06'
        if not self.templates_exist:
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:j_idt1722"]').click()
        else:
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:j_idt1719"]').click()

        self.part = '07'
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:licenses"]').click() #click license dropdown
        time.sleep(.2)
        self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:licenses_1"]').click() #click "cc-by 4.0" inside dropdown
        time.sleep(.2)
        self.take_screenshot(shot:=shot+1)

        self.part = '08'
        self.set_license(add_string='edit', xpath_dict=self.ds_license_edit_xpaths)
        if self.do_screenshots:
            shot = 0
            for i in range(3):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)

        self.part = '09'
        self.sesh.find_element('xpath','//*[@id="datasetForm:saveBottomTerms"]').click()
        self.take_screenshot(shot:=1)
        time.sleep(1)
        self.take_screenshot(shot:=shot+1)

        self.set_end_time()

        if self.test_files:
            self.set_req('15') # replace file
            self.set_start_time()

            self.part = '01'
            self.take_screenshot(shot:=1)
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:0:fileInfoInclude-filesTable"]/div[2]/div[1]/a').click() 
            self.take_screenshot(shot:=shot+1)

            self.part = '02'
            self.sesh.find_element('xpath', '//*[@id="editFile"]').click()
            time.sleep(.2)
            self.take_screenshot(shot:=1)
            self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div[2]/div/ul/li[3]/a').click()

            self.part = '03'
            self.take_screenshot(shot:=1)
            self.sesh.find_element('xpath', '//*[@id="datasetForm:fileUpload"]/div[1]/span').click()
            self.sesh.implicitly_wait(3600)
            self.sesh.find_element('xpath', '//*[@id="filesHeaderCount"]') 
            self.sesh.implicitly_wait(10)
            print("replace completed")

            self.part = '04'
            # self.part = '05'

            self.part = '06'
            self.take_screenshot(shot:=1)

            self.part = '07'
            self.sesh.find_element('xpath', '//*[@id="datasetForm:fileUpload"]/div[1]/span')
            self.assertEqual(self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileChecksum"]').text, self.test_file_1_replace_md5)

            self.part = '08'
            time.sleep(1)
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileName"]').clear()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileName"]').send_keys('test_file_1_replace_renamed.txt')
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDirectoryName"]').clear()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDirectoryName"]').send_keys('/testreplacefolder/')
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDescription"]').clear()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDescription"]').send_keys('test_file_replace_description')
            self.take_screenshot(shot:=1)

            self.part = '09'
            self.sesh.find_element('xpath','//*[@id="datasetForm:savebutton"]').click() #save
            self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") #confirm success alert
            self.take_screenshot(shot:=1) 
            self.sesh.find_element('xpath','//*[@id="breadcrumbLnk2"]').click() #Go back to dataset page

            self.set_end_time()

            self.set_req('16') # Add new file
            self.set_start_time()

            self.part = '01'
            self.take_screenshot(shot:=1)
            self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:filesTable:filesButtons"]/a').click() #save

            self.part = '02'
            self.take_screenshot(shot:=1) 
            self.sesh.find_element('xpath','//*[@id="datasetForm:fileUpload"]/div[1]/span').click() #save
            self.sesh.implicitly_wait(3600)
            self.sesh.find_element('xpath', '//*[@id="filesHeaderCount"]') 
            self.sesh.implicitly_wait(10)
            print("upload completed")

            self.part = '03'
            # self.part = '04'

            self.part = '05'
            self.sesh.find_element('xpath', '//*[@id="datasetForm:fileUpload"]/div[1]/span')
            self.assertEqual(self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileChecksum"]').text, self.test_file_2_md5)

            self.part = '06'
            time.sleep(1)
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileName"]').clear()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileName"]').send_keys('test_file_2_renamed.txt')
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDirectoryName"]').clear()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDirectoryName"]').send_keys('/testfolder2/')
            self.take_screenshot(shot:=1)

            self.part = '07'
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDescription"]').clear()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDescription"]').send_keys('test_file_description2')
            self.take_screenshot(shot:=1)

            self.part = '08'
            self.sesh.find_element('xpath','//*[@id="datasetForm:savebutton"]').click() #save changes
            self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") #confirm success alert
            self.take_screenshot(shot:=1) 

            self.set_end_time()

#TODO: Add screenshots to code below after adding other requirements
        # self.set_req('18')
        # self.set_start_time()
        if self.test_files:
            self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div[2]/div/a').click() #click publish
        else:
            self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div[1]/div/a').click() #click publish
        
        if not self.templates_exist:
            self.sesh.find_element('xpath', '//*[@id="datasetForm:j_idt2547"]').click() #click publish confirm
        else:
            self.sesh.find_element('xpath', '//*[@id="datasetForm:j_idt2544"]').click() #click publish confirm
        
        self.sesh.implicitly_wait(30)
        self.sesh.find_element('class name', 'label-default') #Find element to wait for load. May trigger prematurely with files added.
        self.sesh.implicitly_wait(10)
        if self.test_files:
            self.assertEqual(self.sesh.find_element('xpath', '//*[@id="title-label-block"]/span').text, "Version 2.0") #Test dataset published
        else:
            self.assertEqual(self.sesh.find_element('xpath', '//*[@id="title-label-block"]/span').text, "Version 1.1") #Test dataset published
        
        self.sesh.find_element('xpath', '//*[@id="editDataSet"]').click() #click add data
        self.sesh.find_element('xpath', '//*[@id="datasetForm:editMetadata"]').click() #click new dataset

        if not self.templates_exist:
            # print("NO")
            self.confirm_dataset_metadata(add_string='edit', is_update=True, xpath_dict=self.ds_edit_xpaths_notemplate) 
        else:
            # print("YES")
            self.confirm_dataset_metadata(add_string='edit', is_update=True, xpath_dict=self.ds_edit_xpaths_yestemplate) 
    
        self.sesh.find_element('xpath', '//*[@id="datasetForm:cancelTop"]').click() #click cancel out of edit after testing

        
    # This test of file upload requires manual interaction by the user, as automating selecting file via toe OS file picker is super painful
    # We may try to automate the file picker someday.
    # Or explore maybe some way to get around this with automating drag and drop https://stackoverflow.com/questions/38829153/
    # We may also want to implement another verison of this function that just uses the API to do file upload for when compliance is not an issue.

    # def r13_mainpath_upload_dataset_files(self):
    #     self.set_req('13')

    #     self.part = '01'

    #     self.part = '02'
    #     # Select files

    def r14_mainpath_review_data_set(self):
        # We need to take the existing "confirm_dataset_metadata" and make it work for the citation metadata tab (instead of the edit page)
        # ... Well because tab versions of the fields combine other ones, I need to rewrite the asserts. So I probably need a new method
        pass

    def r21_mainpath_search_dataset(self):
        # We need to do a simple search and an advanced search
        # Can we just do ONE advanced search with all the metadata fields or what?
        # I could construct a string for the search field to do the advanced search (instead of ui interaction). But I probably shouldn't
        # ...
        # So advanced search is an OR statement with the fields. So if we have to exercise ALL the search fields its going to be very painful.
        # Searching multiple words is also painful because they are also ORed
        # ... We can probably avoid the pain by using long custom single words (that no other dataset will have)
        # It seems like there are no actual screenshots or steps for r10?
        # I think we are using this as a catch-all for the editing that is not covered by other requirements
        self.set_req('12')
        self.set_start_time()

        self.sesh.get(self.dv_url)
        
        self.part = '01'
        self.part = '02'
        self.part = '03'
        self.part = '04'
        self.part = '05'
        self.part = '06'
        self.part = '07'
        


        self.set_end_time()

    def r24_mainpath_browse_datasets(self):
        # Need to test the previous/next buttons
        # Need to select facets and click a dataset? (Maybe we can avoid clicking?)
        pass

    def take_screenshot(self, shot):
        if self.do_screenshots: 
            dict_key = f'r{self.req}_p{self.part}_s{"%02d" % (shot)}'
            #print(dict[dict_key])
            if dict_key in self.screenshots.keys():
                raise Exception("Duplicate screenshot key encountered. Check test code.")
            self.screenshots[dict_key] = self.sesh.get_screenshot_as_base64()

    def set_start_time(self):
        self.start_times[int(self.req)] = time.time()

    def set_end_time(self):
        self.end_times[int(self.req)] = time.time()