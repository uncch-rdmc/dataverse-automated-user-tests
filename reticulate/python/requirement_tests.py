import time, unittest, os, traceback

#TODO: These import paths will almost certainly break when running this code outside R. Not sure how to fix this.
#      ... Ideally there would be some way to tell reticulate what directory to work from?
import python.dataset_test_helper as dst
import python.dataverse_test_helper as dvt

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
#from seleniumwire import webdriver
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from webdriver_manager.chrome import ChromeDriverManager

#TODO: 
# - How am I handling one test failing causing the others to not run?
#   - Should we build it into python or r?
# - Can we make this code useful for people testing without R?

exec(compile(source=open('/Users/madunlap/Documents/GitHub/secret_table_user_test.py').read(), filename='.', mode='exec')) #Reads file with secret info.

class RequirementTests:
  sesh = None
  test_case = None
  failed = False
  test_case = unittest.TestCase()
  username = None
  password = None
  
  #TODO: we may want to reference our dataset title, dataverse name and dataverse identifier from the dictionaries instead of a global like before
  # ...  or we completely avoid the dictionaries. it probably can't live in two places.
  
  def r01alt_mainpath_builtin_auth(self, tc):
    self.sesh.get(f'{DV_URL}/loginpage.xhtml?redirectPage=%2Fdataverse.xhtml')
    self.sesh.find_element('xpath', '//*[@id="loginForm:credentialsContainer:0:credValue"]').send_keys(self.username)
    self.sesh.find_element('xpath', '//*[@id="loginForm:credentialsContainer:1:sCredValue"]').send_keys(self.password)
    self.sesh.find_element('xpath', '//*[@id="loginForm:login"]').click()
    
    self.sesh.find_element('xpath', '//*[@id="dataverseDesc"]') #Find element to wait for load
    tc.assertEqual(f'{DV_URL}/dataverse.xhtml', self.sesh.current_url)
  
  ### UNTESTED REQUIREMENT TESTS  
  def r03_mainpath_create_sub_dataverse(self, tc):
    self.sesh.get(DV_URL)
    ### Main Landing Page ###
    self.sesh.find_element('xpath', '//*[@id="addDataForm"]/div/button').click() #click add data
    self.sesh.find_element('xpath', '//*[@id="addDataForm"]/div/ul/li[1]/a').click() #click new dataverse
    
    ### Create Dataverse Page ###
    self.sesh.find_element('xpath', '//*[@id="dataverseForm:selectHostDataverse_input"]').clear()
    self.sesh.find_element('xpath', '//*[@id="dataverseForm:selectHostDataverse_input"]').send_keys(dv_props["host_dataverse"])
    time.sleep(2) # wait for host list to load
    self.sesh.find_element('xpath', '//*[@id="dataverseForm:selectHostDataverse_input"]').send_keys(Keys.ENTER)
    time.sleep(.5) # wait after click for ui to be usable
    dvt.set_dataverse_metadata(self.sesh, tc, add_string="create") #Metadata that is same for create/edit
   
    ### Test Save ###
    tc.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div').get_attribute("class"), "alert alert-success") #confirm success alert
    print("requirement_test dvt.dataverse_name:" + dvt.dataverse_name)
    tc.assertEqual(DV_URL+'/dataverse/'+dvt.dataverse_name+'/', self.sesh.current_url) #confirm page
    
    test_dataverse_metadata(self.sesh, tc, add_string="create")
    self.sesh.get(DV_URL+'/dataverse/'+dvt.dataverse_name)
    
    ### Dataverse Page - Publish ###
    
    self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div/div/div[2]/button').click() #click publish
    self.sesh.find_element('xpath', '//*[@id="dataverseForm:j_idt431"]').click() #confirm publish
    
    tc.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div').get_attribute("class"), "alert alert-success") #confirm success alert
    
    dataverse_id <<- sub(".*=", "", self.sesh.find_element('xpath', '//*[@id="dataverseForm:themeWidgetsOpts"]').get_attribute("href")) 
  
  def r04_mainpath_edit_dataverse(self, tc):
    self.sesh.get(DV_URL+'/dataverse/'+dvt.dataverse_name)
    time.sleep(default_wait)
    self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div/div/div[2]/div[2]/button').click()
    self.sesh.find_element('xpath', '//*[@id="dataverseForm:editInfo"]').click()
    
    set_dataverse_metadata(self.sesh, tc)
    test_dataverse_metadata(self.sesh, tc)
    
    time.sleep(1) #wait before switching pages in r05
  
  def r05_mainpath_create_metadata_template(self, tc):
    self.sesh.get(DV_URL+'/dataverse/'+dvt.dataverse_name)
    time.sleep(default_wait)
  
    self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div/div/div[2]/div[2]/button').click() #click dataverse edit button
    self.sesh.find_element('xpath', '//*[@id="dataverseForm:manageTemplates"]').click() #click manage templates
    time.sleep(default_wait)
    self.sesh.find_element('xpath', '//*[@id="manageTemplatesForm"]/div[1]/div/a').click() #click create dataset template
    time.sleep(default_wait)
    self.sesh.find_element('xpath', '//*[@id="templateForm:templateName"]').send_keys("test template create") #Create template title
    set_dataset_metadata_edit(self.sesh, tc, add_string='create', xpath_dict=ds_template_xpaths)
    
    self.sesh.find_element('xpath', '//*[@id="templateForm:j_idt620:0:j_idt623:0:instr"]').click()
    time.sleep(.2)
  #TODO: What?
    self.sesh.switch_to.active_element.send_keys("test"+"WOWOWOWOW")
    time.sleep(999999999999)
    
      
    self.sesh.find_element('xpath', '//*[@id="templateForm:j_idt892"]').click() #click "Save + Add Terms"
  
    tc.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") #confirm success alert
    
  #TODO: Replace param_get with a new way to get the query params from a url
    template_id <<- param_get(self.sesh.current_url, "id")
  
    set_template_license(self.sesh, tc, add_string='create')
    self.sesh.find_element('xpath', '//*[@id="templateForm:j_idt893"]').click() #click "Save Dataset Template" (which actually just saves the license)
    
    tc.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") #confirm success alert
    time.sleep(default_wait) #not sure why I have to do this but ok? Shouldn't confirming the alert work?
    
    self.sesh.get(DV_URL+'/template.xhtml?id='+template_id+'&ownerId='+dataverse_id+'&editMode=METADATA')
    test_dataset_metadata(self.sesh, tc, add_string='create', xpath_dict=ds_template_xpaths)
    
    self.sesh.get(DV_URL+'/template.xhtml?id='+template_id+'&ownerId='+dataverse_id+'&editMode=LICENSE')
    test_template_license(self.sesh, tc, add_string='create')
  
  def r06_mainpath_edit_metadata_template(self, tc):
    self.sesh.get(DV_URL+'/template.xhtml?id='+template_id+'&ownerId='+dataverse_id+'&editMode=METADATA')
    set_dataset_metadata_edit(self.sesh, tc, add_string='edit', xpath_dict=ds_template_xpaths)
    self.sesh.find_element('xpath', '//*[@id="templateForm:j_idt893"]').click() #click "Save + Add Terms"
    tc.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") #confirm success alert
    
    self.sesh.get(DV_URL+'/template.xhtml?id='+template_id+'&ownerId='+dataverse_id+'&editMode=LICENSE')
    set_template_license(self.sesh, tc, add_string='edit')
    self.sesh.find_element('xpath', '//*[@id="templateForm:j_idt893"]').click() #click "Save Changes"
    time.sleep(default_wait) #not sure why I have to do this but ok? Shouldn't confirming the alert work?
    
    self.sesh.get(DV_URL+'/template.xhtml?id='+template_id+'&ownerId='+dataverse_id+'&editMode=METADATA')
    test_dataset_metadata(self.sesh, tc, add_string='edit', xpath_dict=ds_template_xpaths)
    
    self.sesh.get(DV_URL+'/template.xhtml?id='+template_id+'&ownerId='+dataverse_id+'&editMode=LICENSE')
    test_template_license(self.sesh, tc, add_string='edit')
  
  def r09_mainpath_create_dataset(self, tc):
    self.sesh.get(DV_URL+'/dataverse/'+dvt.dataverse_name)
    
    self.sesh.find_element('xpath', '//*[@id="addDataForm"]/div/button').click() #click add data
    self.sesh.find_element('xpath', '//*[@id="addDataForm"]/div/ul/li[2]/a').click() #click new dataset
    
    set_dataset_metadata_create(self.sesh, tc, add_string='create')
    
    tc.assertEqual(self.sesh.find_element('xpath', '//*[@id="messagePanel"]/div/div[1]').get_attribute("class"), "alert alert-success") #confirm success alert
    
    ### Get dataset id from permissions page url for later uses ###
    dataset_id <<- sub(".*=", "", self.sesh.find_element('xpath', '//*[@id="datasetForm:manageDatasetPermissions"]').get_attribute("href")) 
    # print(dataset_id)
    
    self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div[1]/div/a').click() #click publish
  
    self.sesh.find_element('xpath', '//*[@id="datasetForm:j_idt2547"]').click() #click publish confirm
  
    self.sesh.find_element('xpath', 'label-default', using='class name') #Find element to wait for load. May trigger prematurely with files added.
    tc.assertEqual(self.sesh.find_element('xpath', '//*[@id="title-label-block"]/span').text, "Version 1.0") #Test dataset published
    
    self.sesh.find_element('xpath', '//*[@id="editDataSet"]').click() #click add data
    self.sesh.find_element('xpath', '//*[@id="datasetForm:editMetadata"]').click() #click edit dataset
    
    test_dataset_metadata(self.sesh, tc, add_string='create', is_update=FALSE, xpath_dict=ds_edit_xpaths)
    
    self.sesh.find_element('xpath', '//*[@id="datasetForm:cancel"]').click() #click out after testing data
    
    time.sleep(default_wait)
  
  def r10_mainpath_edit_dataset(self, tc):
    self.sesh.find_element('xpath', '//*[@id="editDataSet"]').click() #click add data
    self.sesh.find_element('xpath', '//*[@id="datasetForm:editMetadata"]').click() #click new dataset
  
    set_dataset_metadata_edit(self.sesh, tc, add_string='edit', xpath_dict=ds_edit_xpaths)
    self.sesh.find_element('xpath', '//*[@id="datasetForm:saveBottom"]').click() #click to create dataset
  
    self.sesh.find_element('xpath', '//*[@id="actionButtonBlock"]/div[1]/div/a').click() #click publish
  
    self.sesh.find_element('xpath', '//*[@id="datasetForm:j_idt2547"]').click() #click publish confirm
    
    self.sesh.find_element('xpath', 'label-default', using='class name') #Find element to wait for load. May trigger prematurely with files added.
    tc.assertEqual(self.sesh.find_element('xpath', '//*[@id="title-label-block"]/span').text, "Version 1.1") #Test dataset published
    
    self.sesh.find_element('xpath', '//*[@id="editDataSet"]').click() #click add data
    self.sesh.find_element('xpath', '//*[@id="datasetForm:editMetadata"]').click() #click new dataset
    
    test_dataset_metadata(self.sesh, tc, add_string='edit', is_update=TRUE, xpath_dict=ds_edit_xpaths) 
  
    self.sesh.find_element('xpath', '//*[@id="datasetForm:cancelTop"]').click() #click cancel out of edit after testing
  
  #############################################
  ### Requirement Test Additional Functions ###
  #############################################
  
  def begin_user_browser(self, tc):
    options = Options()
    self.sesh = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    self.sesh.implicitly_wait(20) #Set high for dataset publish. Maybe we should keep it low normally and set it up when needed?

  def test_caller(self, req_funct):
    if self.failed:
      return False
    
    try:
      req_funct(self.test_case)
      #test_assert(self.test_case)
      return True
    except Exception as e:
      self.failed = True
      #print(type(e).__name__ + ":", e)
      #print(traceback.format_exc())
      traceback.print_exc()
      return False
  
  #For use when getting the results of the individual steps doesn't matter. Not used by our R code  
  #TODO: make username/password optional somehow whe we do oauth
  def linear_test_runner(self, username, password):
    print(f"Set username/password: {self.set_username_password(username, password)}")
    print(f"Begin Browser: {self.test_caller(self.begin_user_browser)}")
    print(f"R01alt mainpath auth: {self.test_caller(self.r01alt_mainpath_builtin_auth)}")
    self.sesh.close()
    return self.failed
    
  def set_username_password(self, username, password):
    self.username = username
    self.password = password
    
    
    
    
    
    
