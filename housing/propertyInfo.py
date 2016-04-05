'''
The following attributes are returned from the ZWILLOW API
get_property_info returns an object that has the following attributes
	- zillow_id
	- home_type
	- home_detail_link
	- photo_gallery
	- latitude
	- latitude
	- coordinates
	- year_built
	- property_size
	- home_size
	- bathrooms
	- bedrooms
	- home_info
	- year_updated
	- floors
	- basement
	- roof
	- view
	- heating_sources
	- heating_system
	- rooms
	- neighborhood
	- school_district
'''
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults

ZILLOW_API_KEY = 'X1-ZWz19sbb9f7k7f_40oka'

def get_property_info(address, zipcode):
	if address and zipcode:
		zillow_data = ZillowWrapper(ZILLOW_API_KEY)
		deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
		result = GetDeepSearchResults(deep_search_response)
		return result

if __name__ == '__main__':
	# sample use case
	address = '53 Scottsville Road'
	zipcode = '14611'
	property_object = get_property_info(address, zipcode)
	print property_object