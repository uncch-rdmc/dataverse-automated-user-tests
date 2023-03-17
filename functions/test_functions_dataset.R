#########################################
### Dataset Test Additional Functions ###
#########################################

ds_props <- c(
  #'host_dataverse'='',
  'title'=dataset_name,
  'author_name'='author',
  'author_affiliation'='affiliation',
  #'author_id_type'='ORCID',
  'author_id'='author_affil_id',
  'contact_name'='contact',
  'contact_affiliation'='contact_affil',
  'contact_email'='test@example.com',
  'description'='this is a test description',
  'date'='2022-11-11',
  'subject'='Physics',
  'keyword_term'='keyword',
  'keyword_cv_name'='vocab_name',
  'keyword_cv_url'='https://odum.unc.edu/',
  'related_pub_citation'='this is a test citation',
  #'related_pub_id_type'='lissn',
  'related_pub_id'='pub_id',
  'related_pub_url'='https://odum.unc.edu/',
  'notes'='this is a test note',
  'depositor'='a depositor',
  'deposit_date'='2020-01-01',
  
  'subtitle'='subtitle',
  'alternative_title'='alternative_title',
  'alternative_url'='https://odum.unc.edu/',
  'other_id_agency'='other_id_agency',
  'other_id_id'='other_id_id',
  'topic_class_term'='topic_class_term',
  'topic_class_cv_name'='topic_class_cv_name',
  'topic_class_cv_url'='https://odum.unc.edu/',
  'language'='language',
  'producer_name'='producer_name',
  'producer_affiliation'='produder_affiliation',
  'producer_abbrev_name'='produder_abbrev_name',
  'producer_url'='https://odum.unc.edu/',
  'producer_logo_url'='https://odum.unc.edu/',
  'producer_date'='2020-01-01',
  'producer_location'='produder_location',
  'contributor_type'='contributor_type',
  'contributor_name'='contributor_name',
  'funding_info_agency'='funding_info_agency',
  'funding_info_id'='funding_info_id',
  'distributor_name'='distributor_name',
  'distributor_affiliation'='distributor_affiliation',
  'distributor_abbrev_name'='distributor_abbrev_name',
  'distributor_url'='https://odum.unc.edu/',
  'distributor_logo_url'='https://odum.unc.edu/',
  'distribution_date'='2020-01-01',
  'time_period_start'='2020-01-01',
  'time_period_end'='2020-01-02',
  'date_of_collection_start'='2020-01-01',
  'date_of_collection_end'='2020-01-02',
  'data_type'='data_type',
  'series_name'='series_name',
  'series_info'='series_info',
  'software_name'='software_name',
  'software_version'='software_version',
  'related_material'='related_material',
  'related_dataset'='related_dataset',
  'other_reference'='other_reference',
  'data_source'='data_source',
  'origin_hist_sources'='origin_hist_sources',
  'character_of_sources'='character_of_sources',
  'doc_to_sources'='doc_to_sources'
)

# Used both for editing and seeing results of create/edit
ds_edit_xpaths <- c(
  #'host_dataverse'='',
  'title'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:0:fieldvaluelist:0:inputText"]',
  'author_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:0:inputText"]',
  'author_affiliation'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:1:inputText"]',
  #'author_id_type'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:2:cvv_label"]',
  'author_id'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:3:inputText"]',
  'contact_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:6:j_idt1679:0:j_idt1681:0:inputText"]',
  'contact_affiliation'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:6:j_idt1679:0:j_idt1681:1:inputText"]',
  'contact_email'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:6:j_idt1679:0:j_idt1681:2:inputText"]',
  'description'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:7:j_idt1679:0:j_idt1681:0:description"]',
  'date'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:7:j_idt1679:0:j_idt1681:1:inputText"]',
  #'subject'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:8:unique2"]/ul/li/span[1]', #This probably won't work due to the weirdness of the dropdown. Definitely not for create
  'keyword_term'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:9:j_idt1679:0:j_idt1681:0:inputText"]',
  'keyword_cv_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:9:j_idt1679:0:j_idt1681:1:inputText"]',
  'keyword_cv_url'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:9:j_idt1679:0:j_idt1681:2:inputText"]',
  'related_pub_citation'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:0:description"]',
  #'related_pub_id_type'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:1:cvv_label"]', #Also might not work
  'related_pub_id'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:2:inputText"]',
  'related_pub_url'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:3:inputText"]',
  'notes'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:12:fieldvaluelist:0:description"]',
  'depositor'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:21:fieldvaluelist:0:inputText"]',
  'deposit_date'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:22:fieldvaluelist:0:inputText"]',
  
  'subtitle'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:1:fieldvaluelist:0:inputText"]',
  'alternative_title'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:2:fieldvaluelist:0:inputText"]',
  'alternative_url'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:3:fieldvaluelist:0:inputText"]',
  'other_id_agency'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:4:j_idt1679:0:j_idt1681:0:inputText"]',
  'other_id_id'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:4:j_idt1679:0:j_idt1681:1:inputText"]',
  'topic_class_term'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:10:j_idt1679:0:j_idt1681:0:inputText"]',
  'topic_class_cv_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:10:j_idt1679:0:j_idt1681:1:inputText"]',
  'topic_class_cv_url'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:10:j_idt1679:0:j_idt1681:2:inputText"]',
  #'language'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:13:unique2"]/ul/li/span[2]', #This probably doesn't work, like subject
  'producer_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:14:j_idt1679:0:j_idt1681:0:inputText"]',
  'producer_affiliation'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:14:j_idt1679:0:j_idt1681:1:inputText"]',
  'producer_abbrev_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:14:j_idt1679:0:j_idt1681:2:inputText"]',
  'producer_url'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:14:j_idt1679:0:j_idt1681:3:inputText"]',
  'producer_logo_url'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:14:j_idt1679:0:j_idt1681:4:inputText"]',
  'producer_date'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:15:fieldvaluelist:0:inputText"]',
  'producer_location'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:16:fieldvaluelist:0:inputText"]',
  #'contributor_type'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:17:j_idt1679:0:j_idt1681:0:cvv_label"]',
  'contributor_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:17:j_idt1679:0:j_idt1681:1:inputText"]',
  'funding_info_agency'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:18:j_idt1679:0:j_idt1681:0:inputText"]',
  'funding_info_id'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:18:j_idt1679:0:j_idt1681:1:inputText"]',
  'distributor_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:19:j_idt1679:0:j_idt1681:0:inputText"]',
  'distributor_affiliation'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:19:j_idt1679:0:j_idt1681:1:inputText"]',
  'distributor_abbrev_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:19:j_idt1679:0:j_idt1681:2:inputText"]',
  'distributor_url'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:19:j_idt1679:0:j_idt1681:3:inputText"]',
  'distributor_logo_url'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:19:j_idt1679:0:j_idt1681:4:inputText"]',
  'distribution_date'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:20:fieldvaluelist:0:inputText"]',
  'time_period_start'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:23:j_idt1679:0:j_idt1681:0:inputText"]',
  'time_period_end'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:23:j_idt1679:0:j_idt1681:1:inputText"]',
  'date_of_collection_start'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:24:j_idt1679:0:j_idt1681:0:inputText"]',
  'date_of_collection_end'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:24:j_idt1679:0:j_idt1681:1:inputText"]',
  'data_type'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:25:fieldvaluelist:0:inputText"]',
  'series_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:26:j_idt1679:0:j_idt1681:0:inputText"]',
  'series_info'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:26:j_idt1679:0:j_idt1681:1:description"]',
  'software_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:27:j_idt1679:0:j_idt1681:0:inputText"]',
  'software_version'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:27:j_idt1679:0:j_idt1681:1:inputText"]',
  'related_material'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:28:fieldvaluelist:0:description"]',
  'related_dataset'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:29:fieldvaluelist:0:description"]',
  'other_reference'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:30:fieldvaluelist:0:inputText"]',
  'data_source'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:31:fieldvaluelist:0:description"]',
  'origin_hist_sources'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:32:fieldvaluelist:0:description"]',
  'character_of_sources'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:33:fieldvaluelist:0:description"]',
  'doc_to_sources'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:34:fieldvaluelist:0:description"]'
)

ds_template_xpaths <- c(
  #'host_dataverse'='',
  'title'='//*[@id="templateForm:j_idt620:0:j_idt623:0:fieldvaluelist:0:inputText"]',
  'author_name'='//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:0:inputText"]',
  'author_affiliation'='//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:1:inputText"]',
  #'author_id_type'='',
  'author_id'='//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:3:inputText"]',
  'contact_name'='//*[@id="templateForm:j_idt620:0:j_idt623:6:j_idt677:0:j_idt679:0:inputText"]',
  'contact_affiliation'='//*[@id="templateForm:j_idt620:0:j_idt623:6:j_idt677:0:j_idt679:1:inputText"]',
  'contact_email'='//*[@id="templateForm:j_idt620:0:j_idt623:6:j_idt677:0:j_idt679:2:inputText"]',
  'description'='//*[@id="templateForm:j_idt620:0:j_idt623:7:j_idt677:0:j_idt679:0:description"]',
  'date'='//*[@id="templateForm:j_idt620:0:j_idt623:7:j_idt677:0:j_idt679:1:inputText"]',
  #'subject'='',
  'keyword_term'='//*[@id="templateForm:j_idt620:0:j_idt623:9:j_idt677:0:j_idt679:0:inputText"]',
  'keyword_cv_name'='//*[@id="templateForm:j_idt620:0:j_idt623:9:j_idt677:0:j_idt679:1:inputText"]',
  'keyword_cv_url'='//*[@id="templateForm:j_idt620:0:j_idt623:9:j_idt677:0:j_idt679:2:inputText"]',
  'related_pub_citation'='//*[@id="templateForm:j_idt620:0:j_idt623:11:j_idt677:0:j_idt679:0:description"]',
  #'related_pub_id_type'='',
  'related_pub_id'='//*[@id="templateForm:j_idt620:0:j_idt623:11:j_idt677:0:j_idt679:2:inputText"]',
  'related_pub_url'='//*[@id="templateForm:j_idt620:0:j_idt623:11:j_idt677:0:j_idt679:3:inputText"]',
  'notes'='//*[@id="templateForm:j_idt620:0:j_idt623:12:fieldvaluelist:0:description"]',
  'depositor'='//*[@id="templateForm:j_idt620:0:j_idt623:21:fieldvaluelist:0:inputText"]',
  'deposit_date'='//*[@id="templateForm:j_idt620:0:j_idt623:22:fieldvaluelist:0:inputText"]',
  
  'subtitle'='//*[@id="templateForm:j_idt620:0:j_idt623:1:fieldvaluelist:0:inputText"]',
  'alternative_title'='//*[@id="templateForm:j_idt620:0:j_idt623:2:fieldvaluelist:0:inputText"]',
  'alternative_url'='//*[@id="templateForm:j_idt620:0:j_idt623:3:fieldvaluelist:0:inputText"]',
  'other_id_agency'='//*[@id="templateForm:j_idt620:0:j_idt623:4:j_idt677:0:j_idt679:0:inputText"]',
  'other_id_id'='//*[@id="templateForm:j_idt620:0:j_idt623:4:j_idt677:0:j_idt679:1:inputText"]',
  'topic_class_term'='//*[@id="templateForm:j_idt620:0:j_idt623:10:j_idt677:0:j_idt679:0:inputText"]',
  'topic_class_cv_name'='//*[@id="templateForm:j_idt620:0:j_idt623:10:j_idt677:0:j_idt679:1:inputText"]',
  'topic_class_cv_url'='//*[@id="templateForm:j_idt620:0:j_idt623:10:j_idt677:0:j_idt679:2:inputText"]',
  #'language'='',
  'producer_name'='//*[@id="templateForm:j_idt620:0:j_idt623:14:j_idt677:0:j_idt679:0:inputText"]',
  'producer_affiliation'='//*[@id="templateForm:j_idt620:0:j_idt623:14:j_idt677:0:j_idt679:1:inputText"]',
  'producer_abbrev_name'='//*[@id="templateForm:j_idt620:0:j_idt623:14:j_idt677:0:j_idt679:2:inputText"]',
  'producer_url'='//*[@id="templateForm:j_idt620:0:j_idt623:14:j_idt677:0:j_idt679:3:inputText"]',
  'producer_logo_url'='//*[@id="templateForm:j_idt620:0:j_idt623:14:j_idt677:0:j_idt679:4:inputText"]',
  'producer_date'='//*[@id="templateForm:j_idt620:0:j_idt623:15:fieldvaluelist:0:inputText"]',
  'producer_location'='//*[@id="templateForm:j_idt620:0:j_idt623:16:fieldvaluelist:0:inputText"]',
  #'contributor_type'='',
  'contributor_name'='//*[@id="templateForm:j_idt620:0:j_idt623:17:j_idt677:0:j_idt679:1:inputText"]',
  'funding_info_agency'='//*[@id="templateForm:j_idt620:0:j_idt623:18:j_idt677:0:j_idt679:0:inputText"]',
  'funding_info_id'='//*[@id="templateForm:j_idt620:0:j_idt623:18:j_idt677:0:j_idt679:1:inputText"]',
  'distributor_name'='//*[@id="templateForm:j_idt620:0:j_idt623:19:j_idt677:0:j_idt679:0:inputText"]',
  'distributor_affiliation'='//*[@id="templateForm:j_idt620:0:j_idt623:19:j_idt677:0:j_idt679:1:inputText"]',
  'distributor_abbrev_name'='//*[@id="templateForm:j_idt620:0:j_idt623:19:j_idt677:0:j_idt679:2:inputText"]',
  'distributor_url'='//*[@id="templateForm:j_idt620:0:j_idt623:19:j_idt677:0:j_idt679:3:inputText"]',
  'distributor_logo_url'='//*[@id="templateForm:j_idt620:0:j_idt623:19:j_idt677:0:j_idt679:4:inputText"]',
  'distribution_date'='//*[@id="templateForm:j_idt620:0:j_idt623:20:fieldvaluelist:0:inputText"]',
  'time_period_start'='//*[@id="templateForm:j_idt620:0:j_idt623:23:j_idt677:0:j_idt679:0:inputText"]',
  'time_period_end'='//*[@id="templateForm:j_idt620:0:j_idt623:23:j_idt677:0:j_idt679:1:inputText"]',
  'date_of_collection_start'='//*[@id="templateForm:j_idt620:0:j_idt623:24:j_idt677:0:j_idt679:0:inputText"]',
  'date_of_collection_end'='//*[@id="templateForm:j_idt620:0:j_idt623:24:j_idt677:0:j_idt679:1:inputText"]',
  'data_type'='//*[@id="templateForm:j_idt620:0:j_idt623:25:fieldvaluelist:0:inputText"]',
  'series_name'='//*[@id="templateForm:j_idt620:0:j_idt623:26:j_idt677:0:j_idt679:0:inputText"]',
  'series_info'='//*[@id="templateForm:j_idt620:0:j_idt623:26:j_idt677:0:j_idt679:1:description"]',
  'software_name'='//*[@id="templateForm:j_idt620:0:j_idt623:27:j_idt677:0:j_idt679:0:inputText"]',
  'software_version'='//*[@id="templateForm:j_idt620:0:j_idt623:27:j_idt677:0:j_idt679:1:inputText"]',
  'related_material'='//*[@id="templateForm:j_idt620:0:j_idt623:28:fieldvaluelist:0:description"]',
  'related_dataset'='//*[@id="templateForm:j_idt620:0:j_idt623:29:fieldvaluelist:0:description"]',
  'other_reference'='//*[@id="templateForm:j_idt620:0:j_idt623:30:fieldvaluelist:0:inputText"]',
  'data_source'='//*[@id="templateForm:j_idt620:0:j_idt623:31:fieldvaluelist:0:description"]',
  'origin_hist_sources'='//*[@id="templateForm:j_idt620:0:j_idt623:32:fieldvaluelist:0:description"]',
  'character_of_sources'='//*[@id="templateForm:j_idt620:0:j_idt623:33:fieldvaluelist:0:description"]',
  'doc_to_sources'='//*[@id="templateForm:j_idt620:0:j_idt623:34:fieldvaluelist:0:description"]'
)

# We have different functions for create / edit as the xpath changes between the two, and there is no other way to get the fields
set_dataset_metadata_create <- function(add_string='') {
  # We clear all the elements for when this code is called during edit and there are already contents
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:0:fieldvaluelist:0:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:0:fieldvaluelist:0:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['title'], sep='')))
  
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:0:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:0:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['author_name'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:1:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:1:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['author_affiliation'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:2:cvv_label"]')$clickElement() #click author identifier type dropdown
  Sys.sleep(.1)
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:2:cvv_2"]')$clickElement() #click "ISNI" inside dropdown
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:3:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:3:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['author_id'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:6:j_idt630:0:j_idt632:0:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:6:j_idt630:0:j_idt632:0:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['contact_name'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:6:j_idt630:0:j_idt632:1:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:6:j_idt630:0:j_idt632:1:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['contact_affiliation'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:6:j_idt630:0:j_idt632:2:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:6:j_idt630:0:j_idt632:2:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['contact_email'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:7:j_idt630:0:j_idt632:0:description"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:7:j_idt630:0:j_idt632:0:description"]')$sendKeysToElement(list(paste(add_string, ds_props['description'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:7:j_idt630:0:j_idt632:1:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:7:j_idt630:0:j_idt632:1:inputText"]')$sendKeysToElement(list(ds_props['date'], sep=''))
  #TODO: add a clear for the select thing?
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:8:unique2"]')$clickElement() #click subject dropdown
  Sys.sleep(.1)
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:8:unique2_panel"]/div[2]/ul/li[14]/div')$clickElement() #click "other" inside dropdown
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:9:j_idt630:0:j_idt632:0:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:9:j_idt630:0:j_idt632:0:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['keyword_term'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:9:j_idt630:0:j_idt632:1:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:9:j_idt630:0:j_idt632:1:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['keyword_cv_name'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:9:j_idt630:0:j_idt632:2:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:9:j_idt630:0:j_idt632:2:inputText"]')$sendKeysToElement(list(paste(ds_props['keyword_cv_url'], add_string, sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:0:description"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:0:description"]')$sendKeysToElement(list(paste(add_string, ds_props['related_pub_citation'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:1:cvv_label"]')$clickElement() #click related pub id type dropdown
  Sys.sleep(.1)
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:1:cvv_4"]')$clickElement() #click "doi" inside dropdown
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:2:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:2:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['related_pub_id'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:3:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:3:inputText"]')$sendKeysToElement(list(paste(ds_props['related_pub_url'], add_string, sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:12:fieldvaluelist:0:description"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:12:fieldvaluelist:0:description"]')$sendKeysToElement(list(paste(add_string, ds_props['notes'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:21:fieldvaluelist:0:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:21:fieldvaluelist:0:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['depositor'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:22:fieldvaluelist:0:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:22:fieldvaluelist:0:inputText"]')$sendKeysToElement(list(ds_props['deposit_date'], sep=''))
  
  #TODO: Upload files here?
  sesh$findElement(value='//*[@id="datasetForm:saveBottom"]')$clickElement() #create dataset
}

#also supports dataset template
set_dataset_metadata_edit <- function(add_string='', xpath_dict=NULL) {
  
  #NOTE: For some reason moving some of these dropdown tests to the bottom of this files causes it to fail. Is it because they are too far off the page or... I have no idea what?
  if (isTRUE(all.equal(xpath_dict,ds_edit_xpaths))) {
    
    sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:2:cvv"]')$clickElement() #click author identifier type dropdown
    Sys.sleep(.3)
    sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:2:cvv_4"]')$clickElement() #click "VIAF" inside dropdown
    sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:8:unique2"]/ul/li/span[1]')$clickElement() #Delete existing field "Other"
    sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:8:unique2"]')$clickElement() #click subject dropdown
    Sys.sleep(.3)
    sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:8:unique2_panel"]/div[2]/ul/li[10]/div')$clickElement() #click "mathematical science" inside dropdown
    #sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:1:cvv"]/div[3]')$clickElement() #click related pub id type dropdown
    sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:1:cvv"]')$clickElement() #click related pub id type dropdown
    Sys.sleep(.3)
    sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:1:cvv_4"]')$clickElement() #click "DOI" inside dropdown
    sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:13:unique2"]/div[3]')$clickElement() #click language dropdown
    Sys.sleep(.3)
    sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:13:unique2_panel"]/div[2]/ul/li[2]')$clickElement() #click "Afar" inside dropdown
    sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:17:j_idt1679:0:j_idt1681:0:cvv"]')$clickElement() #click contributor type dropdown
    Sys.sleep(.3)
    sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:17:j_idt1679:0:j_idt1681:0:cvv_3"]')$clickElement() #click "Data Manager" inside dropdown
    
    # sesh$findElement(value='//*[@id="datasetForm:saveBottom"]')$clickElement() #create dataset
  } else if (isTRUE(all.equal(xpath_dict,ds_template_xpaths))) {
    
    sesh$findElement(value='//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:2:cvv"]')$clickElement() #click author identifier type dropdown
    Sys.sleep(.5)
    sesh$findElement(value='//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:2:cvv_5"]')$clickElement() #click "GND" inside dropdown
    sesh$findElement(value='//*[@id="templateForm:j_idt620:0:j_idt623:8:editPrimitiveValueFragment"]/div[3]/div/div/div')$clickElement() #click subject dropdown
    Sys.sleep(.5)
    sesh$findElement(value='//*[@id="templateForm:j_idt620:0:j_idt623:8:unique2_panel"]/div[2]/ul/li[6]')$clickElement() #click "Computer and Information Science" inside dropdown
    sesh$findElement(value='//*[@id="templateForm:j_idt620:0:j_idt623:11:j_idt677:0:j_idt679:1:cvv"]')$clickElement() #click related pub id type dropdown
    Sys.sleep(.5)
    sesh$findElement(value='//*[@id="templateForm:j_idt620:0:j_idt623:11:j_idt677:0:j_idt679:1:cvv_5"]')$clickElement() #click "ean13" inside dropdown
    sesh$findElement(value='//*[@id="templateForm:j_idt620:0:j_idt623:13:unique2"]')$clickElement() #click language dropdown
    Sys.sleep(.5)
    sesh$findElement(value='//*[@id="templateForm:j_idt620:0:j_idt623:13:unique2_panel"]/div[2]/ul/li[72]')$clickElement() #click "Inuktitut" inside dropdown
    
    sesh$findElement(value='//*[@id="templateForm:j_idt620:0:j_idt623:17:j_idt677:0:j_idt679:0:cvv"]')$clickElement() #click contributor type dropdown
    Sys.sleep(.5)
    sesh$findElement(value='//*[@id="templateForm:j_idt620:0:j_idt623:17:j_idt677:0:j_idt679:0:cvv_11"]')$clickElement() #click "Researcher" inside dropdown
  }
  sesh$findElement(value=xpath_dict['title'])$clearElement()
  sesh$findElement(value=xpath_dict['title'])$sendKeysToElement(list(paste(add_string, ds_props['title'], sep='')))
  sesh$findElement(value=xpath_dict['author_name'])$clearElement()
  sesh$findElement(value=xpath_dict['author_name'])$sendKeysToElement(list(paste(add_string, ds_props['author_name'], sep='')))
  sesh$findElement(value=xpath_dict['author_affiliation'])$clearElement()
  sesh$findElement(value=xpath_dict['author_affiliation'])$sendKeysToElement(list(paste(add_string, ds_props['author_affiliation'], sep='')))
  sesh$findElement(value=xpath_dict['author_id'])$clearElement()
  sesh$findElement(value=xpath_dict['author_id'])$sendKeysToElement(list(paste(add_string, ds_props['author_id'], sep='')))
  sesh$findElement(value=xpath_dict['contact_name'])$clearElement()
  sesh$findElement(value=xpath_dict['contact_name'])$sendKeysToElement(list(paste(add_string, ds_props['contact_name'], sep='')))
  sesh$findElement(value=xpath_dict['contact_affiliation'])$clearElement()
  sesh$findElement(value=xpath_dict['contact_affiliation'])$sendKeysToElement(list(paste(add_string, ds_props['contact_affiliation'], sep='')))
  sesh$findElement(value=xpath_dict['contact_email'])$clearElement()
  sesh$findElement(value=xpath_dict['contact_email'])$sendKeysToElement(list(paste(add_string, ds_props['contact_email'], sep='')))
  sesh$findElement(value=xpath_dict['description'])$clearElement()
  sesh$findElement(value=xpath_dict['description'])$sendKeysToElement(list(paste(add_string, ds_props['description'], sep='')))
  sesh$findElement(value=xpath_dict['date'])$clearElement()
  sesh$findElement(value=xpath_dict['date'])$sendKeysToElement(list(ds_props['date'], sep=''))
  sesh$findElement(value=xpath_dict['keyword_term'])$clearElement()
  sesh$findElement(value=xpath_dict['keyword_term'])$sendKeysToElement(list(paste(add_string, ds_props['keyword_term'], sep='')))
  sesh$findElement(value=xpath_dict['keyword_cv_name'])$clearElement()
  sesh$findElement(value=xpath_dict['keyword_cv_name'])$sendKeysToElement(list(paste(add_string, ds_props['keyword_cv_name'], sep='')))
  sesh$findElement(value=xpath_dict['keyword_cv_url'])$clearElement()
  sesh$findElement(value=xpath_dict['keyword_cv_url'])$sendKeysToElement(list(paste(ds_props['keyword_cv_url'], add_string, sep='')))
  sesh$findElement(value=xpath_dict['related_pub_citation'])$clearElement()
  sesh$findElement(value=xpath_dict['related_pub_citation'])$sendKeysToElement(list(paste(add_string, ds_props['related_pub_citation'], sep='')))
  sesh$findElement(value=xpath_dict['related_pub_id'])$clearElement()
  sesh$findElement(value=xpath_dict['related_pub_id'])$sendKeysToElement(list(paste(add_string, ds_props['related_pub_id'], sep='')))
  sesh$findElement(value=xpath_dict['related_pub_url'])$clearElement()
  sesh$findElement(value=xpath_dict['related_pub_url'])$sendKeysToElement(list(paste(ds_props['related_pub_url'], add_string, sep='')))
  sesh$findElement(value=xpath_dict['notes'])$clearElement()
  sesh$findElement(value=xpath_dict['notes'])$sendKeysToElement(list(paste(add_string, ds_props['notes'], sep='')))
  sesh$findElement(value=xpath_dict['depositor'])$clearElement()
  sesh$findElement(value=xpath_dict['depositor'])$sendKeysToElement(list(paste(add_string, ds_props['depositor'], sep='')))
  sesh$findElement(value=xpath_dict['deposit_date'])$clearElement()
  sesh$findElement(value=xpath_dict['deposit_date'])$sendKeysToElement(list(ds_props['deposit_date'], sep=''))
  
  sesh$findElement(value=xpath_dict['subtitle'])$clearElement()
  sesh$findElement(value=xpath_dict['subtitle'])$sendKeysToElement(list(paste(add_string, ds_props['subtitle'], sep='')))
  sesh$findElement(value=xpath_dict['alternative_title'])$clearElement()
  sesh$findElement(value=xpath_dict['alternative_title'])$sendKeysToElement(list(paste(add_string, ds_props['alternative_title'], sep='')))
  sesh$findElement(value=xpath_dict['alternative_url'])$clearElement()
  sesh$findElement(value=xpath_dict['alternative_url'])$sendKeysToElement(list(paste(ds_props['alternative_url'], add_string, sep='')))
  sesh$findElement(value=xpath_dict['other_id_agency'])$clearElement()
  sesh$findElement(value=xpath_dict['other_id_agency'])$sendKeysToElement(list(paste(add_string, ds_props['other_id_agency'], sep='')))
  sesh$findElement(value=xpath_dict['other_id_id'])$clearElement()
  sesh$findElement(value=xpath_dict['other_id_id'])$sendKeysToElement(list(paste(add_string, ds_props['other_id_id'], sep='')))
  sesh$findElement(value=xpath_dict['topic_class_term'])$clearElement()
  sesh$findElement(value=xpath_dict['topic_class_term'])$sendKeysToElement(list(paste(add_string, ds_props['topic_class_term'], sep='')))
  sesh$findElement(value=xpath_dict['topic_class_cv_name'])$clearElement()
  sesh$findElement(value=xpath_dict['topic_class_cv_name'])$sendKeysToElement(list(paste(add_string, ds_props['topic_class_cv_name'], sep='')))
  sesh$findElement(value=xpath_dict['topic_class_cv_url'])$clearElement()
  sesh$findElement(value=xpath_dict['topic_class_cv_url'])$sendKeysToElement(list(paste(ds_props['topic_class_cv_url'], add_string, sep='')))
  sesh$findElement(value=xpath_dict['producer_name'])$clearElement()
  sesh$findElement(value=xpath_dict['producer_name'])$sendKeysToElement(list(paste(add_string, ds_props['producer_name'], sep='')))
  sesh$findElement(value=xpath_dict['producer_affiliation'])$clearElement()
  sesh$findElement(value=xpath_dict['producer_affiliation'])$sendKeysToElement(list(paste(add_string, ds_props['producer_affiliation'], sep='')))
  sesh$findElement(value=xpath_dict['producer_abbrev_name'])$clearElement()
  sesh$findElement(value=xpath_dict['producer_abbrev_name'])$sendKeysToElement(list(paste(add_string, ds_props['producer_abbrev_name'], sep='')))
  sesh$findElement(value=xpath_dict['producer_url'])$clearElement()
  sesh$findElement(value=xpath_dict['producer_url'])$sendKeysToElement(list(paste(ds_props['producer_url'], add_string, sep='')))
  sesh$findElement(value=xpath_dict['producer_logo_url'])$clearElement()
  sesh$findElement(value=xpath_dict['producer_logo_url'])$sendKeysToElement(list(paste(ds_props['producer_logo_url'], add_string, sep='')))
  sesh$findElement(value=xpath_dict['producer_date'])$clearElement()
  sesh$findElement(value=xpath_dict['producer_date'])$sendKeysToElement(list(toString(ds_props['producer_date'])))
  sesh$findElement(value=xpath_dict['producer_location'])$clearElement()
  sesh$findElement(value=xpath_dict['producer_location'])$sendKeysToElement(list(paste(add_string, ds_props['producer_location'], sep='')))
  sesh$findElement(value=xpath_dict['contributor_name'])$clearElement()
  sesh$findElement(value=xpath_dict['contributor_name'])$sendKeysToElement(list(paste(add_string, ds_props['contributor_name'], sep='')))
  sesh$findElement(value=xpath_dict['funding_info_agency'])$clearElement()
  sesh$findElement(value=xpath_dict['funding_info_agency'])$sendKeysToElement(list(paste(add_string, ds_props['funding_info_agency'], sep='')))
  sesh$findElement(value=xpath_dict['funding_info_id'])$clearElement()
  sesh$findElement(value=xpath_dict['funding_info_id'])$sendKeysToElement(list(paste(add_string, ds_props['funding_info_id'], sep='')))
  sesh$findElement(value=xpath_dict['distributor_name'])$clearElement()
  sesh$findElement(value=xpath_dict['distributor_name'])$sendKeysToElement(list(paste(add_string, ds_props['distributor_name'], sep='')))
  sesh$findElement(value=xpath_dict['distributor_affiliation'])$clearElement()
  sesh$findElement(value=xpath_dict['distributor_affiliation'])$sendKeysToElement(list(paste(add_string, ds_props['distributor_affiliation'], sep='')))
  sesh$findElement(value=xpath_dict['distributor_abbrev_name'])$clearElement()
  sesh$findElement(value=xpath_dict['distributor_abbrev_name'])$sendKeysToElement(list(paste(add_string, ds_props['distributor_abbrev_name'], sep='')))
  sesh$findElement(value=xpath_dict['distributor_url'])$clearElement()
  sesh$findElement(value=xpath_dict['distributor_url'])$sendKeysToElement(list(paste(ds_props['distributor_url'], add_string, sep='')))
  sesh$findElement(value=xpath_dict['distributor_logo_url'])$clearElement()
  sesh$findElement(value=xpath_dict['distributor_logo_url'])$sendKeysToElement(list(paste(ds_props['distributor_logo_url'], add_string, sep='')))
  sesh$findElement(value=xpath_dict['distribution_date'])$clearElement()
  sesh$findElement(value=xpath_dict['distribution_date'])$sendKeysToElement(list(toString(ds_props['distribution_date'])))
  sesh$findElement(value=xpath_dict['time_period_start'])$clearElement()
  sesh$findElement(value=xpath_dict['time_period_start'])$sendKeysToElement(list(toString(ds_props['time_period_start'])))
  sesh$findElement(value=xpath_dict['time_period_end'])$clearElement()
  sesh$findElement(value=xpath_dict['time_period_end'])$sendKeysToElement(list(toString(ds_props['time_period_end'])))
  sesh$findElement(value=xpath_dict['date_of_collection_start'])$clearElement()
  sesh$findElement(value=xpath_dict['date_of_collection_start'])$sendKeysToElement(list(toString(ds_props['date_of_collection_start'])))
  sesh$findElement(value=xpath_dict['date_of_collection_end'])$clearElement()
  sesh$findElement(value=xpath_dict['date_of_collection_end'])$sendKeysToElement(list(toString(ds_props['date_of_collection_end'])))
  sesh$findElement(value=xpath_dict['data_type'])$clearElement()
  sesh$findElement(value=xpath_dict['data_type'])$sendKeysToElement(list(paste(add_string, ds_props['data_type'], sep='')))
  sesh$findElement(value=xpath_dict['series_name'])$clearElement()
  sesh$findElement(value=xpath_dict['series_name'])$sendKeysToElement(list(paste(add_string, ds_props['series_name'], sep='')))
  sesh$findElement(value=xpath_dict['series_info'])$clearElement()
  sesh$findElement(value=xpath_dict['series_info'])$sendKeysToElement(list(paste(add_string, ds_props['series_info'], sep='')))
  sesh$findElement(value=xpath_dict['software_name'])$clearElement()
  sesh$findElement(value=xpath_dict['software_name'])$sendKeysToElement(list(paste(add_string, ds_props['software_name'], sep='')))
  sesh$findElement(value=xpath_dict['software_version'])$clearElement()
  sesh$findElement(value=xpath_dict['software_version'])$sendKeysToElement(list(paste(add_string, ds_props['software_version'], sep='')))
  sesh$findElement(value=xpath_dict['related_material'])$clearElement()
  sesh$findElement(value=xpath_dict['related_material'])$sendKeysToElement(list(paste(add_string, ds_props['related_material'], sep='')))
  sesh$findElement(value=xpath_dict['related_dataset'])$clearElement()
  sesh$findElement(value=xpath_dict['related_dataset'])$sendKeysToElement(list(paste(add_string, ds_props['related_dataset'], sep='')))
  sesh$findElement(value=xpath_dict['other_reference'])$clearElement()
  sesh$findElement(value=xpath_dict['other_reference'])$sendKeysToElement(list(paste(add_string, ds_props['other_reference'], sep='')))
  sesh$findElement(value=xpath_dict['data_source'])$clearElement()
  sesh$findElement(value=xpath_dict['data_source'])$sendKeysToElement(list(paste(add_string, ds_props['data_source'], sep='')))
  sesh$findElement(value=xpath_dict['origin_hist_sources'])$clearElement()
  sesh$findElement(value=xpath_dict['origin_hist_sources'])$sendKeysToElement(list(paste(add_string, ds_props['origin_hist_sources'], sep='')))  
  sesh$findElement(value=xpath_dict['character_of_sources'])$clearElement()
  sesh$findElement(value=xpath_dict['character_of_sources'])$sendKeysToElement(list(paste(add_string, ds_props['character_of_sources'], sep='')))  
  sesh$findElement(value=xpath_dict['doc_to_sources'])$clearElement()
  sesh$findElement(value=xpath_dict['doc_to_sources'])$sendKeysToElement(list(paste(add_string, ds_props['doc_to_sources'], sep='')))  

}

#Also supports dataset template
test_dataset_metadata <- function(add_string='', is_update=FALSE, xpath_dict=NULL) {
  # if (is_update) {
  #   Sys.sleep(999999999)
  # }
  # add_string='edit'
  # is_update=TRUE
  
  #For some reason, dates are false when tested identical. I'm not sure if some character is being replaced on the backend or what. But this is fine
  #We don't currently test some dropdowns results because it is extremely convoluted to test the values of jquery dropdowns.
  expect_identical(toString(sesh$findElement(value=xpath_dict['title'])$getElementAttribute("value")), paste(add_string, ds_props['title'], sep=''))
  expect_identical(toString(sesh$findElement(value=xpath_dict['author_name'])$getElementAttribute("value")), paste(add_string, ds_props['author_name'], sep=''))
  expect_identical(toString(sesh$findElement(value=xpath_dict['author_affiliation'])$getElementAttribute("value")), paste(add_string, ds_props['author_affiliation'], sep=''))
  #expect_identical(toString(sesh$findElement(value=xpath_dict['author_id_type'])$getElementAttribute("value")), paste(add_string, ds_props['author_id_type'], sep=''))
  expect_identical(toString(sesh$findElement(value=xpath_dict['author_id'])$getElementAttribute("value")), paste(add_string, ds_props['author_id'], sep=''))
  expect_identical(toString(sesh$findElement(value=xpath_dict['contact_name'])$getElementAttribute("value")), paste(add_string, ds_props['contact_name'], sep=''))
  expect_identical(toString(sesh$findElement(value=xpath_dict['contact_affiliation'])$getElementAttribute("value")), paste(add_string, ds_props['contact_affiliation'], sep=''))
  expect_identical(toString(sesh$findElement(value=xpath_dict['contact_email'])$getElementAttribute("value")), paste(add_string, ds_props['contact_email'], sep=''))
  expect_identical(toString(sesh$findElement(value=xpath_dict['description'])$getElementAttribute("value")), paste(add_string, ds_props['description'], sep=''))
  expect_identical(toString(sesh$findElement(value=xpath_dict['date'])$getElementAttribute("value")), toString(ds_props['date']))
  #expect_identical(toString(sesh$findElement(value=xpath_dict['subject'])$getElementAttribute("value")), paste(add_string, ds_props['subject'], sep=''))
  expect_identical(toString(sesh$findElement(value=xpath_dict['keyword_term'])$getElementAttribute("value")), paste(add_string, ds_props['keyword_term'], sep=''))
  expect_identical(toString(sesh$findElement(value=xpath_dict['keyword_cv_name'])$getElementAttribute("value")), paste(add_string, ds_props['keyword_cv_name'], sep=''))
  expect_identical(toString(sesh$findElement(value=xpath_dict['keyword_cv_url'])$getElementAttribute("value")), paste(ds_props['keyword_cv_url'], add_string, sep=''))
  expect_identical(toString(sesh$findElement(value=xpath_dict['related_pub_citation'])$getElementAttribute("value")), paste(add_string, ds_props['related_pub_citation'], sep=''))
  #expect_identical(toString(sesh$findElement(value=xpath_dict['related_pub_id_type'])$getElementAttribute("value")), paste(add_string, ds_props['related_pub_id_type'], sep=''))
  #TODO: I think this doesn't work because it needs the above set... but weirdly I thought it worked before???? Well it doesn't work now
  expect_identical(toString(sesh$findElement(value=xpath_dict['related_pub_id'])$getElementAttribute("value")), paste(add_string, ds_props['related_pub_id'], sep=''))
  expect_identical(toString(sesh$findElement(value=xpath_dict['related_pub_url'])$getElementAttribute("value")), paste(ds_props['related_pub_url'], add_string, sep=''))
  expect_identical(toString(sesh$findElement(value=xpath_dict['notes'])$getElementAttribute("value")), paste(add_string, ds_props['notes'], sep=''))
  expect_identical(toString(sesh$findElement(value=xpath_dict['depositor'])$getElementAttribute("value")), paste(add_string, ds_props['depositor'], sep=''))
  expect_identical(toString(sesh$findElement(value=xpath_dict['deposit_date'])$getElementAttribute("value")), toString(ds_props['deposit_date']))
  
  if (is_update) {
    expect_identical(toString(sesh$findElement(value=xpath_dict['subtitle'])$getElementAttribute("value")), paste(add_string, ds_props['subtitle'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['alternative_title'])$getElementAttribute("value")), paste(add_string, ds_props['alternative_title'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['alternative_url'])$getElementAttribute("value")), paste(ds_props['alternative_url'], add_string, sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['other_id_agency'])$getElementAttribute("value")), paste(add_string, ds_props['other_id_agency'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['other_id_id'])$getElementAttribute("value")), paste(add_string, ds_props['other_id_id'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['topic_class_term'])$getElementAttribute("value")), paste(add_string, ds_props['topic_class_term'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['topic_class_cv_name'])$getElementAttribute("value")), paste(add_string, ds_props['topic_class_cv_name'], sep=''))
    # expect_identical(toString(sesh$findElement(value=xpath_dict['language'])$getElementAttribute("value")), paste(add_string, ds_props['language'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['producer_name'])$getElementAttribute("value")), paste(add_string, ds_props['producer_name'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['producer_affiliation'])$getElementAttribute("value")), paste(add_string, ds_props['producer_affiliation'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['producer_abbrev_name'])$getElementAttribute("value")), paste(add_string, ds_props['producer_abbrev_name'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['producer_url'])$getElementAttribute("value")), paste(ds_props['producer_url'], add_string,  sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['producer_logo_url'])$getElementAttribute("value")), paste(ds_props['producer_logo_url'], add_string, sep=''))
    expect_equivalent(toString(sesh$findElement(value=xpath_dict['producer_date'])$getElementAttribute("value")), ds_props['producer_date'])
    expect_identical(toString(sesh$findElement(value=xpath_dict['producer_location'])$getElementAttribute("value")), paste(add_string, ds_props['producer_location'], sep=''))
    # expect_identical(toString(sesh$findElement(value=xpath_dict['contributor_type'])$getElementAttribute("value")), paste(add_string, ds_props['contributor_type'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['contributor_name'])$getElementAttribute("value")), paste(add_string, ds_props['contributor_name'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['funding_info_agency'])$getElementAttribute("value")), paste(add_string, ds_props['funding_info_agency'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['funding_info_id'])$getElementAttribute("value")), paste(add_string, ds_props['funding_info_id'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['distributor_name'])$getElementAttribute("value")), paste(add_string, ds_props['distributor_name'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['distributor_affiliation'])$getElementAttribute("value")), paste(add_string, ds_props['distributor_affiliation'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['distributor_abbrev_name'])$getElementAttribute("value")), paste(add_string, ds_props['distributor_abbrev_name'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['distributor_url'])$getElementAttribute("value")), paste(ds_props['distributor_url'], add_string, sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['distributor_logo_url'])$getElementAttribute("value")), paste(ds_props['distributor_logo_url'], add_string, sep=''))
    expect_equivalent(toString(sesh$findElement(value=xpath_dict['distribution_date'])$getElementAttribute("value")), ds_props['distribution_date'])
    expect_equivalent(toString(sesh$findElement(value=xpath_dict['time_period_start'])$getElementAttribute("value")), ds_props['time_period_start'])
    expect_equivalent(toString(sesh$findElement(value=xpath_dict['time_period_end'])$getElementAttribute("value")), ds_props['time_period_end'])
    expect_equivalent(toString(sesh$findElement(value=xpath_dict['date_of_collection_start'])$getElementAttribute("value")), ds_props['date_of_collection_start'])
    expect_equivalent(toString(sesh$findElement(value=xpath_dict['date_of_collection_end'])$getElementAttribute("value")), ds_props['date_of_collection_end'])
    expect_identical(toString(sesh$findElement(value=xpath_dict['data_type'])$getElementAttribute("value")), paste(add_string, ds_props['data_type'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['series_name'])$getElementAttribute("value")), paste(add_string, ds_props['series_name'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['series_info'])$getElementAttribute("value")), paste(add_string, ds_props['series_info'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['software_name'])$getElementAttribute("value")), paste(add_string, ds_props['software_name'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['software_version'])$getElementAttribute("value")), paste(add_string, ds_props['software_version'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['related_material'])$getElementAttribute("value")), paste(add_string, ds_props['related_material'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['related_dataset'])$getElementAttribute("value")), paste(add_string, ds_props['related_dataset'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['other_reference'])$getElementAttribute("value")), paste(add_string, ds_props['other_reference'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['data_source'])$getElementAttribute("value")), paste(add_string, ds_props['data_source'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['origin_hist_sources'])$getElementAttribute("value")), paste(add_string, ds_props['origin_hist_sources'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['character_of_sources'])$getElementAttribute("value")), paste(add_string, ds_props['character_of_sources'], sep=''))
    expect_identical(toString(sesh$findElement(value=xpath_dict['doc_to_sources'])$getElementAttribute("value")), paste(add_string, ds_props['doc_to_sources'], sep=''))
  }
}
 #Delete
delete_template_via_ui <- function(id, dv_id) {
  sesh$navigate(paste(dv_server_url,'/manage-templates.xhtml?dataverseId=', root_dv_id, sep=''))
  template_trs = sesh$findElements(value='//*[@id="manageTemplatesForm:allTemplates_data"]/tr')

  for (tr in template_trs) {
    tr_id = toString(param_get(toString(tr$findChildElement(value='td[4]/div/div/ul/li[1]/a')$getElementAttribute("href")), c("id")))
    if (id == tr_id) {
      tr$findChildElement(value='td[4]/div/a[3]')$clickElement()
      Sys.sleep(.2)
      sesh$findElement(value='//*[@id="manageTemplatesForm:contDeleteTemplateBtn"]')$clickElement()
      return(TRUE)
    }
  }
  
  print(paste("Unable to delete dataset template with id:", id))
  return(FALSE)
  #TODO: Raise exception if we get here?
  
  # STEPS:
  # Iterate through tr inside //*[@id="manageTemplatesForm:allTemplates_data"]
  # Get the ID out of the edit data / metadata menu option
  # - //*[@id="manageTemplatesForm:allTemplates_data"]/tr[1]/td[4]/div/div/ul/li[1]/a
  # - <a href="/template.xhtml?id=10&amp;ownerId=1&amp;editMode=METADATA">Metadata</a>
  # If it matches the provided id, we click the delete button in that tr
}
