dataverse_name = "test_dataverse"

###################################
### Dataverse Test Dictionaries ###
###################################

dv_props = {
  'host_dataverse': 'Root',
  'name': dataverse_name,
  'affiliation': 'Odum',
  'identifier': dataverse_name,
  'category': 'Journal',
  'email': 'test@example.com',
  'description': 'this is a test description'
}

###########################################
### Dataverse Test Additional Functions ###
###########################################'


def set_dataverse_metadata(sesh, tc, add_string=''):
  # We clear all the elements for when this code is called during edit and there are already contents
  sesh.find_element('xpath','//*[@id="dataverseForm:name"]').clear()
  sesh.find_element('xpath','//*[@id="dataverseForm:name"]').send_keys(add_string + dv_props['name'])
  sesh.find_element('xpath','//*[@id="dataverseForm:affiliation"]').clear()
  sesh.find_element('xpath','//*[@id="dataverseForm:affiliation"]').send_keys(add_string + dv_props['affiliation'])
  sesh.find_element('xpath','//*[@id="dataverseForm:identifier"]').clear()
  sesh.find_element('xpath','//*[@id="dataverseForm:identifier"]').send_keys(add_string + dv_props['identifier'])
  #TODO: How are we fixing this in python?
  dataverse_name = add_string+dv_props['identifier']
  print("dataverse_test_helper dataverse_name:" + dataverse_name)
  #dataverse_name <<- paste(add_string, dv_props['identifier'])
  sesh.find_element('xpath','//*[@id="dataverseForm:dataverseCategory"]').send_keys(list(dv_props['category']))
  sesh.find_element('xpath','//*[@id="dataverseForm:j_idt271:0:contactEmail"]').clear()
  sesh.find_element('xpath','//*[@id="dataverseForm:j_idt271:0:contactEmail"]').send_keys(add_string + dv_props['email'])
  sesh.find_element('xpath','//*[@id="dataverseForm:description"]').clear()
  sesh.find_element('xpath','//*[@id="dataverseForm:description"]').send_keys(add_string + dv_props['description'])
  
  sesh.find_element('xpath','//*[@id="dataverseForm:save"]').click() #create dataverse

def test_dataverse_metadata(sesh, tc, add_string=''):
  #TODO: Do we really need this navigate?
  #      ... Also, we could have maybe just tested this content from the edit page after saving. But maybe this is better?
  sesh.get(dv_server_url + '/dataverse/' + dataverse_name + '/')
   
  ### Dataverse Page - Test Save Results ###
  
  tc.assertEqual(sesh.find_element('xpath','//*[@id="breadcrumbLnk0"]').text, dv_props['host_dataverse'])
  tc.assertEqual(sesh.find_element('xpath','//*[@id="dataverseHeader"]/div/div/a/h1').text, add_string+dv_props['name'])
  tc.assertEqual(sesh.find_element('xpath','//*[@id="dataverseHeader"]/div/div/span[1]').text, '('+add_string+dv_props['affiliation']+')')
  tc.assertEqual(sesh.current_url), paste(dv_server_url,'/dataverse/', add_string, dv_props['identifier'], '/')
  tc.assertEqual(sesh.find_element('xpath','//*[@id="dataverseDesc"]').text, add_string+dv_props['description'])
  
  ### Dataverse Edit Page - Test Save Results Additional ###
  # Category and contactEmail do not show up in the overview (public) page, so we test them here
  
  sesh.find_element('xpath','//*[@id="actionButtonBlock"]/div/div/div[2]/div[2]/button').click()
  sesh.find_element('xpath','//*[@id="dataverseForm:editInfo"]').click()
  
  tc.assertEqual(sesh.find_element('xpath','//*[@id="dataverseForm:dataverseCategory"]/option[@selected]').text, dv_props['category'])
  tc.assertEqual(sesh.find_element('xpath','//*[@id="dataverseForm:j_idt271:0:contactEmail"]').get_attribute('value'), add_string+dv_props['email'])
  
  sesh.find_element('xpath','//*[@id="dataverseForm:cancel"]').click()
