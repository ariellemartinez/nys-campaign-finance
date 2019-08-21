from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup

# Create your views here.

def contributions(request, category_in, year, zip_code_3):
	url = "http://www.elections.state.ny.us:8080/plsql_browser/CONTRIBUTORC_COUNTY?CATEGORY_IN=" + category_in + "&OFFICE_IN=ALL&county_IN=ALL&date_from=01%2F01%2F" + str(year) + "&date_to=12%2F31%2F" + str(year) + "&AMOUNT_from=.99&AMOUNT_to=999999999.99&ZIP1=" + str(zip_code_3) + "00&ZIP2=" + str(zip_code_3) + "99&ORDERBY_IN=N"
	webpage_response = requests.get(url)
	webpage = webpage_response.content
	soup = BeautifulSoup(webpage, "html.parser")
	all_tables = soup.find_all('table')
	right_table = all_tables[1]
	right_table_rows = right_table.find_all('tr')
	right_table_header_tags = right_table_rows[0].find_all('th')
	right_table_headers = []
	for header_tag in right_table_header_tags:
		right_table_headers.append(header_tag.get_text())
	table_list =[]
	for row in right_table_rows:
		row_data_tags = row.find_all('td')
		row_link = ""
		for a_tag in row.find_all('a'):
			row_a_href = a_tag.get('href')
			row_link = "http://www.elections.state.ny.us:8080" + row_a_href
		row_data = []
		for data_tag in row_data_tags:
			row_data.append(data_tag.get_text(', ').strip())
		row_zip = zip(right_table_headers, row_data)
		row_dictionary = {key:value for key, value in row_zip}
		row_dictionary['Link'] = row_link
		table_list.append(row_dictionary)
	table_list.pop(0)
	table_list.pop()
	table_data = {'results': table_list}
	response = JsonResponse(table_data)
	return response