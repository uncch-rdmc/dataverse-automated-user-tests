import time, unittest, os, requests, re, hashlib
from shutil import rmtree
from zipfile import ZipFile
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

class IngestWorkflowReportTestCase(unittest.TestCase, DataverseTestingMixin, DatasetTestingMixin):
    def __init__(self, *args, **kwargs):
        self.do_screenshots = kwargs.pop('do_screenshots', False)
        self.do_file_tests = kwargs.pop('do_file_tests', True) 
        super(IngestWorkflowReportTestCase, self).__init__( *args, **kwargs)

    def setUp(self):
        self.username = os.getenv('DATAVERSE_TEST_USER_USERNAME')
        self.password = os.getenv('DATAVERSE_TEST_USER_PASSWORD_BUILTIN')
        self.dv_url = os.getenv('DATAVERSE_SERVER_URL')
        self.perm_test_username = os.getenv('DATAVERSE_USERNAME_FOR_PERM_TEST')
        self.sso_option_value = os.getenv('DATAVERSE_SSO_OPTION_VALUE')
        self.download_full_path = os.getenv('DOWNLOAD_PARENT_DIR')+"/seleniumdownloads"
        self.extra_wait = int(os.getenv('EXTRA_WAIT'))
        self.scroll_height = 600
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

        self.test_file_1_md5 = 'a5890ace30a3e84d9118196c161aeec2'
        self.test_file_1_replace_md5 = '07436de69e3283065a2453322ee22ba3'
        self.test_file_2_md5 = 'c7803e4497be4984e41102e1b2ef64cc'
        self.md5_prefix = 'MD5: ' #what dataverse appends to the beginning of md5s

        self.role_alias = "test_role_auto"
        self.role_alias_created = False

        options = Options()
        if self.browser_type == "Chrome":
            options.add_experimental_option("prefs", {
                "download.default_directory":self.download_full_path, 
                "download.prompt_for_download": False
            })
            
            self.sesh = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        else:
            print("Browsers other than Chrome have not been tested, and certain tests will fail (file downloading).")
        if self.do_screenshots:
            self.sesh.set_window_size(1200,827) #675 should be the height with the screenshot not including the top/bottom bar. At least with chrome v111

        self.sesh.implicitly_wait(10)

    def tearDown(self):
        self.delete_dv_resources(self.dataset_id, self.dataverse_id, (self.role_alias if self.role_alias_created else None))
        if os.path.isdir(self.download_full_path):
            try:
                rmtree(self.download_full_path)
            except Exception as e:
                print("Unable to delete download folder even though it exists. Error: " + str(e))

    def test_requirements(self):

        self.info = self.get_testing_info()

        tests = [
            self.r01alt_mainpath_builtin_auth,
            #self.r01_mainpath_test_sso_auth,
            self.get_api_token,
            self.r02_mainpath_add_user_group_role,
            self.r03_mainpath_create_sub_dataverse,
            self.r04_mainpath_edit_dataverse,
            self.r05_mainpath_create_metadata_template,
            self.r06_mainpath_edit_metadata_template,
            self.r09r11r13r20_mainpath_create_dataset,
            self.r10r12r15r16r17r18_mainpath_edit_dataset,
            self.r21r22r23r24r25_dataset_file_discovery,
        ]
        for test in tests:
            test()
                
        print("Tests Complete")

    def delete_dv_resources(self, ds_id=None, dv_id=None, r_alias=None):
        headers = {'X-Dataverse-key': self.api_token}
        if ds_id is not None:
            try:
                resp_ds_destroy = requests.delete(f'{self.dv_url}/api/datasets/{ds_id}/destroy', headers=headers)
                if "data" in resp_ds_destroy.json() and "message" in resp_ds_destroy.json()["data"]:
                    print(f'Role delete called. Result: {resp_ds_destroy.status_code} - {resp_ds_destroy.json()["data"]["message"]}')
                else:
                    print(f'Role delete called. Result: {resp_ds_destroy.status_code} - {resp_ds_destroy.text}')
            except Exception as e:
                print("Unable to destroy dataset on tearDown. Error: " + str(e))
        if dv_id is not None:
            try:
                resp_dv_delete = requests.delete(f'{self.dv_url}/api/dataverses/{dv_id}', headers=headers)
                if "data" in resp_dv_delete.json() and "message" in resp_dv_delete.json()["data"]:
                    print(f'Role delete called. Result: {resp_dv_delete.status_code} - {resp_dv_delete.json()["data"]["message"]}')
                else:
                    print(f'Role delete called. Result: {resp_dv_delete.status_code} - {resp_dv_delete.text}')
            except Exception as e:
                print("Unable to delete dataverse on tearDown. Error: " + str(e))
        if r_alias is not None:
            try:
                resp_role_delete = requests.delete(f'{self.dv_url}/api/roles/:alias?alias={r_alias}', headers=headers)
                if "data" in resp_role_delete.json() and "message" in resp_role_delete.json()["data"]:
                    print(f'Role delete called. Result: {resp_role_delete.status_code} - {resp_role_delete.json()["data"]["message"]}')
                else:
                    print(f'Role delete called. Result: {resp_role_delete.status_code} - {resp_role_delete.text}')
            except Exception as e:
                print("Unable to delete role on tearDown. Error: " + str(e))
        if (ds_id is None) and (dv_id is None) and (r_alias is None):
            print("No resources to delete")

    def get_dataverse_version(self):
        try:
            dataverse_version = requests.get(f'{self.dv_url}/api/info/version')
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
        self.sesh.find_element('xpath', f"//option[@value='{self.sso_option_value}']").click() 
        self.take_screenshot(shot:=1)
        
        self.part = '03'
        self.sesh.find_element('xpath', '//*[@id="idpSelectListButton"]').click()
        time.sleep(2 + self.extra_wait)
        self.take_screenshot(shot:=1)

        self.part = '04'
        self.sesh.implicitly_wait(3600)
        print("User input required: complete oauth login.")
        self.sesh.find_element('xpath', '//*[@id="dataverseDesc"]') #Find element to wait login to complete
        self.assertEqual(f'{self.dv_url}/dataverse.xhtml', self.sesh.current_url)
        self.take_screenshot(shot:=1)
        print("Authorization Completed")
        self.sesh.implicitly_wait(10)

        self.set_end_time()
            
    #NOTE: This test doesn't actually fufill a req, we just call it alternatively
    def r01alt_mainpath_builtin_auth(self):
        self.set_req('01')

        self.part = '01'
        self.sesh.get(f'{self.dv_url}/loginpage.xhtml?redirectPage=%2Fdataverse.xhtml')
        self.sesh.find_element('xpath', '//*[@id="loginForm:credentialsContainer:0:credValue"]').send_keys(self.username)
        self.sesh.find_element('xpath', '//*[@id="loginForm:credentialsContainer:1:sCredValue"]').send_keys(self.password)
        self.sesh.find_element('xpath', '//*[@id="loginForm:login"]').click()
        self.sesh.find_element('xpath', '//*[@id="dataverseDesc"]') #Find element to wait for load
        self.assertEqual(f'{self.dv_url}/dataverse.xhtml', self.sesh.current_url)

        
    def get_api_token(self):
        #We confirm we are the user we think we are. This is mostly for reporting purproses
        self.sesh.get(f'{self.dv_url}/dataverseuser.xhtml?selectTab=accountInfo')
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="userIdentifier"]/td').text, self.username) 
        
        #Note: This code assumes you have already clicked "Create Token" with this account.
        self.sesh.get(f'{self.dv_url}/dataverseuser.xhtml?selectTab=apiTokenTab')
        self.api_token = self.sesh.find_element('xpath', '//*[@id="apiToken"]/pre/code').text 

    def r02_mainpath_add_user_group_role(self):
        self.set_req('02')
        self.set_start_time()
        shot = 0

        self.part = '01'
        self.sesh.get(f'{self.dv_url}')
        time.sleep(1 + self.extra_wait)
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div/div[2]/div[2]/div/button').click() #click edit
        time.sleep(.5 + self.extra_wait)
        self.take_screenshot(shot:=shot+1)

        self.part = '02'
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:managePermissions"]').click()
        time.sleep(1 + self.extra_wait)
        self.take_screenshot(shot:=1)

        self.part = '03'
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm"]/div[1]/div[3]').click()
        time.sleep(.5 + self.extra_wait)
        self.take_screenshot(shot:=1)

        self.part = '04'
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:rolesAdd"]').click()
        time.sleep(1 + self.extra_wait)
        self.take_screenshot(shot:=1)

        self.part = '05'
        self.sesh.find_element('xpath','//*[@id="rolesPermissionsForm:roleName"]').send_keys("Test Role Automated")
        self.sesh.find_element('xpath','//*[@id="rolesPermissionsForm:roleAlias"]').send_keys(self.role_alias)
        self.sesh.find_element('xpath','//*[@id="rolesPermissionsForm:roleDescription"]').send_keys("This is an automated test role.")
        self.take_screenshot(shot:=1)

        self.part = '06'
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:editRolePermissionPanel_content"]/table/tbody/tr[1]/td/input').click()
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:editRolePermissionPanel_content"]/table/tbody/tr[2]/td/input').click()
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:editRolePermissionPanel_content"]/table/tbody/tr[3]/td/input').click()
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:editRolePermissionPanel_content"]/table/tbody/tr[4]/td/input').click()
        self.take_screenshot(shot:=1)

        self.part = '07'
        self.sesh.find_element('xpath', '//*[@id="editRoleButtonPanel"]/button[1]').click()
        time.sleep(1 + self.extra_wait)
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:roleMessages"]/div/div').get_attribute("class"), "alert alert-success") 
        self.role_alias_created = True
        self.take_screenshot(shot:=1)

        self.part = '08'
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm"]/div[1]/div[2]/div[1]').click()
        time.sleep(.5 + self.extra_wait)
        self.take_screenshot(shot:=1)

        self.part = '09'
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:userGroupsAdd"]').click()
        time.sleep(1.5 + self.extra_wait)
        self.take_screenshot(shot:=1)

        self.part = '10'
        self.sesh.find_element('xpath','//*[@id="rolesPermissionsForm:userGroupNameAssign_input"]').send_keys(self.perm_test_username)
        time.sleep(2 + self.extra_wait)
        self.sesh.find_element('xpath','//*[@id="rolesPermissionsForm:userGroupNameAssign_input"]').send_keys(Keys.RETURN)

        self.part = '11'
        self.sesh.find_element('xpath', "//label[text()='Test Role Automated']").click()
        time.sleep(1 + self.extra_wait)
        self.take_screenshot(shot:=1)

        self.part = '12'
        self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:assignRoleContent"]/div[2]/button[1]').click()
        time.sleep(1 + self.extra_wait)
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="rolesPermissionsForm:assignmentMessages"]/div/div').get_attribute("class"), "alert alert-success") 
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
        time.sleep(2 + self.extra_wait) # wait for host list to load
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:selectHostDataverse_input"]').send_keys(Keys.ENTER)
        time.sleep(1 + self.extra_wait) # wait after click for ui to be usable
        self.set_dataverse_metadata(add_string="create") #Metadata that is same for create/edit
        if self.do_screenshots:
            for i in range(3):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)
        self.part = '04'

        self.sesh.find_element('xpath','//*[@id="dataverseForm:save"]').click() #create dataverse

        ### Test Save ###
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div').get_attribute("class"), "alert alert-success") 
        self.assertEqual(self.dv_url+'/dataverse/'+self.dataverse_identifier+'/', self.sesh.current_url) #confirm page
        self.take_screenshot(shot:=1)

        self.confirm_dataverse_metadata(add_string="create")
        self.sesh.get(self.dv_url+'/dataverse/'+self.dataverse_identifier)
        
        ### Dataverse Page - Publish ###
        self.part = '05'
        self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div/div/div[2]/button').click() #click publish
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:j_idt431"]').click() #confirm publish
        self.take_screenshot(shot:=shot+1)
        self.sesh.implicitly_wait(30)
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div').get_attribute("class"), "alert alert-success") 
        self.sesh.implicitly_wait(10)
        self.take_screenshot(shot:=shot+1)

        self.dataverse_id = re.sub(".*=", "", self.sesh.find_element('xpath', '//*[@id="dataverseForm:themeWidgetsOpts"]').get_attribute("href")) 

        self.set_end_time()
        
    def r04_mainpath_edit_dataverse(self):
        self.set_req('04')
        self.set_start_time()

        self.part = '01'
        self.sesh.get(self.dv_url+'/dataverse/'+self.dataverse_identifier)
        time.sleep(2 + self.extra_wait)
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div/div/div[2]/div[2]/button').click()
        self.part = '02'
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:editInfo"]').click()

        self.part = '03'
        self.take_screenshot(shot:=1)
        self.set_dataverse_metadata()
        self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath','//*[@id="dataverseForm:save"]').click() #save dataverse

        # We do self.part 10 before the other parts because we don't want any of the facet/search changes to stick
        self.part = '10'
        time.sleep(2 + self.extra_wait)
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div').get_attribute("class"), "alert alert-success") 
        self.take_screenshot(shot:=1)
        
        time.sleep(1 + self.extra_wait)
        self.confirm_dataverse_metadata()

        self.part = '04' #Select metadata facets
        self.sesh.get(self.dv_url+'/dataverse/'+self.dataverse_identifier)
        self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div/div/div[2]/div[2]/button').click()
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:editInfo"]').click()
        
        self.sesh.execute_script(f"window.scrollTo(0, {2*self.scroll_height})")
        self.sesh.find_element('xpath','//*[@id="dataverseForm:metadataRoot"]').click()
        self.take_screenshot(shot:=1)
        time.sleep(1 + self.extra_wait)

        self.part = '05'
        self.sesh.find_element('xpath','//*[@id="2"]').click()
        self.take_screenshot(shot:=1)
        time.sleep(.5 + self.extra_wait)
        self.sesh.find_element('xpath','//*[@id="3"]').click()
        self.take_screenshot(shot:=shot+1)
        time.sleep(.5 + self.extra_wait)
        self.sesh.find_element('xpath','//*[@id="4"]').click()
        self.take_screenshot(shot:=shot+1)
        time.sleep(.5 + self.extra_wait)
        self.sesh.find_element('xpath','//*[@id="5"]').click()
        self.take_screenshot(shot:=shot+1)
        time.sleep(.5 + self.extra_wait)
        self.sesh.find_element('xpath','//*[@id="6"]').click()
        self.take_screenshot(shot:=shot+1)
        time.sleep(.5 + self.extra_wait)

        self.part = '06'
        self.sesh.find_element('xpath','//*[@id="dataverseForm:facetsRoot"]').click()
        self.take_screenshot(shot:=1)
        time.sleep(.5 + self.extra_wait)

        self.part = '07' #Browse/search facets
        self.sesh.find_element('xpath','//*[@id="dataverseForm:j_idt330"]').click()
        time.sleep(.2 + self.extra_wait)
        self.take_screenshot(shot:=1)
        time.sleep(.5 + self.extra_wait)
        self.sesh.find_element('xpath','//*[@id="dataverseForm:j_idt330_1"]').click()
        self.take_screenshot(shot:=shot+1)
        time.sleep(.5 + self.extra_wait)

        self.part = '08'
        self.sesh.find_element('xpath','//*[@id="dataverseForm:facetPickListCreate"]/div[1]/ul/li[4]').click()
        self.take_screenshot(shot:=1)

        self.part = '09'
        self.sesh.find_element('xpath','//*[@id="dataverseForm:facetPickListCreate"]/div[2]/div/button[1]').click()
        self.sesh.find_element('xpath','//*[@id="dataverseForm:facetPickListCreate"]/div[1]/ul/li[6]').click()
        self.sesh.find_element('xpath','//*[@id="dataverseForm:facetPickListCreate"]/div[2]/div/button[1]').click()
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath','//*[@id="dataverseForm:cancel"]/span').click()

        time.sleep(1 + self.extra_wait)

        self.set_end_time()
            
    def r05_mainpath_create_metadata_template(self):
        self.set_req('05')
        self.set_start_time()

        self.part = '01'
        self.sesh.get(self.dv_url+'/dataverse/'+self.dataverse_identifier)
        time.sleep(2 + self.extra_wait)
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div/div/div[2]/div[2]/button').click() #click dataverse edit button
        self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:manageTemplates"]').click() #click manage templates
        time.sleep(2 + self.extra_wait)
        self.take_screenshot(shot:=shot+1)
        self.part = '02'
        self.sesh.find_element('xpath', '//*[@id="manageTemplatesForm"]/div[1]/div/a').click() #click create dataset template
        time.sleep(2 + self.extra_wait)
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
        time.sleep(1 + self.extra_wait)
        self.sesh.execute_script('document.evaluate(\'//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:2:cvv"]/div[3]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        time.sleep(1 + self.extra_wait)
        self.sesh.execute_script('document.evaluate(\'//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:2:cvv"]/div[3]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        time.sleep(1 + self.extra_wait)
        self.part = '04'
        self.set_dataset_metadata_edit(add_string='create', xpath_dict=self.ds_template_xpaths)
        if self.do_screenshots:
            shot = 0
            for i in range(9):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)

        self.part = '07'
        self.sesh.find_element('xpath', '//*[@id="templateForm:j_idt892"]').click() #click "Save + Add Terms"
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") 
        self.take_screenshot(shot:=1)

        self.template_id = parse.parse_qs(parse.urlparse(self.sesh.current_url).query)['id'][0]
    
        self.part = '08'
        self.sesh.find_element('xpath','//*[@id="templateForm:licenses_label"]').click() #click license dropdown
        time.sleep(.2 + self.extra_wait)
        self.sesh.find_element('xpath','//*[@id="templateForm:licenses_1"]').click() #click "cc-by 4.0" inside dropdown
        time.sleep(.2 + self.extra_wait)
        self.take_screenshot(shot:=1)

        self.part = '09'
        self.set_license(add_string='create', xpath_dict=self.ds_license_template_xpaths)
        if self.do_screenshots:
            shot = 0
            for i in range(3):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)

        self.part = '10'
        self.sesh.find_element('xpath', '//*[@id="templateForm:j_idt893"]').click() #click "Save Dataset Template" (which actually just saves the license)
        time.sleep(2 + self.extra_wait)
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") 
        self.take_screenshot(shot:=1)
        time.sleep(2 + self.extra_wait) #We have to wait extra after the alert before doing other things or the test blows up 

        #NOTE: we don't screenshot here because its not an actual requirement to check at this point. We could maybe disable this
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
        self.sesh.get(self.dv_url+'/dataverse/'+self.dataverse_identifier)
        time.sleep(2 + self.extra_wait)
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div/div/div[2]/div[2]/button').click() #click dataverse edit button
        self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:manageTemplates"]').click() #click manage templates
        time.sleep(2 + self.extra_wait)

        self.part = '02'
        #we disable display of root templates to make the template list always contain our one template
        if(self.sesh.find_element('xpath', '//*[@id="manageTemplatesForm:templateRoot"]').is_selected()):
            self.sesh.find_element('xpath', '//*[@id="manageTemplatesForm:templateRoot"]').click() 
            time.sleep(1 + self.extra_wait)
        self.take_screenshot(shot:=1)

        self.sesh.find_element('xpath', '//*[@id="manageTemplatesForm:allTemplates_data"]/tr/td[4]/div/div/button').click()
        time.sleep(.5 + self.extra_wait)
        self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath', '//*[@id="manageTemplatesForm:allTemplates_data"]/tr/td[4]/div/div/ul/li[1]/a').click()
        time.sleep(2 + self.extra_wait) #added for screenshot
        self.take_screenshot(shot:=shot+1)

        self.part = '04' #part 5 screenshots capture part 4
        self.part = '05'
        self.set_dataset_metadata_template_instructions(add_string='edit')

        if self.do_screenshots:
            shot = 0
            for i in range(9):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)
        #See note in R05 about the similar code
        time.sleep(1 + self.extra_wait)
        self.sesh.execute_script('document.evaluate(\'//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:2:cvv"]/div[3]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        time.sleep(1 + self.extra_wait)
        self.sesh.execute_script('document.evaluate(\'//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:2:cvv"]/div[3]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        time.sleep(1 + self.extra_wait)    
        self.part = '03'    
        self.set_dataset_metadata_edit(add_string='edit', xpath_dict=self.ds_template_xpaths)
        if self.do_screenshots:
            shot = 0
            for i in range(9):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)
        self.part = '06'  
        self.sesh.find_element('xpath', '//*[@id="templateForm:j_idt893"]').click() #click "Save Changes"
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") 
        self.take_screenshot(shot:=1)

        self.part = '07'
        self.sesh.get(self.dv_url+'/dataverse/'+self.dataverse_identifier)
        time.sleep(2 + self.extra_wait)
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div/div/div[2]/div[2]/button').click() #click dataverse edit button
        self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath', '//*[@id="dataverseForm:manageTemplates"]').click() #click manage templates
        time.sleep(2 + self.extra_wait)

        self.part = '08'
        #we disable display of root templates to make the template list always contain our one template
        if(self.sesh.find_element('xpath', '//*[@id="manageTemplatesForm:templateRoot"]').is_selected()):
            self.sesh.find_element('xpath', '//*[@id="manageTemplatesForm:templateRoot"]').click() 
            time.sleep(1 + self.extra_wait)
        self.take_screenshot(shot:=1)

        self.sesh.find_element('xpath', '//*[@id="manageTemplatesForm:allTemplates_data"]/tr/td[4]/div/div/button').click()
        time.sleep(.5 + self.extra_wait)
        self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath', '//*[@id="manageTemplatesForm:allTemplates_data"]/tr/td[4]/div/div/ul/li[2]/a').click()
        time.sleep(2 + self.extra_wait) #added for screenshot
        self.take_screenshot(shot:=shot+1)

        self.part = '09'

        self.sesh.find_element('xpath','//*[@id="templateForm:licenses_label"]').click() #click license dropdown
        time.sleep(.2 + self.extra_wait)
        self.sesh.find_element('xpath','//*[@id="templateForm:licenses_0"]').click() #click "cc-by 1.0" inside dropdown
        time.sleep(.2 + self.extra_wait)
        self.set_license(add_string='edit', xpath_dict=self.ds_license_template_xpaths)
        if self.do_screenshots:
            shot = 0
            for i in range(3):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)

        self.part = '10'  
        self.sesh.find_element('xpath', '//*[@id="templateForm:j_idt893"]').click() #click "Save Changes"
        time.sleep(2 + self.extra_wait)
        self.take_screenshot(shot:=1)

        #NOTE: we don't screenshot here because its not a requirement to confirm the data.
        self.sesh.get(self.dv_url+'/template.xhtml?id='+self.template_id+'&ownerId='+self.dataverse_id+'&editMode=METADATA')
        self.confirm_dataset_metadata(add_string='edit', xpath_dict=self.ds_template_xpaths)
        self.confirm_dataset_metadata_template_instructions(add_string='edit')
        self.sesh.get(self.dv_url+'/template.xhtml?id='+self.template_id+'&ownerId='+self.dataverse_id+'&editMode=LICENSE')
        self.confirm_license(add_string='edit', xpath_dict=self.ds_license_template_xpaths)

        self.set_end_time()
            
    def r09r11r13r20_mainpath_create_dataset(self):
        self.set_req('09')
        self.set_start_time()

        self.part = '01'
        self.sesh.get(self.dv_url+'/dataverse/'+self.dataverse_identifier)
        self.sesh.find_element('xpath', '//*[@id="addDataForm"]/div/button').click() #click add data
        self.take_screenshot(shot:=1)

        self.part = '02'
        self.sesh.find_element('xpath', '//*[@id="addDataForm"]/div/ul/li[2]/a').click() #click new dataset
        self.take_screenshot(shot:=1)

        self.part = '03'
        self.sesh.find_element('xpath', '//*[@id="datasetForm:selectHostDataverse_input"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:selectHostDataverse_input"]').send_keys(self.dv_props['name'])
        time.sleep(2 + self.extra_wait)
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:selectHostDataverse_input"]').send_keys(Keys.ENTER)
        self.take_screenshot(shot:=shot+1)
        time.sleep(1 + self.extra_wait)
        #self.set_end_time() #We continue this test later

        self.set_req('11')
        self.set_start_time()

        self.part = '01'
        self.set_dataset_metadata_create(add_string='create')
        if self.do_screenshots:
            shot = 0
            for i in range(4):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)
        #self.set_end_time() #We continue this test later so we don't do the end time here

        if self.do_file_tests:
            self.set_req('13')
            self.set_start_time()

            self.part = '01' #click add button
            self.sesh.find_element('xpath', '//*[@id="datasetForm:fileUpload"]/div[1]/span').click()
            self.take_screenshot(shot:=1)

            self.part = '02' #file system dialog
            self.sesh.implicitly_wait(3600)
            print("User input required: upload test_file_1.txt")
            self.sesh.find_element('xpath', '//*[@id="filesHeaderCount"]') 
            self.sesh.implicitly_wait(10)
            print("Upload Completed")
            self.take_screenshot(shot:=1)
            self.set_end_time()

            # self.part = '03' # We do not currently test drag & Drop

            self.set_req('20')
            self.set_start_time()
            self.part = '01' #confirm md5
            self.sesh.find_element('xpath', '//*[@id="datasetForm:fileUpload"]/div[1]/span')
            self.assertEqual(self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileChecksum"]').text, self.md5_prefix + self.test_file_1_md5)

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

        self.part = '04' #NOTE: This is part of req 20 even though with do_file_tests disabled it won't be a part of it
        self.sesh.find_element('xpath','//*[@id="datasetForm:saveBottom"]').click() #create dataset
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") 
        self.take_screenshot(shot:=1)

        ### Get dataset id from permissions page url for later uses ###
        self.dataset_id = re.sub(".*=", "", self.sesh.find_element('xpath', '//*[@id="datasetForm:manageDatasetPermissions"]').get_attribute("href")) 

        self.set_req('09')

        ### Dataset-terms (note: create and edit use the same code) ###
        self.part = '04'
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView"]/ul/li[3]/a').click()
        self.take_screenshot(shot:=shot+1)
        time.sleep(1 + self.extra_wait)

        self.part = '05'
        if not self.templates_exist:
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:j_idt1722"]').click()
        else:
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:j_idt1719"]').click()

        self.part = '06'
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:licenses"]').click() #click license dropdown
        time.sleep(.2 + self.extra_wait)
        self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:licenses_1"]').click() #click "cc-by 4.0" inside dropdown
        time.sleep(.2 + self.extra_wait)
        self.take_screenshot(shot:=shot+1)

        self.part = '07'
        self.set_license(add_string='edit', xpath_dict=self.ds_license_edit_xpaths)
        if self.do_screenshots:
            shot = 0
            for i in range(3):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)

        self.part = '08'
        self.sesh.find_element('xpath','//*[@id="datasetForm:saveBottomTerms"]').click()
        self.take_screenshot(shot:=1)
        time.sleep(1 + self.extra_wait)
        self.take_screenshot(shot:=shot+1)

        self.set_req('11')

        self.part = '02' #click edit dataset
        self.sesh.find_element('xpath', '//*[@id="editDataSet"]').click() #click edit dataset
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:editMetadata"]').click() #click metadata
        self.take_screenshot(shot:=shot+1)

        self.part = '03' #edit metadata postcreate
        self.set_dataset_metadata_edit(add_string='postcreate', xpath_dict=self.ds_edit_xpaths_notemplate)
        if self.do_screenshots:
            shot = 0
            for i in range(8):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)

        self.part = '04' #save
        self.sesh.find_element('xpath', '//*[@id="datasetForm:saveBottom"]').click() #click to save dataset
        self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div[2]/div/a') #Wait for load
        self.take_screenshot(shot:=1)

        self.set_end_time()

        self.set_req('14') #NOTE: Very similar to req 18. If you edit this also edit that
        self.set_start_time()

        self.part = '01' 

        self.sesh.execute_script(f"window.scrollTo(0, {3 * self.scroll_height})") 
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:0:fileInfoInclude-filesTable"]/div[2]/div[1]/a').text, 'test_file_1_renamed.txt')
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:0:fileHierarchy"]').text, 'testfolder/')
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:0:fileInfoInclude-filesTable"]/div[2]/div[2]/div[2]/span[1]').get_attribute('data-clipboard-text'), self.test_file_1_md5)
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:0:fileDescNonEmpty"]').text, 'test_file_description')
        self.take_screenshot(shot:=1)

        self.part = '02'
        self.sesh.execute_script("window.scrollTo(0, 0)") 
        self.sesh.find_element('xpath', '//*[@id="editDataSet"]').click() #click add data
        self.sesh.find_element('xpath', '//*[@id="datasetForm:editMetadata"]').click() #click edit dataset
        self.sesh.implicitly_wait(3) #We fail fast because we expect this to happen when a dataset template has been made already (normal test path)
        try: 
            self.confirm_dataset_metadata(add_string='postcreate', is_update=False, xpath_dict=self.ds_edit_xpaths_notemplate)
        except Exception:
            self.templates_exist = True
            self.confirm_dataset_metadata(add_string='postcreate', is_update=False, xpath_dict=self.ds_edit_xpaths_yestemplate)
        self.sesh.implicitly_wait(10)
        if self.do_screenshots:
            shot = 0
            for i in range(8):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:cancel"]').click() #click out after testing data

        self.part = '03' #terms (license)
    
        self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView"]/ul/li[3]/a').click()
        time.sleep(.5 + self.extra_wait)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:termsTab"]/div[1]/a').click()
        time.sleep(1 + self.extra_wait)

        self.confirm_license(add_string='edit', xpath_dict=self.ds_license_edit_xpaths)
        if self.do_screenshots:
            shot = 0
            for i in range(3):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:cancel"]').click()

        self.set_end_time()

        self.set_req('09')

        self.part = '09'

        self.take_screenshot(shot:=1)
        if self.do_file_tests:
            self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div[2]/div/a').click() #click publish
        else:
            self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div[1]/div/a').click() #click publish
        self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:publishDataset_content"]/div[4]/button[1]').click() #click publish confirm
        self.take_screenshot(shot:=shot+1)
        self.sesh.implicitly_wait(30)
        self.sesh.find_element('class name', 'label-default') #Find element to wait for load
        self.sesh.implicitly_wait(10)
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="title-label-block"]/span').text, "Version 1.0") #Test dataset published
        self.take_screenshot(shot:=shot+1)

        self.set_end_time()
            
    def r10r12r15r16r17r18_mainpath_edit_dataset(self):
        self.set_req('12')
        self.set_start_time()

        self.part = '01'
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="editDataSet"]').click() #click add data
        self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:editMetadata"]').click() #click edit dataset
        time.sleep(2 + self.extra_wait) #added for screenshot
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
        time.sleep(2 + self.extra_wait) #added for screenshot
        self.take_screenshot(shot:=1)

        self.set_end_time()

        self.set_req('10')
        self.set_start_time()

        if self.do_file_tests:
            ### File-level metadata ###
            self.part = '01'
            self.take_screenshot(shot:=1)
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable_data"]/tr/td[1]/div').click()
            self.take_screenshot(shot:=shot+1)

            self.part = '02'
            time.sleep(.5 + self.extra_wait)
            if not self.templates_exist:
                self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:j_idt1295"]/span/div/button').click()
            else:
                self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:j_idt1292"]/span/div/button').click()
            self.take_screenshot(shot:=1)
            time.sleep(.5 + self.extra_wait)
            if not self.templates_exist:
                self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:j_idt1300"]').click()
            else:
                self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:j_idt1297"]').click()
            time.sleep(1 + self.extra_wait)
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
            time.sleep(2 + self.extra_wait)
            self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success")
            self.take_screenshot(shot:=1)
    
        ### Dataset-terms (note: create and edit use the same code) ###
        self.part = '05'
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView"]/ul/li[3]/a').click()
        self.take_screenshot(shot:=shot+1)
        time.sleep(1 + self.extra_wait)

        self.part = '06'
        if not self.templates_exist:
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:j_idt1722"]').click()
        else:
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:j_idt1719"]').click()

        self.part = '07'
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:licenses"]').click() #click license dropdown
        time.sleep(.2 + self.extra_wait)
        self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:licenses_1"]').click() #click "cc-by 4.0" inside dropdown
        time.sleep(.2 + self.extra_wait)
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
        time.sleep(1 + self.extra_wait)
        self.take_screenshot(shot:=shot+1)

        self.set_end_time()

        if self.do_file_tests:
            self.set_req('15') # replace file
            self.set_start_time()

            self.part = '01'
            self.take_screenshot(shot:=1)
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:0:fileInfoInclude-filesTable"]/div[2]/div[1]/a').click() 
            self.take_screenshot(shot:=shot+1)

            self.part = '02'
            self.sesh.find_element('xpath', '//*[@id="editFile"]').click()
            time.sleep(.2 + self.extra_wait)
            self.take_screenshot(shot:=1)
            self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div[2]/div/ul/li[3]/a').click()

            self.part = '03'
            self.take_screenshot(shot:=1)
            self.sesh.find_element('xpath', '//*[@id="datasetForm:fileUpload"]/div[1]/span').click()
            self.sesh.implicitly_wait(3600)
            print("User input required: upload test_file_1_replace.txt")
            self.sesh.find_element('xpath', '//*[@id="filesHeaderCount"]') 
            self.sesh.implicitly_wait(10)
            print("Replace Completed")

            self.part = '04'
            # self.part = '05' #Drag and drop, untested

            self.part = '06'
            self.take_screenshot(shot:=1)

            self.part = '07'
            self.sesh.find_element('xpath', '//*[@id="datasetForm:fileUpload"]/div[1]/span')
            time.sleep(1 + self.extra_wait)
            self.assertEqual(self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileChecksum"]').text, self.md5_prefix + self.test_file_1_replace_md5)

            self.part = '08'
            time.sleep(1 + self.extra_wait)
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileName"]').clear()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileName"]').send_keys('test_file_1_replace_renamed.txt')
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDirectoryName"]').clear()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDirectoryName"]').send_keys('/testreplacefolder/')
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDescription"]').clear()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDescription"]').send_keys('test_file_replace_description')
            self.take_screenshot(shot:=1)

            self.part = '09'
            self.sesh.find_element('xpath','//*[@id="datasetForm:savebutton"]').click() #save
            self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") 
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
            print("User input required: upload test_file_2.png")
            self.sesh.find_element('xpath', '//*[@id="filesHeaderCount"]') 
            self.sesh.implicitly_wait(10)
            print("Upload Completed")

            self.part = '03'
            # self.part = '04' #Drag and drop, untested

            self.part = '05'
            self.sesh.find_element('xpath', '//*[@id="datasetForm:fileUpload"]/div[1]/span')
            self.assertEqual(self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileChecksum"]').text, self.md5_prefix + self.test_file_2_md5)

            self.part = '06'
            time.sleep(1 + self.extra_wait)
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileName"]').clear()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileName"]').send_keys('test_file_2_renamed.png')
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDirectoryName"]').clear()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDirectoryName"]').send_keys('/testfolder2/')
            self.take_screenshot(shot:=1)

            self.part = '07'
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDescription"]').clear()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:filesTable:0:fileDescription"]').send_keys('test_file_description2')
            self.take_screenshot(shot:=1)

            self.part = '08'
            self.sesh.find_element('xpath','//*[@id="datasetForm:savebutton"]').click() #save changes
            self.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") 
            self.take_screenshot(shot:=1) 

            self.set_end_time()

        self.set_req('18') #NOTE: Very similar to req 14. If you edit this also edit that
        self.set_start_time()

        self.part = '01' 

        self.sesh.execute_script(f"window.scrollTo(0, {3 * self.scroll_height})") 
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:0:fileInfoInclude-filesTable"]/div[2]/div[1]/a').text, 'test_file_1_replace_renamed.txt')
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:0:fileHierarchy"]').text, 'testreplacefolder/')
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:0:fileInfoInclude-filesTable"]/div[2]/div[2]/div[2]/span[1]').get_attribute('data-clipboard-text'), self.test_file_1_replace_md5)
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:0:fileDescNonEmpty"]').text, 'test_file_replace_description')

        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:1:fileInfoInclude-filesTable"]/div[2]/div[1]/a').text, 'test_file_2_renamed.png')
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:1:fileHierarchy"]').text, 'testfolder2/')
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:1:fileInfoInclude-filesTable"]/div[2]/div[2]/div[2]/span[1]').get_attribute('data-clipboard-text'), self.test_file_2_md5)
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:1:fileDescNonEmpty"]').text, 'test_file_description2')
        self.take_screenshot(shot:=1)

        self.part = '02'
        self.sesh.execute_script("window.scrollTo(0, 0)") 
        self.sesh.find_element('xpath', '//*[@id="editDataSet"]').click() #click add data
        self.sesh.find_element('xpath', '//*[@id="datasetForm:editMetadata"]').click() #click edit dataset
        # if not self.templates_exist: 
        #     self.confirm_dataset_metadata(add_string='edit', is_update=False, xpath_dict=self.ds_edit_xpaths_notemplate)
        # else:
        #NOTE: This seems to line up with notemplate even though there is one at this point? Maybe its different off a draft dataset instead of off a non-draft?
        #      If this blows up testing without a template, investigate more
        self.confirm_dataset_metadata(add_string='edit', is_update=True, xpath_dict=self.ds_edit_xpaths_notemplate)
        if self.do_screenshots:
            shot = 0
            for i in range(8):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:cancel"]').click() #click out after testing data

        self.part = '03' #terms (license)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView"]/ul/li[3]/a').click()
        time.sleep(.5 + self.extra_wait)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:termsTab"]/div[1]/a').click()
        time.sleep(1 + self.extra_wait)
        self.confirm_license(add_string='edit', xpath_dict=self.ds_license_edit_xpaths)
        if self.do_screenshots:
            shot = 0
            for i in range(3):
                self.sesh.execute_script(f"window.scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:cancel"]').click()

        self.set_end_time()

        time.sleep(1 + self.extra_wait)

#TODO: Add this code to a part (with screenshots) once we get clarity on which test the rest of the code are a part of
        if self.do_file_tests:
            self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div[2]/div/a').click() #click publish
        else:
            self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div[1]/div/a').click() #click publish
        
        time.sleep(1 + self.extra_wait)

        self.sesh.find_element('xpath', '//*[@id="datasetForm:publishDataset"]/div[2]/div[2]/button[1]').click()
        
        self.sesh.implicitly_wait(30)
        self.sesh.find_element('class name', 'label-default') #Find element to wait for load. May trigger prematurely with files added.
        self.sesh.implicitly_wait(10)
        if self.do_file_tests:
            self.assertEqual(self.sesh.find_element('xpath', '//*[@id="title-label-block"]/span').text, "Version 2.0") #Test dataset published
        else:
            self.assertEqual(self.sesh.find_element('xpath', '//*[@id="title-label-block"]/span').text, "Version 1.1") #Test dataset published
        
        self.sesh.find_element('xpath', '//*[@id="editDataSet"]').click() #click add data
        self.sesh.find_element('xpath', '//*[@id="datasetForm:editMetadata"]').click() #click new dataset

        if not self.templates_exist:
            self.confirm_dataset_metadata(add_string='edit', is_update=True, xpath_dict=self.ds_edit_xpaths_notemplate) 
        else:
            self.confirm_dataset_metadata(add_string='edit', is_update=True, xpath_dict=self.ds_edit_xpaths_yestemplate) 

        self.sesh.find_element('xpath', '//*[@id="datasetForm:cancelTop"]').click() #click cancel out of edit after testing
        time.sleep(5 + self.extra_wait) #We have to sleep after cancelling, even though test 21 just goes to another page, because it won't nav

    # The test of file upload requires manual interaction by the user, as automating selecting file via toe OS file picker is super painful
    # We may try to automate the file picker someday.
    # Or explore maybe some way to get around this with automating drag and drop https://stackoverflow.com/questions/38829153/
    # We may also want to implement another verison of this function that just uses the API to do file upload for when compliance is not an issue.
    def r21r22r23r24r25_dataset_file_discovery(self):
        self.set_req('21')
        self.set_start_time()

        self.part = '01' # enter search terms (basic)
        self.sesh.get(self.dv_url)
        time.sleep(5 + self.extra_wait)
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath','//*[@id="searchResults"]/div[2]/div[1]/form/div/div/input').send_keys('edit'+self.ds_props['title']) #each word is an inclusive or search
        self.take_screenshot(shot:=shot+1)

        self.part = '02' # click search button

        self.sesh.find_element('xpath', '//*[@id="searchResults"]/div[2]/div[1]/form/div/div/span').click()
        time.sleep(1 + self.extra_wait)
        self.take_screenshot(shot:=1)

        self.part = '03' # select relevant dataset
        self.sesh.find_element('xpath', '//*[@id="resultsTable"]/tbody/tr[1]/td/div/div[1]/a').click()
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="title"]').text, 'edit'+self.ds_props['title'])
        self.take_screenshot(shot:=1)

        self.part = '04' # click advanced search
        self.sesh.get(self.dv_url)
        time.sleep(1 + self.extra_wait)
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="searchResults"]/div[2]/div[1]/form/div/a').click()
        time.sleep(1 + self.extra_wait)
        self.take_screenshot(shot:=shot+1)

        self.part = '05' # enter metadata based search content
        self.sesh.find_element('xpath','//*[@id="advancedSearchForm:block:0:field:5:searchValue"]').send_keys('edit'+self.ds_props['keyword_term']) #each word is an inclusive or search
        self.take_screenshot(shot:=1)

        self.part = '06' # click find
        self.sesh.find_element('xpath', '//*[@id="advancedSearchForm"]/div[5]/button').click()
        time.sleep(1 + self.extra_wait)
        self.take_screenshot(shot:=1)

        self.part = '07' # select dataset
        self.sesh.find_element('xpath', '//*[@id="resultsTable"]/tbody/tr[1]/td/div/div[1]/a').click()
        self.assertEqual(self.sesh.find_element('xpath', '//*[@id="title"]').text, 'edit'+self.ds_props['title'])
        self.take_screenshot(shot:=1)

        self.set_end_time()

        self.set_req('22')
        self.set_start_time()

        self.part = '01' #nav to landing (already there)
        self.take_screenshot(shot:=1)

        self.part = '02' #nav to file tab, click a file
        self.sesh.execute_script("window.scrollTo(0, 600)") 
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:1:fileInfoInclude-filesTable"]/div[2]/div[1]/a').click() #click edit dataset
        time.sleep(2 + self.extra_wait)
        self.take_screenshot(shot:=shot+1)

        self.part = '03' #nav to metadata tab
        self.sesh.find_element('xpath', '//*[@id="breadcrumbLnk2"]').click() #click back to dataset
        time.sleep(2 + self.extra_wait)
        self.sesh.execute_script("window.scrollTo(0, 600)") 
        self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView"]/ul/li[2]/a').click()
        time.sleep(.2 + self.extra_wait)
        self.take_screenshot(shot:=1)

        self.part = '04' #nav to terms tab
        self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView"]/ul/li[3]/a').click()
        time.sleep(.2 + self.extra_wait)
        self.take_screenshot(shot:=1)
        self.set_end_time()

        #This code is not part of a req per say. But we need another version of the dataset for version testing, and more files to garuntee enough objects for browse pagination

        if self.do_file_tests:
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView"]/ul/li[1]/a').click()
            time.sleep(1 + self.extra_wait)
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:filesButtons"]/a').click()
            time.sleep(1 + self.extra_wait)
            self.sesh.find_element('xpath', '//*[@id="datasetForm:fileUpload"]/div[1]/span').click()
            self.sesh.implicitly_wait(3600)
            print("User input required: upload 6 pagination files (select multiple in the system dialog).")
            self.sesh.find_element('xpath', '//*[@id="filesHeaderCount"]') 
            self.sesh.implicitly_wait(10)
            print("Upload Completed")
            self.sesh.find_element('xpath','//*[@id="datasetForm:savebutton"]').click() #save files

        self.set_req('23')
        self.set_start_time()

        self.part = '01' #nav to dataset and then version tab
        time.sleep(1 + self.extra_wait)
        self.take_screenshot(shot:=1)
        self.sesh.execute_script("window.scrollTo(0, 600)") 
        self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView"]/ul/li[4]/a').click()
        time.sleep(.2 + self.extra_wait)
        self.take_screenshot(shot:=shot+1)

        self.part = '02' #click version details for a version
        self.take_screenshot(shot:=1)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:versionsTable_data"]/tr[2]/td[3]/a').click()
        time.sleep(2 + self.extra_wait)
        if self.do_screenshots:
            for i in range(4):
                self.sesh.execute_script(f"document.getElementById('datasetForm:detailsBlocks_content').scrollTo(0, {i * self.scroll_height})") 
                self.take_screenshot(shot:=shot+1)
        self.sesh.find_element('xpath', '//*[@id="datasetForm:detailsBlocks"]/div[1]/a').click()

        if self.do_file_tests: #Requires files currently because uploading of the files creates the draft version which creates 3 version and enabled the checkbox compare dialog
            time.sleep(1 + self.extra_wait)
            self.take_screenshot(shot:=shot+1)
            self.part = '03' #compare two versions
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:versionsTable_data"]/tr[3]/td[1]/div/div/span').click()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:versionsTable_data"]/tr[1]/td[1]/div/div/span').click()
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:versionsTab"]/div[1]/button[1]').click()
            time.sleep(2 + self.extra_wait)
            if self.do_screenshots:
                shot = 0
                for i in range(5):
                    self.sesh.execute_script(f"document.getElementById('datasetForm:detailsBlocks_content').scrollTo(0, {i * self.scroll_height})") 
                    self.take_screenshot(shot:=shot+1)
            self.sesh.find_element('xpath', '//*[@id="datasetForm:detailsBlocks"]/div[1]/a').click()

        self.set_end_time()

        self.set_req('24')
        self.set_start_time()

        if self.do_file_tests: #Requires files currently because we upload 6 additional files to have enough files to ensure pagination exists
            self.part = '01' #from main page, exercise pagination.
            self.sesh.get(self.dv_url)
            self.sesh.find_element('xpath', '//*[@id="facetType"]/div[3]/a[1]/div/div[2]/span').click()
            time.sleep(1 + self.extra_wait)
            self.take_screenshot(shot:=1)
            self.sesh.execute_script("window.scrollTo(0, 600)") 
            self.take_screenshot(shot:=shot+1)
            self.sesh.execute_script("window.scrollTo(0, 1200)") 
            self.take_screenshot(shot:=shot+1)
            self.sesh.find_element('xpath', '//*[@id="dv-main"]/div[2]/ul/li[4]/a').click()
            time.sleep(2 + self.extra_wait)
            self.take_screenshot(shot:=shot+1)
            self.sesh.execute_script("window.scrollTo(0, 600)") 
            self.take_screenshot(shot:=shot+1)
            self.sesh.execute_script("window.scrollTo(0, 1200)") 
            self.take_screenshot(shot:=shot+1)

        self.part = '02' #use metadata facet to filter
        self.sesh.get(self.dv_url)
        time.sleep(1 + self.extra_wait)
        self.take_screenshot(shot:=1)
        self.sesh.get(f'{self.dv_url}/dataverse/root?q=&fq1=keywordValue_ss%3A%22edit{self.ds_props["keyword_term"]}%22&fq0=dvObjectType%3A%28dataverses+OR+datasets+OR+files%29&types=dataverses%3Adatasets%3Afiles&sort=dateSort&order=') 
        time.sleep(1 + self.extra_wait)
        self.take_screenshot(shot:=shot+1)

        self.part = '03' #select dataset
        self.sesh.find_element('xpath', '//*[@id="resultsTable"]/tbody/tr[2]/td/div/div[1]/a/span').click()
        time.sleep(1 + self.extra_wait)
        self.take_screenshot(shot:=1)

        self.set_end_time()

        self.set_req('25')
        self.set_start_time()
        if self.do_file_tests:
            self.part = '01' #navigate to dataset
            self.take_screenshot(shot:=1)

            self.part = '02' #download individual file via access file icon next to file info
            self.sesh.execute_script("window.scrollTo(0, 900)") 
            self.take_screenshot(shot:=1)
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable_data"]/tr[2]/td[3]/div/div[1]/a[2]/span[1]').click()
            time.sleep(2 + self.extra_wait)
            self.take_screenshot(shot:=shot+1)
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable_data"]/tr[2]/td[3]/div/div[1]/ul/li[4]/a').click()
            time.sleep(2 + self.extra_wait)
            downloaded_hash_single = hashlib.md5(open(f'{self.download_full_path}/test_file_2_renamed.png', 'rb').read()).hexdigest()
            self.assertEqual(self.test_file_2_md5, downloaded_hash_single)

            self.part = '03' #select multiple files for download
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable_data"]/tr[1]/td[1]/div/div').click()
            time.sleep(1 + self.extra_wait)
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable_data"]/tr[3]/td[1]/div/div').click()
            time.sleep(1 + self.extra_wait)
            self.sesh.execute_script("window.scrollTo(0, 900)") 
            self.take_screenshot(shot:=1)

            self.part = '04' #download files via download button above list
            self.sesh.find_element('xpath', '//*[@id="datasetForm:tabView:filesTable:downloadButtonBlockNormal"]/a').click()
            time.sleep(4 + self.extra_wait)
            with ZipFile(f'{self.download_full_path}/dataverse_files.zip', 'r') as zip_ref:
                zip_ref.extractall(f'{self.download_full_path}/zipfolder/')

            downloaded_hash_folder_file_1_replaced = hashlib.md5(open(f'{self.download_full_path}/zipfolder/testreplacefolder/test_file_1_replace_renamed.txt', 'rb').read()).hexdigest()
            self.assertEqual(self.test_file_1_replace_md5, downloaded_hash_folder_file_1_replaced)

        self.set_end_time()

### Non-test functions ###

    def take_screenshot(self, shot):
        if self.do_screenshots: 
            dict_key = f'r{self.req}_p{self.part}_s{"%02d" % (shot)}'
            if dict_key in self.screenshots.keys():
                raise Exception("Duplicate screenshot key encountered. Check test code.")
            self.screenshots[dict_key] = self.sesh.get_screenshot_as_base64()

    def set_start_time(self):
        self.start_times[int(self.req)] = time.time()

    def set_end_time(self):
        self.end_times[int(self.req)] = time.time()