###################################
### Dataverse Test Dictionaries ###
###################################

dv_props = {
  'host_dataverse': 'Root',
  'name': 'name', #dataverse_name,
  'affiliation': 'Odum',
  'identifier': 'identifier', #dataverse_name,
  'category': 'Journal',
  'email': 'test@example.com',
  'description': 'this is a test description'
}

###########################################
### Dataverse Test Additional Functions ###
###########################################'


def set_dataverse_metadata(tc, add_string=''):
  # We clear all the elements for when this code is called during edit and there are already contents
  self.sesh.find_element('xpath','//*[@id="dataverseForm:name"]').clear()
  self.sesh.find_element('xpath','//*[@id="dataverseForm:name"]').send_keys(add_string + dv_props['name'])
  self.sesh.find_element('xpath','//*[@id="dataverseForm:affiliation"]').clear()
  self.sesh.find_element('xpath','//*[@id="dataverseForm:affiliation"]').send_keys(add_string + dv_props['affiliation'])
  self.sesh.find_element('xpath','//*[@id="dataverseForm:identifier"]').clear()
  self.sesh.find_element('xpath','//*[@id="dataverseForm:identifier"]').send_keys(add_string + dv_props['identifier'])
  #TODO: How are we fixing this in python?
  #dataverse_name <<- paste(add_string, dv_props['identifier'])
  self.sesh.find_element('xpath','//*[@id="dataverseForm:dataverseCategory"]').send_keys(list(dv_props['category']))
  self.sesh.find_element('xpath','//*[@id="dataverseForm:j_idt271:0:contactEmail"]').clear()
  self.sesh.find_element('xpath','//*[@id="dataverseForm:j_idt271:0:contactEmail"]').send_keys(add_string + dv_props['email'])
  self.sesh.find_element('xpath','//*[@id="dataverseForm:description"]').clear()
  self.sesh.find_element('xpath','//*[@id="dataverseForm:description"]').send_keys(add_string + dv_props['description'])
  
  self.sesh.find_element('xpath','//*[@id="dataverseForm:save"]').click() #create dataverse

def test_dataverse_metadata(tc, add_string=''):
  #TODO: Do we really need this navigate?
  #      ... Also, we could have maybe just tested this content from the edit page after saving. But maybe this is better?
  sesh.get(dv_server_url + '/dataverse/' + dataverse_name + '/')
   
  ### Dataverse Page - Test Save Results ###
  
  tc.assertEqual((self.sesh.find_element('xpath','//*[@id="breadcrumbLnk0"]').text, dv_props['host_dataverse'])
  tc.assertEqual((self.sesh.find_element('xpath','//*[@id="dataverseHeader"]/div/div/a/h1').text, add_string+dv_props['name'])
  tc.assertEqual((self.sesh.find_element('xpath','//*[@id="dataverseHeader"]/div/div/span[1]').text, '('+add_string+dv_props['affiliation']+')')
  tc.assertEqual((sesh.current_url), paste(dv_server_url,'/dataverse/', add_string, dv_props['identifier'], '/')
  tc.assertEqual((self.sesh.find_element('xpath','//*[@id="dataverseDesc"]').text, add_string+dv_props['description'])
  
  ### Dataverse Edit Page - Test Save Results Additional ###
  # Category and contactEmail do not show up in the overview (public) page, so we test them here
  
  self.sesh.find_element('xpath','//*[@id="actionButtonBlock"]/div/div/div[2]/div[2]/button').click()
  self.sesh.find_element('xpath','//*[@id="dataverseForm:editInfo"]').click()
  
  tc.assertEqual((self.sesh.find_element('xpath','//*[@id="dataverseForm:dataverseCategory"]/option[@selected]').text, dv_props['category'])
  tc.assertEqual((self.sesh.find_element('xpath','//*[@id="dataverseForm:j_idt271:0:contactEmail"]').get_attribute('value'), add_string+dv_props['email'])
  
  self.sesh.find_element('xpath','//*[@id="dataverseForm:cancel"]').click()
