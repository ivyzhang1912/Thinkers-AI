import os

def read_dir(path):
    fileArray = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            eachpath = str(root+'/'+fn)
            fileArray.append(eachpath)
    return fileArray

def merge(path):
    with open('合并.txt', 'a') as fw:
        for i in read_dir(path):
            if '正文.txt' in i:
                txt = open(i).read()
                fw.write(txt)

if __name__ == '__main__':
    merge('/Users/zhangduola/Desktop/《中国思想家评传》/《中国思想家评传》文本提取/《中国思想家评传》系列丛书_正文及注释')
