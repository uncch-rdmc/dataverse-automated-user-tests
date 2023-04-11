import time

class DatasetTestingMixin(object):
    dataset_name = "test_dataset"
    dataset_id = None
    template_id = None

    #################################
    ### Dataset Test Dictionaries ###
    #################################

    ds_props = {
        #'host_dataverse': '',
        'title': dataset_name,
        'author_name': 'author',
        'author_affiliation': 'affiliation',
        #'author_id_type': 'ORCID',
        'author_id': 'author_affil_id',
        'contact_name': 'contact',
        'contact_affiliation': 'contact_affil',
        'contact_email': 'test@example.com',
        'description': 'this is a test description',
        'date': '2022-11-11',
        'subject': 'Physics',
        'keyword_term': 'keyword',
        'keyword_cv_name': 'vocab_name',
        'keyword_cv_url': 'https://odum.unc.edu/',
        'related_pub_citation': 'this is a test citation',
        #'related_pub_id_type': 'lissn',
        'related_pub_id': 'pub_id',
        'related_pub_url': 'https://odum.unc.edu/',
        'notes': 'this is a test note',
        'depositor': 'a depositor',
        'deposit_date': '2020-01-01',
        
        'subtitle': 'subtitle',
        'alternative_title': 'alternative_title',
        'alternative_url': 'https://odum.unc.edu/',
        'other_id_agency': 'other_id_agency',
        'other_id_id': 'other_id_id',
        'topic_class_term': 'topic_class_term',
        'topic_class_cv_name': 'topic_class_cv_name',
        'topic_class_cv_url': 'https://odum.unc.edu/',
        'language': 'language',
        'producer_name': 'producer_name',
        'producer_affiliation': 'produder_affiliation',
        'producer_abbrev_name': 'produder_abbrev_name',
        'producer_url': 'https://odum.unc.edu/',
        'producer_logo_url': 'https://odum.unc.edu/',
        'producer_date': '2020-01-01',
        'producer_location': 'produder_location',
        'contributor_type': 'contributor_type',
        'contributor_name': 'contributor_name',
        'funding_info_agency': 'funding_info_agency',
        'funding_info_id': 'funding_info_id',
        'distributor_name': 'distributor_name',
        'distributor_affiliation': 'distributor_affiliation',
        'distributor_abbrev_name': 'distributor_abbrev_name',
        'distributor_url': 'https://odum.unc.edu/',
        'distributor_logo_url': 'https://odum.unc.edu/',
        'distribution_date': '2020-01-01',
        'time_period_start': '2020-01-01',
        'time_period_end': '2020-01-02',
        'date_of_collection_start': '2020-01-01',
        'date_of_collection_end': '2020-01-02',
        'data_type': 'data_type',
        'series_name': 'series_name',
        'series_info': 'series_info',
        'software_name': 'software_name',
        'software_version': 'software_version',
        'related_material': 'related_material',
        'related_dataset': 'related_dataset',
        'other_reference': 'other_reference',
        'data_source': 'data_source',
        'origin_hist_sources': 'origin_hist_sources',
        'character_of_sources': 'character_of_sources',
        'doc_to_sources': 'doc_to_sources'
    }

    # Used both for editing and seeing results of create/edit
    ds_edit_xpaths = {
        #'host_dataverse': '',
        'title': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:0:fieldvaluelist:0:inputText"]',
        'author_name': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:0:inputText"]',
        'author_affiliation': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:1:inputText"]',
        #'author_id_type': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:2:cvv_label"]',
        'author_id': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:3:inputText"]',
        'contact_name': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:6:j_idt1679:0:j_idt1681:0:inputText"]',
        'contact_affiliation': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:6:j_idt1679:0:j_idt1681:1:inputText"]',
        'contact_email': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:6:j_idt1679:0:j_idt1681:2:inputText"]',
        'description': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:7:j_idt1679:0:j_idt1681:0:description"]',
        'date': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:7:j_idt1679:0:j_idt1681:1:inputText"]',
        #'subject': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:8:unique2"]/ul/li/span[1]', #This probably won't work due to the weirdness of the dropdown. Definitely not for create
        'keyword_term': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:9:j_idt1679:0:j_idt1681:0:inputText"]',
        'keyword_cv_name': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:9:j_idt1679:0:j_idt1681:1:inputText"]',
        'keyword_cv_url': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:9:j_idt1679:0:j_idt1681:2:inputText"]',
        'related_pub_citation': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:0:description"]',
        #'related_pub_id_type': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:1:cvv_label"]', #Also might not work
        'related_pub_id': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:2:inputText"]',
        'related_pub_url': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:3:inputText"]',
        'notes': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:12:fieldvaluelist:0:description"]',
        'depositor': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:21:fieldvaluelist:0:inputText"]',
        'deposit_date': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:22:fieldvaluelist:0:inputText"]',
        
        'subtitle': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:1:fieldvaluelist:0:inputText"]',
        'alternative_title': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:2:fieldvaluelist:0:inputText"]',
        'alternative_url': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:3:fieldvaluelist:0:inputText"]',
        'other_id_agency': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:4:j_idt1679:0:j_idt1681:0:inputText"]',
        'other_id_id': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:4:j_idt1679:0:j_idt1681:1:inputText"]',
        'topic_class_term': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:10:j_idt1679:0:j_idt1681:0:inputText"]',
        'topic_class_cv_name': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:10:j_idt1679:0:j_idt1681:1:inputText"]',
        'topic_class_cv_url': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:10:j_idt1679:0:j_idt1681:2:inputText"]',
        #'language': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:13:unique2"]/ul/li/span[2]', #This probably doesn't work, like subject
        'producer_name': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:14:j_idt1679:0:j_idt1681:0:inputText"]',
        'producer_affiliation': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:14:j_idt1679:0:j_idt1681:1:inputText"]',
        'producer_abbrev_name': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:14:j_idt1679:0:j_idt1681:2:inputText"]',
        'producer_url': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:14:j_idt1679:0:j_idt1681:3:inputText"]',
        'producer_logo_url': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:14:j_idt1679:0:j_idt1681:4:inputText"]',
        'producer_date': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:15:fieldvaluelist:0:inputText"]',
        'producer_location': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:16:fieldvaluelist:0:inputText"]',
        #'contributor_type': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:17:j_idt1679:0:j_idt1681:0:cvv_label"]',
        'contributor_name': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:17:j_idt1679:0:j_idt1681:1:inputText"]',
        'funding_info_agency': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:18:j_idt1679:0:j_idt1681:0:inputText"]',
        'funding_info_id': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:18:j_idt1679:0:j_idt1681:1:inputText"]',
        'distributor_name': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:19:j_idt1679:0:j_idt1681:0:inputText"]',
        'distributor_affiliation': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:19:j_idt1679:0:j_idt1681:1:inputText"]',
        'distributor_abbrev_name': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:19:j_idt1679:0:j_idt1681:2:inputText"]',
        'distributor_url': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:19:j_idt1679:0:j_idt1681:3:inputText"]',
        'distributor_logo_url': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:19:j_idt1679:0:j_idt1681:4:inputText"]',
        'distribution_date': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:20:fieldvaluelist:0:inputText"]',
        'time_period_start': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:23:j_idt1679:0:j_idt1681:0:inputText"]',
        'time_period_end': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:23:j_idt1679:0:j_idt1681:1:inputText"]',
        'date_of_collection_start': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:24:j_idt1679:0:j_idt1681:0:inputText"]',
        'date_of_collection_end': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:24:j_idt1679:0:j_idt1681:1:inputText"]',
        'data_type': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:25:fieldvaluelist:0:inputText"]',
        'series_name': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:26:j_idt1679:0:j_idt1681:0:inputText"]',
        'series_info': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:26:j_idt1679:0:j_idt1681:1:description"]',
        'software_name': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:27:j_idt1679:0:j_idt1681:0:inputText"]',
        'software_version': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:27:j_idt1679:0:j_idt1681:1:inputText"]',
        'related_material': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:28:fieldvaluelist:0:description"]',
        'related_dataset': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:29:fieldvaluelist:0:description"]',
        'other_reference': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:30:fieldvaluelist:0:inputText"]',
        'data_source': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:31:fieldvaluelist:0:description"]',
        'origin_hist_sources': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:32:fieldvaluelist:0:description"]',
        'character_of_sources': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:33:fieldvaluelist:0:description"]',
        'doc_to_sources': '//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:34:fieldvaluelist:0:description"]'
    }

    ds_template_xpaths = {
        #'host_dataverse': '',
        'title': '//*[@id="templateForm:j_idt620:0:j_idt623:0:fieldvaluelist:0:inputText"]',
        'author_name': '//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:0:inputText"]',
        'author_affiliation': '//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:1:inputText"]',
        #'author_id_type': '',
        'author_id': '//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:3:inputText"]',
        'contact_name': '//*[@id="templateForm:j_idt620:0:j_idt623:6:j_idt677:0:j_idt679:0:inputText"]',
        'contact_affiliation': '//*[@id="templateForm:j_idt620:0:j_idt623:6:j_idt677:0:j_idt679:1:inputText"]',
        'contact_email': '//*[@id="templateForm:j_idt620:0:j_idt623:6:j_idt677:0:j_idt679:2:inputText"]',
        'description': '//*[@id="templateForm:j_idt620:0:j_idt623:7:j_idt677:0:j_idt679:0:description"]',
        'date': '//*[@id="templateForm:j_idt620:0:j_idt623:7:j_idt677:0:j_idt679:1:inputText"]',
        #'subject': '',
        'keyword_term': '//*[@id="templateForm:j_idt620:0:j_idt623:9:j_idt677:0:j_idt679:0:inputText"]',
        'keyword_cv_name': '//*[@id="templateForm:j_idt620:0:j_idt623:9:j_idt677:0:j_idt679:1:inputText"]',
        'keyword_cv_url': '//*[@id="templateForm:j_idt620:0:j_idt623:9:j_idt677:0:j_idt679:2:inputText"]',
        'related_pub_citation': '//*[@id="templateForm:j_idt620:0:j_idt623:11:j_idt677:0:j_idt679:0:description"]',
        #'related_pub_id_type': '',
        'related_pub_id': '//*[@id="templateForm:j_idt620:0:j_idt623:11:j_idt677:0:j_idt679:2:inputText"]',
        'related_pub_url': '//*[@id="templateForm:j_idt620:0:j_idt623:11:j_idt677:0:j_idt679:3:inputText"]',
        'notes': '//*[@id="templateForm:j_idt620:0:j_idt623:12:fieldvaluelist:0:description"]',
        'depositor': '//*[@id="templateForm:j_idt620:0:j_idt623:21:fieldvaluelist:0:inputText"]',
        'deposit_date': '//*[@id="templateForm:j_idt620:0:j_idt623:22:fieldvaluelist:0:inputText"]',
        
        'subtitle': '//*[@id="templateForm:j_idt620:0:j_idt623:1:fieldvaluelist:0:inputText"]',
        'alternative_title': '//*[@id="templateForm:j_idt620:0:j_idt623:2:fieldvaluelist:0:inputText"]',
        'alternative_url': '//*[@id="templateForm:j_idt620:0:j_idt623:3:fieldvaluelist:0:inputText"]',
        'other_id_agency': '//*[@id="templateForm:j_idt620:0:j_idt623:4:j_idt677:0:j_idt679:0:inputText"]',
        'other_id_id': '//*[@id="templateForm:j_idt620:0:j_idt623:4:j_idt677:0:j_idt679:1:inputText"]',
        'topic_class_term': '//*[@id="templateForm:j_idt620:0:j_idt623:10:j_idt677:0:j_idt679:0:inputText"]',
        'topic_class_cv_name': '//*[@id="templateForm:j_idt620:0:j_idt623:10:j_idt677:0:j_idt679:1:inputText"]',
        'topic_class_cv_url': '//*[@id="templateForm:j_idt620:0:j_idt623:10:j_idt677:0:j_idt679:2:inputText"]',
        #'language': '',
        'producer_name': '//*[@id="templateForm:j_idt620:0:j_idt623:14:j_idt677:0:j_idt679:0:inputText"]',
        'producer_affiliation': '//*[@id="templateForm:j_idt620:0:j_idt623:14:j_idt677:0:j_idt679:1:inputText"]',
        'producer_abbrev_name': '//*[@id="templateForm:j_idt620:0:j_idt623:14:j_idt677:0:j_idt679:2:inputText"]',
        'producer_url': '//*[@id="templateForm:j_idt620:0:j_idt623:14:j_idt677:0:j_idt679:3:inputText"]',
        'producer_logo_url': '//*[@id="templateForm:j_idt620:0:j_idt623:14:j_idt677:0:j_idt679:4:inputText"]',
        'producer_date': '//*[@id="templateForm:j_idt620:0:j_idt623:15:fieldvaluelist:0:inputText"]',
        'producer_location': '//*[@id="templateForm:j_idt620:0:j_idt623:16:fieldvaluelist:0:inputText"]',
        #'contributor_type': '',
        'contributor_name': '//*[@id="templateForm:j_idt620:0:j_idt623:17:j_idt677:0:j_idt679:1:inputText"]',
        'funding_info_agency': '//*[@id="templateForm:j_idt620:0:j_idt623:18:j_idt677:0:j_idt679:0:inputText"]',
        'funding_info_id': '//*[@id="templateForm:j_idt620:0:j_idt623:18:j_idt677:0:j_idt679:1:inputText"]',
        'distributor_name': '//*[@id="templateForm:j_idt620:0:j_idt623:19:j_idt677:0:j_idt679:0:inputText"]',
        'distributor_affiliation': '//*[@id="templateForm:j_idt620:0:j_idt623:19:j_idt677:0:j_idt679:1:inputText"]',
        'distributor_abbrev_name': '//*[@id="templateForm:j_idt620:0:j_idt623:19:j_idt677:0:j_idt679:2:inputText"]',
        'distributor_url': '//*[@id="templateForm:j_idt620:0:j_idt623:19:j_idt677:0:j_idt679:3:inputText"]',
        'distributor_logo_url': '//*[@id="templateForm:j_idt620:0:j_idt623:19:j_idt677:0:j_idt679:4:inputText"]',
        'distribution_date': '//*[@id="templateForm:j_idt620:0:j_idt623:20:fieldvaluelist:0:inputText"]',
        'time_period_start': '//*[@id="templateForm:j_idt620:0:j_idt623:23:j_idt677:0:j_idt679:0:inputText"]',
        'time_period_end': '//*[@id="templateForm:j_idt620:0:j_idt623:23:j_idt677:0:j_idt679:1:inputText"]',
        'date_of_collection_start': '//*[@id="templateForm:j_idt620:0:j_idt623:24:j_idt677:0:j_idt679:0:inputText"]',
        'date_of_collection_end': '//*[@id="templateForm:j_idt620:0:j_idt623:24:j_idt677:0:j_idt679:1:inputText"]',
        'data_type': '//*[@id="templateForm:j_idt620:0:j_idt623:25:fieldvaluelist:0:inputText"]',
        'series_name': '//*[@id="templateForm:j_idt620:0:j_idt623:26:j_idt677:0:j_idt679:0:inputText"]',
        'series_info': '//*[@id="templateForm:j_idt620:0:j_idt623:26:j_idt677:0:j_idt679:1:description"]',
        'software_name': '//*[@id="templateForm:j_idt620:0:j_idt623:27:j_idt677:0:j_idt679:0:inputText"]',
        'software_version': '//*[@id="templateForm:j_idt620:0:j_idt623:27:j_idt677:0:j_idt679:1:inputText"]',
        'related_material': '//*[@id="templateForm:j_idt620:0:j_idt623:28:fieldvaluelist:0:description"]',
        'related_dataset': '//*[@id="templateForm:j_idt620:0:j_idt623:29:fieldvaluelist:0:description"]',
        'other_reference': '//*[@id="templateForm:j_idt620:0:j_idt623:30:fieldvaluelist:0:inputText"]',
        'data_source': '//*[@id="templateForm:j_idt620:0:j_idt623:31:fieldvaluelist:0:description"]',
        'origin_hist_sources': '//*[@id="templateForm:j_idt620:0:j_idt623:32:fieldvaluelist:0:description"]',
        'character_of_sources': '//*[@id="templateForm:j_idt620:0:j_idt623:33:fieldvaluelist:0:description"]',
        'doc_to_sources': '//*[@id="templateForm:j_idt620:0:j_idt623:34:fieldvaluelist:0:description"]'
    }

#//*[@id="templateForm:j_idt620:0:j_idt623:4:compinstr_display"]

    #This doesn't include the ends of the xpaths as we append different values to it for set vs check
    ds_template_instruct_xpaths_incomplete = {
        'title': '//*[@id="templateForm:j_idt620:0:j_idt623:0:instr',
        'subtitle': '//*[@id="templateForm:j_idt620:0:j_idt623:1:instr',
        'alternative_title': '//*[@id="templateForm:j_idt620:0:j_idt623:2:instr',
        'alternative_url': '//*[@id="templateForm:j_idt620:0:j_idt623:3:instr',
        'other_id': '//*[@id="templateForm:j_idt620:0:j_idt623:4:compinstr',
        'author': '//*[@id="templateForm:j_idt620:0:j_idt623:5:compinstr',
        'contact': '//*[@id="templateForm:j_idt620:0:j_idt623:6:compinstr',
        'description': '//*[@id="templateForm:j_idt620:0:j_idt623:7:compinstr',
        'subject': '//*[@id="templateForm:j_idt620:0:j_idt623:8:instr', 
        'keyword': '//*[@id="templateForm:j_idt620:0:j_idt623:9:compinstr',
        'topic_class': '//*[@id="templateForm:j_idt620:0:j_idt623:10:compinstr',
        'related_pub': '//*[@id="templateForm:j_idt620:0:j_idt623:11:compinstr',
        'notes': '//*[@id="templateForm:j_idt620:0:j_idt623:12:instr',
        'language': '//*[@id="templateForm:j_idt620:0:j_idt623:13:instr',
        'producer': '//*[@id="templateForm:j_idt620:0:j_idt623:14:compinstr',
        'producer_date': '//*[@id="templateForm:j_idt620:0:j_idt623:15:instr',
        'producer_location': '//*[@id="templateForm:j_idt620:0:j_idt623:16:instr',
        'contributor': '//*[@id="templateForm:j_idt620:0:j_idt623:17:compinstr',
        'funding_info': '//*[@id="templateForm:j_idt620:0:j_idt623:18:compinstr',
        'distributor': '//*[@id="templateForm:j_idt620:0:j_idt623:19:compinstr',
        'distribution_date': '//*[@id="templateForm:j_idt620:0:j_idt623:20:instr',
        'depositor': '//*[@id="templateForm:j_idt620:0:j_idt623:21:instr',
        'deposit_date': '//*[@id="templateForm:j_idt620:0:j_idt623:22:instr',
        'time_period': '//*[@id="templateForm:j_idt620:0:j_idt623:23:compinstr',
        'date_of_collection': '//*[@id="templateForm:j_idt620:0:j_idt623:24:compinstr',
        'data_type': '//*[@id="templateForm:j_idt620:0:j_idt623:25:instr',
        'series': '//*[@id="templateForm:j_idt620:0:j_idt623:26:compinstr',
        'software': '//*[@id="templateForm:j_idt620:0:j_idt623:27:compinstr',
        'related_material': '//*[@id="templateForm:j_idt620:0:j_idt623:28:instr',
        'related_dataset': '//*[@id="templateForm:j_idt620:0:j_idt623:29:instr',
        'other_reference': '//*[@id="templateForm:j_idt620:0:j_idt623:30:instr',
        'data_source': '//*[@id="templateForm:j_idt620:0:j_idt623:31:instr',
        'origin_hist_sources': '//*[@id="templateForm:j_idt620:0:j_idt623:32:instr',
        'character_of_sources': '//*[@id="templateForm:j_idt620:0:j_idt623:33:instr',
        'doc_to_sources': '//*[@id="templateForm:j_idt620:0:j_idt623:34:instr'
    }

    ds_template_instruct_props = {
        'title': 'instructions title',
        'subtitle': 'instructions subtitle',
        'alternative_title': 'instructions alt title',
        'alternative_url': 'instructions alt url',
        'other_id': 'instructions other id',
        'author': 'instructions author',
        'contact': 'instructions contact',
        'description': 'instructions description',
        'subject': 'instructions subject', 
        'keyword': 'instructions keyword',
        'topic_class': 'instructions topic class',
        'related_pub': 'instructions related pub',
        'notes': 'instructions notes',
        'language': 'instructions language',
        'producer': 'instructions producer',
        'producer_date': 'instructions producer_date',
        'producer_location': 'instructions producer_location',
        'contributor': 'instructions contributor',
        'funding_info': 'instructions finding_info',
        'distributor': 'instructions distributor',
        'distribution_date': 'instructions distribution_date',
        'depositor': 'instructions depositor',
        'deposit_date': 'instructions deposit_date',
        'time_period': 'instructions time_period',
        'date_of_collection': 'instructions date_of_collection',
        'data_type': 'instructions data_type',
        'series': 'instructions series',
        'software': 'instructions software',
        'related_material': 'instructions related_material',
        'related_dataset': 'instructions related_dataset',
        'other_reference': 'instructions other ref',
        'data_source': 'instructions data_source',
        'origin_hist_sources': 'instructions origin_hist',
        'character_of_sources': 'instructions character',
        'doc_to_sources': 'instructions doc'
    }

    ds_license_xpaths = {
        'terms_restricted': '//*[@id="templateForm:metadata_TermsAccess"]',
        'access_place': '//*[@id="templateForm:dataAccessPlace"]',
        'original_archive': '//*[@id="templateForm:originalArchive"]',
        'available_status': '//*[@id="templateForm:availabilityStatus"]',
        'access_contact': '//*[@id="templateForm:contactForAccess"]',
        'collection_size': '//*[@id="templateForm:sizeOfCollection"]',
        'study_completion': '//*[@id="templateForm:studyCompletion"]'
    }

    ds_license_props = {
        'terms_restricted': 'restricted',
        'access_place': 'data access place',
        'original_archive': 'original archive',
        'available_status': 'availability status',
        'access_contact': 'contact for access',
        'collection_size': 'size of collection',
        'study_completion': 'study completion'
    }

    #########################################
    ### Dataset Test Additional Functions ###
    #########################################


    #TODO: move?
    def set_template_license(self, add_string=''):
        self.sesh.find_element('xpath','//*[@id="templateForm:licenses_label"]').click() #click license dropdown
        time.sleep(.2)
        self.sesh.find_element('xpath','//*[@id="templateForm:licenses_1"]').click() #click "cc-by 4.0" inside dropdown
        time.sleep(.2)
        
        self.sesh.find_element('xpath',self.ds_license_xpaths['terms_restricted']).clear()
        self.sesh.find_element('xpath',self.ds_license_xpaths['terms_restricted']).send_keys(add_string + self.ds_license_props['terms_restricted'])
        self.sesh.find_element('xpath',self.ds_license_xpaths['access_place']).clear()
        self.sesh.find_element('xpath',self.ds_license_xpaths['access_place']).send_keys(add_string + self.ds_license_props['access_place'])
        self.sesh.find_element('xpath',self.ds_license_xpaths['original_archive']).clear()
        self.sesh.find_element('xpath',self.ds_license_xpaths['original_archive']).send_keys(add_string + self.ds_license_props['original_archive'])
        self.sesh.find_element('xpath',self.ds_license_xpaths['available_status']).clear()
        self.sesh.find_element('xpath',self.ds_license_xpaths['available_status']).send_keys(add_string + self.ds_license_props['available_status'])
        self.sesh.find_element('xpath',self.ds_license_xpaths['access_contact']).clear()
        self.sesh.find_element('xpath',self.ds_license_xpaths['access_contact']).send_keys(add_string + self.ds_license_props['access_contact'])
        self.sesh.find_element('xpath',self.ds_license_xpaths['collection_size']).clear()
        self.sesh.find_element('xpath',self.ds_license_xpaths['collection_size']).send_keys(add_string + self.ds_license_props['collection_size'])
        self.sesh.find_element('xpath',self.ds_license_xpaths['study_completion']).clear()
        self.sesh.find_element('xpath',self.ds_license_xpaths['study_completion']).send_keys(add_string + self.ds_license_props['study_completion'])

    def confirm_template_license(self, add_string=''):
        self.assertEqual(self.sesh.find_element('xpath',self.ds_license_xpaths['terms_restricted']).get_attribute('value'), add_string+self.ds_license_props['terms_restricted'])
        self.assertEqual(self.sesh.find_element('xpath',self.ds_license_xpaths['access_place']).get_attribute('value'), add_string+self.ds_license_props['access_place'])
        self.assertEqual(self.sesh.find_element('xpath',self.ds_license_xpaths['original_archive']).get_attribute('value'), add_string+self.ds_license_props['original_archive'])
        self.assertEqual(self.sesh.find_element('xpath',self.ds_license_xpaths['available_status']).get_attribute('value'), add_string+self.ds_license_props['available_status'])
        self.assertEqual(self.sesh.find_element('xpath',self.ds_license_xpaths['access_contact']).get_attribute('value'), add_string+self.ds_license_props['access_contact'])
        self.assertEqual(self.sesh.find_element('xpath',self.ds_license_xpaths['collection_size']).get_attribute('value'), add_string+self.ds_license_props['collection_size'])
        self.assertEqual(self.sesh.find_element('xpath',self.ds_license_xpaths['study_completion']).get_attribute('value'), add_string+self.ds_license_props['study_completion'])

    # We have different functions for create / edit as the xpath changes between the two, and there is no other way to get the fields
    def set_dataset_metadata_create(self, add_string=''):
        # We clear all the elements for when this code is called during edit and there are already contents
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:0:fieldvaluelist:0:inputText"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:0:fieldvaluelist:0:inputText"]').send_keys(add_string + self.ds_props['title'])
        
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:0:inputText"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:0:inputText"]').send_keys(add_string + self.ds_props['author_name'])
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:1:inputText"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:1:inputText"]').send_keys(add_string + self.ds_props['author_affiliation'])
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:2:cvv_label"]').click() #click author identifier type dropdown
        time.sleep(.2)
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:2:cvv_2"]').click() #click "ISNI" inside dropdown
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:3:inputText"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:3:inputText"]').send_keys(add_string + self.ds_props['author_id'])
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:6:j_idt630:0:j_idt632:0:inputText"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:6:j_idt630:0:j_idt632:0:inputText"]').send_keys(add_string + self.ds_props['contact_name'])
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:6:j_idt630:0:j_idt632:1:inputText"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:6:j_idt630:0:j_idt632:1:inputText"]').send_keys(add_string + self.ds_props['contact_affiliation'])
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:6:j_idt630:0:j_idt632:2:inputText"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:6:j_idt630:0:j_idt632:2:inputText"]').send_keys(add_string + self.ds_props['contact_email'])
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:7:j_idt630:0:j_idt632:0:description"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:7:j_idt630:0:j_idt632:0:description"]').send_keys(add_string + self.ds_props['description'])
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:7:j_idt630:0:j_idt632:1:inputText"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:7:j_idt630:0:j_idt632:1:inputText"]').send_keys(self.ds_props['date'])
        #TODO: add a clear for the select thing?
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:8:unique2"]').click() #click subject dropdown
        time.sleep(.2)
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:8:unique2_panel"]/div[2]/ul/li[14]/div').click() #click "other" inside dropdown
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:9:j_idt630:0:j_idt632:0:inputText"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:9:j_idt630:0:j_idt632:0:inputText"]').send_keys(add_string + self.ds_props['keyword_term'])
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:9:j_idt630:0:j_idt632:1:inputText"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:9:j_idt630:0:j_idt632:1:inputText"]').send_keys(add_string + self.ds_props['keyword_cv_name'])
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:9:j_idt630:0:j_idt632:2:inputText"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:9:j_idt630:0:j_idt632:2:inputText"]').send_keys(self.ds_props['keyword_cv_url']+add_string)
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:0:description"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:0:description"]').send_keys(add_string + self.ds_props['related_pub_citation'])
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:1:cvv_label"]').click() #click related pub id type dropdown
        time.sleep(.2)
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:1:cvv_4"]').click() #click "doi" inside dropdown
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:2:inputText"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:2:inputText"]').send_keys(add_string + self.ds_props['related_pub_id'])
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:3:inputText"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:3:inputText"]').send_keys(self.ds_props['related_pub_url']+add_string)
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:12:fieldvaluelist:0:description"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:12:fieldvaluelist:0:description"]').send_keys(add_string + self.ds_props['notes'])
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:21:fieldvaluelist:0:inputText"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:21:fieldvaluelist:0:inputText"]').send_keys(add_string + self.ds_props['depositor'])
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:22:fieldvaluelist:0:inputText"]').clear()
        self.sesh.find_element('xpath','//*[@id="datasetForm:j_idt573:0:j_idt576:22:fieldvaluelist:0:inputText"]').send_keys(self.ds_props['deposit_date'])
        
        #TODO: Upload files here?

    #also supports dataset template
    def set_dataset_metadata_edit(self, add_string='', xpath_dict=None):
        #NOTE: For some reason moving some of these dropdown tests to the bottom of this files causes it to fail. Is it because they are too far off the page or... I have no idea what?
        if xpath_dict == self.ds_edit_xpaths:
            self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:2:cvv"]').click() #click author identifier type dropdown
            time.sleep(1)
            self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:2:cvv_4"]').click() #click "VIAF" inside dropdown
            time.sleep(2)
            # self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:2:cvv"]').click() #click author identifier type dropdown to close

            # time.sleep(1)
            self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:8:unique2"]/ul/li/span[2]').click() #Delete existing field "Other"
            time.sleep(1)
            self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:8:unique2"]').click() #click subject dropdown
            time.sleep(1)
            self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:8:unique2_panel"]/div[2]/ul/li[10]/div').click() #click "mathematical science" inside dropdown
            #self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:1:cvv"]/div[3]').click() #click related pub id type dropdown
            
            self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:1:cvv"]').click() #click related pub id type dropdown
            time.sleep(.5)
            self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:1:cvv_4"]').click() #click "DOI" inside dropdown
            
            time.sleep(.5)
            self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:13:unique2"]/div[3]').click() #click language dropdown
            time.sleep(.5)
            self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:13:unique2_panel"]/div[2]/ul/li[2]').click() #click "Afar" inside dropdown
            
            self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:17:j_idt1679:0:j_idt1681:0:cvv"]').click() #click contributor type dropdown
            time.sleep(.5)
            self.sesh.find_element('xpath','//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:17:j_idt1679:0:j_idt1681:0:cvv_3"]').click() #click "Data Manager" inside dropdown
            
            # self.sesh.find_element('xpath','//*[@id="datasetForm:saveBottom"]').click() #create dataset
        elif xpath_dict == self.ds_template_xpaths:
            self.sesh.find_element('xpath','//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:2:cvv"]').click() #click author identifier type dropdown
            time.sleep(1)
            self.sesh.find_element('xpath','//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:2:cvv_5"]').click() #click "GND" inside dropdown
            # time.sleep(2)
            # self.sesh.find_element('xpath','//*[@id="templateForm:j_idt620:0:j_idt623:5:j_idt677:0:j_idt679:2:cvv"]').click() #exit popup as clicking the element doesn't work
            time.sleep(1)

            self.sesh.find_element('xpath','//*[@id="templateForm:j_idt620:0:j_idt623:8:editPrimitiveValueFragment"]/div[3]/div/div/div').click() #click subject dropdown
            time.sleep(.5)
            self.sesh.find_element('xpath','//*[@id="templateForm:j_idt620:0:j_idt623:8:unique2_panel"]/div[2]/ul/li[6]').click() #click "Computer and Information Science" inside dropdown
            
            self.sesh.find_element('xpath','//*[@id="templateForm:j_idt620:0:j_idt623:11:j_idt677:0:j_idt679:1:cvv"]').click() #click related pub id type dropdown
            time.sleep(.5)
            self.sesh.find_element('xpath','//*[@id="templateForm:j_idt620:0:j_idt623:11:j_idt677:0:j_idt679:1:cvv_5"]').click() #click "ean13" inside dropdown
            
            time.sleep(.5)
            self.sesh.find_element('xpath','//*[@id="templateForm:j_idt620:0:j_idt623:13:unique2"]').click() #click language dropdown
            time.sleep(.5)
            self.sesh.find_element('xpath','//*[@id="templateForm:j_idt620:0:j_idt623:13:unique2_panel"]/div[2]/ul/li[72]').click() #click "Inuktitut" inside dropdown
            
            self.sesh.find_element('xpath','//*[@id="templateForm:j_idt620:0:j_idt623:17:j_idt677:0:j_idt679:0:cvv"]').click() #click contributor type dropdown
            time.sleep(.5)
            self.sesh.find_element('xpath','//*[@id="templateForm:j_idt620:0:j_idt623:17:j_idt677:0:j_idt679:0:cvv_11"]').click() #click "Researcher" inside dropdown

        self.sesh.find_element('xpath',xpath_dict['title']).clear()
        self.sesh.find_element('xpath',xpath_dict['title']).send_keys(add_string + self.ds_props['title'])
        self.sesh.find_element('xpath',xpath_dict['author_name']).clear()
        self.sesh.find_element('xpath',xpath_dict['author_name']).send_keys(add_string + self.ds_props['author_name'])
        self.sesh.find_element('xpath',xpath_dict['author_affiliation']).clear()
        self.sesh.find_element('xpath',xpath_dict['author_affiliation']).send_keys(add_string + self.ds_props['author_affiliation'])
        self.sesh.find_element('xpath',xpath_dict['author_id']).clear()
        self.sesh.find_element('xpath',xpath_dict['author_id']).send_keys(add_string + self.ds_props['author_id'])
        self.sesh.find_element('xpath',xpath_dict['contact_name']).clear()
        self.sesh.find_element('xpath',xpath_dict['contact_name']).send_keys(add_string + self.ds_props['contact_name'])
        self.sesh.find_element('xpath',xpath_dict['contact_affiliation']).clear()
        self.sesh.find_element('xpath',xpath_dict['contact_affiliation']).send_keys(add_string + self.ds_props['contact_affiliation'])
        self.sesh.find_element('xpath',xpath_dict['contact_email']).clear()
        self.sesh.find_element('xpath',xpath_dict['contact_email']).send_keys(add_string + self.ds_props['contact_email'])
        self.sesh.find_element('xpath',xpath_dict['description']).clear()
        self.sesh.find_element('xpath',xpath_dict['description']).send_keys(add_string + self.ds_props['description'])
        self.sesh.find_element('xpath',xpath_dict['date']).clear()
        self.sesh.find_element('xpath',xpath_dict['date']).send_keys(self.ds_props['date'])
        self.sesh.find_element('xpath',xpath_dict['keyword_term']).clear()
        self.sesh.find_element('xpath',xpath_dict['keyword_term']).send_keys(add_string + self.ds_props['keyword_term'])
        self.sesh.find_element('xpath',xpath_dict['keyword_cv_name']).clear()
        self.sesh.find_element('xpath',xpath_dict['keyword_cv_name']).send_keys(add_string + self.ds_props['keyword_cv_name'])
        self.sesh.find_element('xpath',xpath_dict['keyword_cv_url']).clear()
        self.sesh.find_element('xpath',xpath_dict['keyword_cv_url']).send_keys(self.ds_props['keyword_cv_url']+add_string)
        self.sesh.find_element('xpath',xpath_dict['related_pub_citation']).clear()
        self.sesh.find_element('xpath',xpath_dict['related_pub_citation']).send_keys(add_string + self.ds_props['related_pub_citation'])
        self.sesh.find_element('xpath',xpath_dict['related_pub_id']).clear()
        self.sesh.find_element('xpath',xpath_dict['related_pub_id']).send_keys(add_string + self.ds_props['related_pub_id'])
        self.sesh.find_element('xpath',xpath_dict['related_pub_url']).clear()
        self.sesh.find_element('xpath',xpath_dict['related_pub_url']).send_keys(self.ds_props['related_pub_url']+add_string)
        self.sesh.find_element('xpath',xpath_dict['notes']).clear()
        self.sesh.find_element('xpath',xpath_dict['notes']).send_keys(add_string + self.ds_props['notes'])
        self.sesh.find_element('xpath',xpath_dict['depositor']).clear()
        self.sesh.find_element('xpath',xpath_dict['depositor']).send_keys(add_string + self.ds_props['depositor'])
        self.sesh.find_element('xpath',xpath_dict['deposit_date']).clear()
        self.sesh.find_element('xpath',xpath_dict['deposit_date']).send_keys(self.ds_props['deposit_date'])
        
        self.sesh.find_element('xpath',xpath_dict['subtitle']).clear()
        self.sesh.find_element('xpath',xpath_dict['subtitle']).send_keys(add_string + self.ds_props['subtitle'])
        self.sesh.find_element('xpath',xpath_dict['alternative_title']).clear()
        self.sesh.find_element('xpath',xpath_dict['alternative_title']).send_keys(add_string + self.ds_props['alternative_title'])
        self.sesh.find_element('xpath',xpath_dict['alternative_url']).clear()
        self.sesh.find_element('xpath',xpath_dict['alternative_url']).send_keys(self.ds_props['alternative_url']+add_string)
        self.sesh.find_element('xpath',xpath_dict['other_id_agency']).clear()
        self.sesh.find_element('xpath',xpath_dict['other_id_agency']).send_keys(add_string + self.ds_props['other_id_agency'])
        self.sesh.find_element('xpath',xpath_dict['other_id_id']).clear()
        self.sesh.find_element('xpath',xpath_dict['other_id_id']).send_keys(add_string + self.ds_props['other_id_id'])
        self.sesh.find_element('xpath',xpath_dict['topic_class_term']).clear()
        self.sesh.find_element('xpath',xpath_dict['topic_class_term']).send_keys(add_string + self.ds_props['topic_class_term'])
        self.sesh.find_element('xpath',xpath_dict['topic_class_cv_name']).clear()
        self.sesh.find_element('xpath',xpath_dict['topic_class_cv_name']).send_keys(add_string + self.ds_props['topic_class_cv_name'])
        self.sesh.find_element('xpath',xpath_dict['topic_class_cv_url']).clear()
        self.sesh.find_element('xpath',xpath_dict['topic_class_cv_url']).send_keys(self.ds_props['topic_class_cv_url']+add_string)
        self.sesh.find_element('xpath',xpath_dict['producer_name']).clear()
        self.sesh.find_element('xpath',xpath_dict['producer_name']).send_keys(add_string + self.ds_props['producer_name'])
        self.sesh.find_element('xpath',xpath_dict['producer_affiliation']).clear()
        self.sesh.find_element('xpath',xpath_dict['producer_affiliation']).send_keys(add_string + self.ds_props['producer_affiliation'])
        self.sesh.find_element('xpath',xpath_dict['producer_abbrev_name']).clear()
        self.sesh.find_element('xpath',xpath_dict['producer_abbrev_name']).send_keys(add_string + self.ds_props['producer_abbrev_name'])
        self.sesh.find_element('xpath',xpath_dict['producer_url']).clear()
        self.sesh.find_element('xpath',xpath_dict['producer_url']).send_keys(self.ds_props['producer_url']+add_string)
        self.sesh.find_element('xpath',xpath_dict['producer_logo_url']).clear()
        self.sesh.find_element('xpath',xpath_dict['producer_logo_url']).send_keys(self.ds_props['producer_logo_url']+add_string)
        self.sesh.find_element('xpath',xpath_dict['producer_date']).clear()
        self.sesh.find_element('xpath',xpath_dict['producer_date']).send_keys(self.ds_props['producer_date'])
        self.sesh.find_element('xpath',xpath_dict['producer_location']).clear()
        self.sesh.find_element('xpath',xpath_dict['producer_location']).send_keys(add_string + self.ds_props['producer_location'])
        self.sesh.find_element('xpath',xpath_dict['contributor_name']).clear()
        self.sesh.find_element('xpath',xpath_dict['contributor_name']).send_keys(add_string + self.ds_props['contributor_name'])
        self.sesh.find_element('xpath',xpath_dict['funding_info_agency']).clear()
        self.sesh.find_element('xpath',xpath_dict['funding_info_agency']).send_keys(add_string + self.ds_props['funding_info_agency'])
        self.sesh.find_element('xpath',xpath_dict['funding_info_id']).clear()
        self.sesh.find_element('xpath',xpath_dict['funding_info_id']).send_keys(add_string + self.ds_props['funding_info_id'])
        self.sesh.find_element('xpath',xpath_dict['distributor_name']).clear()
        self.sesh.find_element('xpath',xpath_dict['distributor_name']).send_keys(add_string + self.ds_props['distributor_name'])
        self.sesh.find_element('xpath',xpath_dict['distributor_affiliation']).clear()
        self.sesh.find_element('xpath',xpath_dict['distributor_affiliation']).send_keys(add_string + self.ds_props['distributor_affiliation'])
        self.sesh.find_element('xpath',xpath_dict['distributor_abbrev_name']).clear()
        self.sesh.find_element('xpath',xpath_dict['distributor_abbrev_name']).send_keys(add_string + self.ds_props['distributor_abbrev_name'])
        self.sesh.find_element('xpath',xpath_dict['distributor_url']).clear()
        self.sesh.find_element('xpath',xpath_dict['distributor_url']).send_keys(self.ds_props['distributor_url']+add_string)
        self.sesh.find_element('xpath',xpath_dict['distributor_logo_url']).clear()
        self.sesh.find_element('xpath',xpath_dict['distributor_logo_url']).send_keys(self.ds_props['distributor_logo_url']+add_string)
        self.sesh.find_element('xpath',xpath_dict['distribution_date']).clear()
        self.sesh.find_element('xpath',xpath_dict['distribution_date']).send_keys(self.ds_props['distribution_date'])
        self.sesh.find_element('xpath',xpath_dict['time_period_start']).clear()
        self.sesh.find_element('xpath',xpath_dict['time_period_start']).send_keys(self.ds_props['time_period_start'])
        self.sesh.find_element('xpath',xpath_dict['time_period_end']).clear()
        self.sesh.find_element('xpath',xpath_dict['time_period_end']).send_keys(self.ds_props['time_period_end'])
        self.sesh.find_element('xpath',xpath_dict['date_of_collection_start']).clear()
        self.sesh.find_element('xpath',xpath_dict['date_of_collection_start']).send_keys(self.ds_props['date_of_collection_start'])
        self.sesh.find_element('xpath',xpath_dict['date_of_collection_end']).clear()
        self.sesh.find_element('xpath',xpath_dict['date_of_collection_end']).send_keys(self.ds_props['date_of_collection_end'])
        self.sesh.find_element('xpath',xpath_dict['data_type']).clear()
        self.sesh.find_element('xpath',xpath_dict['data_type']).send_keys(add_string + self.ds_props['data_type'])
        self.sesh.find_element('xpath',xpath_dict['series_name']).clear()
        self.sesh.find_element('xpath',xpath_dict['series_name']).send_keys(add_string + self.ds_props['series_name'])
        self.sesh.find_element('xpath',xpath_dict['series_info']).clear()
        self.sesh.find_element('xpath',xpath_dict['series_info']).send_keys(add_string + self.ds_props['series_info'])
        self.sesh.find_element('xpath',xpath_dict['software_name']).clear()
        self.sesh.find_element('xpath',xpath_dict['software_name']).send_keys(add_string + self.ds_props['software_name'])
        self.sesh.find_element('xpath',xpath_dict['software_version']).clear()
        self.sesh.find_element('xpath',xpath_dict['software_version']).send_keys(add_string + self.ds_props['software_version'])
        self.sesh.find_element('xpath',xpath_dict['related_material']).clear()
        self.sesh.find_element('xpath',xpath_dict['related_material']).send_keys(add_string + self.ds_props['related_material'])
        self.sesh.find_element('xpath',xpath_dict['related_dataset']).clear()
        self.sesh.find_element('xpath',xpath_dict['related_dataset']).send_keys(add_string + self.ds_props['related_dataset'])
        self.sesh.find_element('xpath',xpath_dict['other_reference']).clear()
        self.sesh.find_element('xpath',xpath_dict['other_reference']).send_keys(add_string + self.ds_props['other_reference'])
        self.sesh.find_element('xpath',xpath_dict['data_source']).clear()
        self.sesh.find_element('xpath',xpath_dict['data_source']).send_keys(add_string + self.ds_props['data_source'])
        self.sesh.find_element('xpath',xpath_dict['origin_hist_sources']).clear()
        self.sesh.find_element('xpath',xpath_dict['origin_hist_sources']).send_keys(add_string + self.ds_props['origin_hist_sources'])    
        self.sesh.find_element('xpath',xpath_dict['character_of_sources']).clear()
        self.sesh.find_element('xpath',xpath_dict['character_of_sources']).send_keys(add_string + self.ds_props['character_of_sources'])    
        self.sesh.find_element('xpath',xpath_dict['doc_to_sources']).clear()
        self.sesh.find_element('xpath',xpath_dict['doc_to_sources']).send_keys(add_string + self.ds_props['doc_to_sources'])    

    #Also supports dataset template
    def confirm_dataset_metadata(self, add_string='', is_update=False, xpath_dict=None):
        # if (is_update) {
        #     time.sleep(999999999)
        # }
        # add_string='edit'
        # is_update=TRUE
        
        #For some reason, dates are false when tested identical. I'm not sure if some character is being replaced on the backend or what. But this is fine
        #We don't currently test some dropdowns results because it is extremely convoluted to test the values of jquery dropdowns.
        self.assertEqual(self.sesh.find_element('xpath',xpath_dict['title']).get_attribute('value'), add_string+self.ds_props['title'])
        self.assertEqual(self.sesh.find_element('xpath',xpath_dict['author_name']).get_attribute('value'), add_string+self.ds_props['author_name'])
        self.assertEqual(self.sesh.find_element('xpath',xpath_dict['author_affiliation']).get_attribute('value'), add_string+self.ds_props['author_affiliation'])
        #self.assertEqual(self.sesh.find_element('xpath',xpath_dict['author_id_type']).get_attribute('value'), add_string+self.ds_props['author_id_type'])
        self.assertEqual(self.sesh.find_element('xpath',xpath_dict['author_id']).get_attribute('value'), add_string+self.ds_props['author_id'])
        self.assertEqual(self.sesh.find_element('xpath',xpath_dict['contact_name']).get_attribute('value'), add_string+self.ds_props['contact_name'])
        self.assertEqual(self.sesh.find_element('xpath',xpath_dict['contact_affiliation']).get_attribute('value'), add_string+self.ds_props['contact_affiliation'])
        self.assertEqual(self.sesh.find_element('xpath',xpath_dict['contact_email']).get_attribute('value'), add_string+self.ds_props['contact_email'])
        self.assertEqual(self.sesh.find_element('xpath',xpath_dict['description']).get_attribute('value'), add_string+self.ds_props['description'])
        self.assertEqual(self.sesh.find_element('xpath',xpath_dict['date']).get_attribute('value'), self.ds_props['date'])
        #self.assertEqual(self.sesh.find_element('xpath',xpath_dict['subject']).get_attribute('value'), add_string+self.ds_props['subject'])
        self.assertEqual(self.sesh.find_element('xpath',xpath_dict['keyword_term']).get_attribute('value'), add_string+self.ds_props['keyword_term'])
        self.assertEqual(self.sesh.find_element('xpath',xpath_dict['keyword_cv_name']).get_attribute('value'), add_string+self.ds_props['keyword_cv_name'])
        self.assertEqual(self.sesh.find_element('xpath',xpath_dict['keyword_cv_url']).get_attribute('value'), self.ds_props['keyword_cv_url']+add_string)
        self.assertEqual(self.sesh.find_element('xpath',xpath_dict['related_pub_citation']).get_attribute('value'), add_string+self.ds_props['related_pub_citation'])
        #self.assertEqual(self.sesh.find_element('xpath',xpath_dict['related_pub_id_type']).get_attribute('value'), add_string+self.ds_props['related_pub_id_type']
        #TODO: I think this doesn't work because it needs the above set... but weirdly I thought it worked before???? Well it doesn't work now
        self.assertEqual(self.sesh.find_element('xpath',xpath_dict['related_pub_id']).get_attribute('value'), add_string+self.ds_props['related_pub_id'])
        self.assertEqual(self.sesh.find_element('xpath',xpath_dict['related_pub_url']).get_attribute('value'), self.ds_props['related_pub_url']+add_string)
        self.assertEqual(self.sesh.find_element('xpath',xpath_dict['notes']).get_attribute('value'), add_string+self.ds_props['notes'])
        self.assertEqual(self.sesh.find_element('xpath',xpath_dict['depositor']).get_attribute('value'), add_string+self.ds_props['depositor'])
        self.assertEqual(self.sesh.find_element('xpath',xpath_dict['deposit_date']).get_attribute('value'), self.ds_props['deposit_date'])
        
        if is_update:
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['subtitle']).get_attribute('value'), add_string+self.ds_props['subtitle'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['alternative_title']).get_attribute('value'), add_string+self.ds_props['alternative_title'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['alternative_url']).get_attribute('value'), self.ds_props['alternative_url']+add_string)
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['other_id_agency']).get_attribute('value'), add_string+self.ds_props['other_id_agency'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['other_id_id']).get_attribute('value'), add_string+self.ds_props['other_id_id'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['topic_class_term']).get_attribute('value'), add_string+self.ds_props['topic_class_term'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['topic_class_cv_name']).get_attribute('value'), add_string+self.ds_props['topic_class_cv_name'])
            # self.assertEqual(self.sesh.find_element('xpath',xpath_dict['language']).get_attribute('value'), add_string+self.ds_props['language'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['producer_name']).get_attribute('value'), add_string+self.ds_props['producer_name'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['producer_affiliation']).get_attribute('value'), add_string+self.ds_props['producer_affiliation'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['producer_abbrev_name']).get_attribute('value'), add_string+self.ds_props['producer_abbrev_name'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['producer_url']).get_attribute('value'), self.ds_props['producer_url']+add_string)
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['producer_logo_url']).get_attribute('value'), self.ds_props['producer_logo_url']+add_string)
            #NOTE: This line was an equivalent test in R
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['producer_date']).get_attribute('value'), self.ds_props['producer_date'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['producer_location']).get_attribute('value'), add_string+self.ds_props['producer_location'])
            # self.assertEqual(self.sesh.find_element('xpath',xpath_dict['contributor_type']).get_attribute('value'), add_string+self.ds_props['contributor_type'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['contributor_name']).get_attribute('value'), add_string+self.ds_props['contributor_name'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['funding_info_agency']).get_attribute('value'), add_string+self.ds_props['funding_info_agency'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['funding_info_id']).get_attribute('value'), add_string+self.ds_props['funding_info_id'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['distributor_name']).get_attribute('value'), add_string+self.ds_props['distributor_name'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['distributor_affiliation']).get_attribute('value'), add_string+self.ds_props['distributor_affiliation'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['distributor_abbrev_name']).get_attribute('value'), add_string+self.ds_props['distributor_abbrev_name'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['distributor_url']).get_attribute('value'), self.ds_props['distributor_url']+add_string)
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['distributor_logo_url']).get_attribute('value'), self.ds_props['distributor_logo_url']+add_string)
            #NOTE: The 5 lines below test equivalent before, so if they blow up in python try that again
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['distribution_date']).get_attribute('value'), self.ds_props['distribution_date'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['time_period_start']).get_attribute('value'), self.ds_props['time_period_start'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['time_period_end']).get_attribute('value'), self.ds_props['time_period_end'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['date_of_collection_start']).get_attribute('value'), self.ds_props['date_of_collection_start'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['date_of_collection_end']).get_attribute('value'), self.ds_props['date_of_collection_end'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['data_type']).get_attribute('value'), add_string+self.ds_props['data_type'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['series_name']).get_attribute('value'), add_string+self.ds_props['series_name'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['series_info']).get_attribute('value'), add_string+self.ds_props['series_info'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['software_name']).get_attribute('value'), add_string+self.ds_props['software_name'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['software_version']).get_attribute('value'), add_string+self.ds_props['software_version'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['related_material']).get_attribute('value'), add_string+self.ds_props['related_material'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['related_dataset']).get_attribute('value'), add_string+self.ds_props['related_dataset'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['other_reference']).get_attribute('value'), add_string+self.ds_props['other_reference'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['data_source']).get_attribute('value'), add_string+self.ds_props['data_source'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['origin_hist_sources']).get_attribute('value'), add_string+self.ds_props['origin_hist_sources'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['character_of_sources']).get_attribute('value'), add_string+self.ds_props['character_of_sources'])
            self.assertEqual(self.sesh.find_element('xpath',xpath_dict['doc_to_sources']).get_attribute('value'), add_string+self.ds_props['doc_to_sources'])

    #TODO: Can we check element state for these template instructions instead of waiting 1.5 seconds?
    #      Even a loop with a try catch (for a certain time probably) would be an improvement
    def set_dataset_metadata_template_instructions(self, add_string=''):
        #We loop through each instruction, click the text to add it, and add the text
        for key, xpath in self.ds_template_instruct_xpaths_incomplete.items():
            self.sesh.find_element('xpath', xpath+'"]').click()
            success = False
            for _ in range(100):
                try:
                    text_field = self.sesh.switch_to.active_element
                    text_field.clear()
                    text_field.send_keys(add_string + self.ds_template_instruct_props[key])
                    success = True
                    break
                #TODO: maybe figure out why this exception wasn't catching right. Not a big deal though
                except Exception: #selenium.common.exceptions.InvalidElementStateException:
                    pass
                time.sleep(.05)
            if not success:
                raise Exception(f"Test could not set a metadata template instruction after multiple tries. Element {xpath}")

                

    def confirm_dataset_metadata_template_instructions(self, add_string=''):
        #We loop through each instruction, click the text to add it, and add the text
        for key, xpath in self.ds_template_instruct_xpaths_incomplete.items():
            self.assertEqual(self.sesh.find_element('xpath', xpath +'_display"]').text, add_string + self.ds_template_instruct_props[key])
# self.assertEqual(self.sesh.find_element('xpath',xpath_dict['deposit_date']).get_attribute('value'), self.ds_props['deposit_date'])



    # #NOTE: We probably don't need this anymore now that we are adding it to a sub-dataverse that we are deleting
    # def delete_template_via_ui(id, dv_id):
    #     self.sesh.get(paste(dv_server_url,'/manage-templates.xhtml?dataverseId=', dv_id))
    #     template_trs = sesh$findElements(value='//*[@id="manageTemplatesForm:allTemplates_data"]/tr')
    # 
    #     for tr in template_trs:
    #         tr_id = param_get(tr$findChildElement(value='td[4]/div/div/ul/li[1]/a')$getElementAttribute("href"), c("id"
    #         if id == tr_id:
    #             tr$findChildElement(value='td[4]/div/a[3]').click()
    #             time.sleep(.2)
    #             self.sesh.find_element('xpath','//*[@id="manageTemplatesForm:contDeleteTemplateBtn"]').click()
    #             return(TRUE)
    #     
    #     print(paste("Unable to delete dataset template with id:", id))
    #     return(FALSE)
    #     #TODO: Raise exception if we get here?
    #     
    #     # STEPS:
    #     # Iterate through tr inside //*[@id="manageTemplatesForm:allTemplates_data"]
    #     # Get the ID out of the edit data / metadata menu option
    #     # - //*[@id="manageTemplatesForm:allTemplates_data"]/tr[1]/td[4]/div/div/ul/li[1]/a
    #     # - <a href="/template.xhtml?id=10&amp;ownerId=1&amp;editMode=METADATA">Metadata</a>
    #     # If it matches the provided id, we click the delete button in that tr

