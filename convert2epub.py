'''
File : convert2epub.py.py
Auther : MHY
Created : 2024/10/30 19:02
Last Updated : 
Description : 
Version : 
'''
from ebooklib import epub
import os
def create_epub_from_txtFolders(dir_path):
	book = epub.EpubBook()
	book.set_title(dir_path)
	book.set_language('zh')
	book.add_author('MHY')
	# 添加封面图片
	cover_image_path = 'cover.png'
	cover_image = open(cover_image_path, 'rb').read()
	book.set_cover('cover.png', cover_image)
	toc = []
	spine = ['nav']
	chapter_num=1
	txts=os.listdir(dir_path)
	txts.sort(key=lambda x:int(x.split('.')[0]) if x.split('.')[0].isdigit() else 0)
	print(txts)
	for txt in txts:
		lines=open(os.path.join(dir_path,txt),'r',encoding='utf-8').readlines()
		chapter_title=lines[0].strip()
		article_content='<p>'+'</p><p>'.join([p for p in lines[1:]])+'</p>'
		c1 = epub.EpubHtml(title=f'{chapter_title}', file_name=f'chap_{chapter_num}.xhtml', lang='zh')
		c1.content = f'<h1>{chapter_title}</h1><p>{article_content}</p>'
		book.add_item(c1)

		toc.append(epub.Link(f'chap_{chapter_num}.xhtml', f'{chapter_num:04d} {chapter_title}', f'chap_{chapter_num}'), )
		spine.append(c1)
		chapter_num+=1

	book.add_item(epub.EpubNcx())
	book.add_item(epub.EpubNav())
	book.toc = toc
	book.spine = spine
	epub.write_epub(f'{dir_path}.epub', book, {})



folders=os.listdir('./')
folders = [item for item in folders if os.path.isdir(item)]
for folder in folders:
	create_epub_from_txtFolders(folder)
	# break




