import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os
import concurrent.futures

headers={
	'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}
url='https://onehu.xyz/categories/'

response=requests.get(url,headers=headers)
# print(response.text)
page=BeautifulSoup(response.text,'html.parser')
div_list=page.find_all('div',class_='category row nomargin-x')

category_g10_list=[]
other_list=[]
print('获取类别....')
for div in tqdm(div_list):
	a_list=div.find_all('a',class_='list-group-item list-group-item-action')
	category_name=div.find('a',role='tab')['title']
	if a_list[-1].find('span').text == 'More...':
		# print(div)
		category_g10_list.append([category_name,a_list[-1]['href']])
	else:
		other_list.append([category_name]+[[a['title'],a['href']] for a in a_list])
print(category_g10_list)
print(other_list)

def recursion_get_chapter_list(url,):
	chapter_list=[]
	count=1
	while True:
		print(f'获取第{count}页')
		resp=requests.get(url,headers=headers)
		page=BeautifulSoup(resp.text,'html.parser')
		a_list=page.find_all('a',class_='list-group-item list-group-item-action')
		for a in a_list:
			chapter_list.append([a.find('div').text,a['href']])
		next_page=page.find('a',class_='extend next')
		if next_page==None:
			break
		else:
			url='https://onehu.xyz'+next_page['href']
		count+=1
	return chapter_list
def spider_task(category_name,chapter):
	chapter_name = chapter[0]
	chapter_url = 'https://onehu.xyz' + chapter[1]
	resp = requests.get(chapter_url, headers=headers)
	page = BeautifulSoup(resp.text, 'html.parser')
	p_list = page.find_all('p')
	content = chapter_name + '\n' + '\n'.join([p.text for p in p_list])
	with open(category_name + '/' + chapter_name + '.txt', 'w', encoding='utf-8') as f:
		f.write(content)
	print(chapter_name, '爬取成功')


print('获取大于10章的类别的章节....')
for g10 in category_g10_list[:1]:
	category_url='https://onehu.xyz'+g10[1]
	category_name=g10[0]
	print('类别：',category_name)
	print('链接：',category_url)
	os.makedirs(category_name, exist_ok=True)
	print('文件夹创建成功....')
	chapter_list=recursion_get_chapter_list(category_url)
	print(f'共有：{len(chapter_list)}章',)
	print('\n')
	print('开始爬取....')

	# 创建一个包含3个线程的线程池
	with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
		futures = [executor.submit(spider_task, category_name,chapter) for chapter in chapter_list]

	# break

print('获取小于10章的类别的章节....')
for other in other_list:
	category_name=other[0]
	os.makedirs(category_name, exist_ok=True)
	chapter_list=other[1:]
	with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
		futures = [executor.submit(spider_task, category_name, chapter) for chapter in chapter_list]
