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

# PLAN: Write generic python functions that call asserts on a TestCase, similar to how we used testthat.
#       These can then be called via a caller to test for an exception in R.
#       These can also be called later in a more normal unittest test suite

def add(x, y):
  return x + y

def test_caller():
  try:
    tc = unittest.TestCase()
    test_assert(tc)
    return True
  except Exception as e:
    #print(type(e).__name__ + ":", e)
    #print(traceback.format_exc())
    traceback.print_exc()
    return False

def test_assert(tc):
  tc.assertIn("| CORE2 Admin Site", "NOPE")
  tc.assertIn("YEP", "NOPE")
  
def test_selenium():
  options = Options()
  selenium = webdriver.Chrome(ChromeDriverManager().install(), options=options)
  selenium.get("https://xkcd.com")
