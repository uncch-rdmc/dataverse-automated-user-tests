import time, unittest, os, traceback
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

class RequirementTests:
  exec(compile(source=open('/Users/madunlap/Documents/GitHub/secret_table_user_test.py').read(), filename='.', mode='exec')) #Reads file with secret info.
  sesh = None
  test_case = None
  failed = False
  test_case = unittest.TestCase()
  username = None
  password = None
  
  def r01alt_mainpath_builtin_auth(self, tc):
    self.sesh.get(f'{DV_URL}/loginpage.xhtml?redirectPage=%2Fdataverse.xhtml')
    self.sesh.find_element('xpath', '//*[@id="loginForm:credentialsContainer:0:credValue"]').send_keys(self.username)
    self.sesh.find_element('xpath', '//*[@id="loginForm:credentialsContainer:1:sCredValue"]').send_keys(self.password)
    self.sesh.find_element('xpath', '//*[@id="loginForm:login"]').click()
    
    self.sesh.find_element('xpath', '//*[@id="dataverseDesc"]') #Find element to wait for load
    tc.assertEqual(f'{DV_URL}/dataverse.xhtml', self.sesh.current_url)
   
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
    
    
    
    
    
    
