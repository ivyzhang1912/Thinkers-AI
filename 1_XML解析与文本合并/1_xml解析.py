from bs4 import BeautifulSoup
import os

# 获取path文件夹内的所有文件地址，返回列表
def read_dir(path):
    fileArray = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            eachpath = str(root+'/'+fn)
            fileArray.append(eachpath)
    return fileArray

def xml_extract(file, out_dir):
    # 读取xml文件并获取书名
    xml = open(file).read()
    soup = BeautifulSoup(xml, 'xml')
    book = soup.find('title').text
    # book = '智凯评传'

    # 解决部分文本处于para之外的情况
    search_tag = soup.find_all(['sect1', 'sect2', 'sect3'], recursive=True)

    for i in search_tag:
        direct_text_lis = i.find_all(text=True, recursive=False)
        direct_text_lis = [x.strip() for x in direct_text_lis if x.strip() != '']
        if direct_text_lis:
            for direct_text in direct_text_lis:
                alter_text = f'<para>{direct_text}</para>'
                xml = xml.replace(direct_text, alter_text)

    # 获取一个chapter下的父节点为note的文本和非note的文本
    # 创建两个空列表来存储不同情况下的<para>元素
    para_in_note = []
    para_not_in_note = []

    # 以一个chapter为例，遍历<chapter>下的所有<para>，对其进行分类，并对正文文本进行修改，去除其中note部分
    chapters = soup.find_all('chapter')
    for chapter in chapters:
        for para in chapter.find_all(['para', 'title']):
            # 检查<para>的父节点是否是<note>
            parent = para.find_parent()
            if parent and parent.name == "note":
                para_in_note.append(para.get_text(strip=True).strip())
            else:
                cnt = ''.join(para.find_all(text=True, recursive=False)).strip()
                if cnt:
                    para_not_in_note.append(cnt)
    # 写出
    with open(out_dir + '/' + book + '_注释.txt', 'x') as fw:
        for para in para_in_note:
            fw.write(para + '\n')

    with open(out_dir + '/' + book + '_正文.txt', 'x') as fw:
        for para in para_not_in_note:
            fw.write(para + '\n')
    print(book + ' is over\n')

def main():
    files = read_dir('/Users/zhangduola/Desktop/《中国思想家评传》/《中国思想家评传》文本提取/《中国思想家评传》系列丛书')
    xml_files = [i for i in files if '汉武帝.xml' in i]
    for file in xml_files:
        out_dir = '/Users/zhangduola/Desktop/《中国思想家评传》/《中国思想家评传》文本提取/《中国思想家评传》系列丛书_正文及注释/' + file.split('/')[-2]
        os.makedirs(out_dir)
        xml_extract(file, out_dir)
main()
