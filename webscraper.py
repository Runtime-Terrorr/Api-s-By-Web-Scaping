from  bs4 import BeautifulSoup
import requests
import pandas as pd
url = "https://www.programmableweb.com/category/all/apis"
Api_count={}
i=0
while True:
	response = requests.get(url)
	data = response.text
	soup = BeautifulSoup(data , 'html.parser')
	tags = soup.find_all('td',{'class':'views-field views-field-pw-version-title'})
	categ = soup.find_all('td',{'class':'views-field views-field-field-article-primary-category'})
	apis= list(zip(tags,categ))
	for api in apis:
		api_name = api[0].text
		link = "https://www.programmableweb.com"+str(api[0].find('a').get('href'))
		decr_response = requests.get(link)
		decr_data = decr_response.text
		decr_soup = BeautifulSoup(decr_data,'html.parser')
		description_data= decr_soup.find("div",{'class':'api_description tabs-header_description'})
		description = description_data.text if description_data else 'N/A'
		category = api[1].text
		i +=1
		Api_count [i] =[api_name , category , link , description  ]
		if (i<10):
	    	
			print('\nApi Name : ' , api_name , '\nApi Category : ' ,category , '\nApi Link : ',link , '\nApi Decription : ' ,description ,'\nApi No. : ' ,i)
		else:
			break
		url_tag = soup.find('li',{'class':'pager-last'}).find('a').get('href')
		if url_tag :
			url = "https://www.programmableweb.com"+str(url_tag)
			
		else:
			break
Api_count_df= pd.DataFrame.from_dict(Api_count , orient='index' , columns=["Api Name" , "Api Category" , "Api Link" , "Api Description"])
print("Total Api : " , i)
Api_count_df=Api_count_df.to_csv('Api.csv')