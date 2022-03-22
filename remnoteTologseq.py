#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import operator
import random
import string

import urllib.request as request
import socket
import os

#从rem.json 中读出数据
#提取需要的信息
#按照规定的格式写到logseq.json中

'''
读取rem.json文件
以字典的形式存储
获取主要的笔记信息，在docs中
'''
with open('rem4.json','r',encoding='utf-8') as file:
    remjson_dict = json.load(file)
#print(remjson_dict)

docs = remjson_dict['docs']  #list 876 元素是dict
#print(docs[0]['_id'])
img_id = 1#图片编号
def download_img(img_url, api_token):
    print('===============================================================')
    global img_id

    # 为请求增加一下头
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
    headers = ('User-Agent', user_agent)
    opener = request.build_opener()
    opener.addheaders = [headers]
    request.install_opener(opener)
    try:
        img_name = "_img_1647951701034_0.png"
        filename = "D:\\Users\\86152\\Documents\\logseq\\assets\\" + str(img_id) + img_name
        img_id += 1
        pic = request.urlretrieve(img_url,filename)
        return '../assets/'+str(img_id-1) + img_name
    except Exception as e:
        print(Exception, ':', e)
        return "failed"
    #header = {"Authorization": "Bearer " + api_token} # 设置http header
    #request = urllib.request.Request(img_url, headers=header)
    # try:
    #     response = urllib.request.urlopen(request)
    #     img_name = "_img.png"
    #     filename = "D:\\Users\\86152\\Documents\\logseq\\assets\\"+ str(img_id) + img_name
    #     print('filenameeeeeeeeeeeeeeeeeeeeeeeee:',filename)
    #     img_id += 1
    #     if (response.getcode() == 200):
    #         with open(filename, "wb") as f:
    #             f.write(response.read()) # 将内容写入图片
    #         return filename
    # except:
    #     return "failed"


'''
从docs存储的各节点中获取需要的笔记内容及其他信息
以_id为键值存在节点字典中
'''
flag = {}
dicts = {}
#判断是page或folder或block
def judge(id):
    global dicts
    print('judge:',id)
    if "forceIsFolder" in dicts[id]:
        flag[id] = "folder"
        return
    #此处如果不以文件夹为单位导出，第一个就没有键值
    if flag[ dicts[id]['parent'] ] == "folder":
        flag[id] = "page"
        return
    flag[id] = 'block'

def create_uid():
    uid = ''
    uid = ''.join(random.sample(string.ascii_letters + string.digits,9))
    print('uid:',uid)
    return uid

Custom_css_id = '' #
Custom_css = {} #存储kanban、table等id
#获取rem中所有有用的信息
for doc in docs:
    if not doc['_id'] in dicts:
        _id = doc['_id']
        #flag[_id] = False #线默认不是page或folder
        key = doc['key']  #列表，存储的是节点内容
        #删除特殊的无用的节点
        if (operator.eq(key,['Document']) )| (operator.eq(key,['Status']))| (operator.eq(key,['Draft']))| ('rcrp' in doc.keys() ) |('spo' in doc.keys() ):
            continue
        if ('rcrt'in doc) and (doc['rcrt'] == 'w'):
            continue
        children = doc['children']  # 列表，存储的是该节点的子节点_id
        if (len(key) == 0 | len(children) ==0 ):#remnote中最后会有空节点
            continue
        #key_str = '' #列表内容拼接为字符串
        #keyStr = [str(i) for i in key]
        #print(key_str.join(keyStr))
        #parent = doc['parent']  # 字符串，存储的是节点的父节点_id
        #dicts[doc['_id']] = {'key': key, 'children': children, 'parent': parent}
        #可能存在没有parent属性的情况
        if 'parent' in doc:
            parent = doc['parent']  #字符串，存储的是节点的父节点_id
            if doc['parent'] == Custom_css_id:   #父节点是Custom_css_id的表明是样式块，不需要记录到dicts中
                if key[0] == 'kanban': #kanban 样式
                    Custom_css['kanban'] = _id
                    print('kanban:',Custom_css['kanban'])
                    continue
                if key[0] == 'column table  ': #表格样式
                    Custom_css['table'] = _id
                    print('table:', Custom_css['table'])
                    continue
            dicts[doc['_id']] = {'key': key, 'children': children, 'parent': parent}
        else:
            dicts[doc['_id']] = {'key': key, 'children': children}
        if "forceIsFolder" in doc:
            dicts[_id]['forceIsFolder'] = doc['forceIsFolder']
        #将节点存入到节点字典中后判断该节点类型
        #print(dicts[_id])

        if ('references' in doc.keys()) :#被引用过
            dicts[_id]['references'] = doc['references']
            dicts[_id]['uid'] = create_uid()
        if ('type' in doc) and (doc['type'] == 1):#记忆卡片或记忆块 (此处用and可以，短路逻辑，但&不行）
            dicts[_id]['type'] = doc['type']
            if('value' in doc):#记忆卡片
                dicts[_id]['value'] = doc['value']
                dicts[_id]['rmcard'] = 1
            else:
                dicts[_id]['rmblock'] = 1
        if ('rcrt' in doc) and (doc['rcrt'] == 'c'):#Custom CSS
            Custom_css_id = _id  #不用记录custom的信息，只用记录下id，在后面判断其他的样式即可
            continue
        if ('typeParents' in doc):
            if ('kanban' in Custom_css) and  (doc['typeParents'][0]== Custom_css['kanban']):
                dicts[_id]['css'] = 'kanban'
                print('kanban-----------------------------------')
            if ('table' in Custom_css) and (doc['typeParents'][0] == Custom_css['table']):
                dicts[_id]['css'] = 'table'
                print('table-----------------------------------')
        judge(_id)
#打印字典键值及内容
#print(len(dicts))
for key,value in dicts.items():
    print(key,'-----',value)

#print(list(dicts.values())[0]['key'])

'''
将存储在dicts中的笔记内容及信息按照logseq的json格式转存
'''
#logseq的json格式
lsq_dict = {}
folderr = list( dicts.values() )[0]['key'][0]
print('folder:',folderr)
folderr_id = list(dicts.keys())[0]
print('folderr_id:',folderr_id)
folder_flag = True
'''
floder 节点 创建一个page   --- 内容是当前folder下面的所有page的链接
lsq_list 中包含多个 lsq_dict (folder 中 包含多个 page)
每个lsq_dict对应一个page 存储
以每个page为根节点，将所有节点存储到一个lsq_dict中
用一个递归函数创造节点
'''

def create_folder(pages):
    global folderr_id
    page = {}
    page['title'] = dicts[folderr_id]['key'][0] #folder名字
    page['children'] = []
    for page_id in pages:
        if page_id in dicts.keys():
            block = {}
            print(dicts[page_id]['key'][0])
            block["string"] = '[[' + dicts[page_id]['key'][0] + ']]'#page 引用
            block["children"] = []
            page['children'].append(block)
    return page
#返回一个page(dict)
def create_page(page_id):
    global dicts
    page = {}
    page['title'] = dicts[page_id]['key'][0] #title
    page['children'] = [] #子block
    #当前page有 子块
    childs_id = dicts[page_id]['children']
    for child_id in childs_id:
        if child_id in dicts.keys():
            page['children'].append(create_node(child_id))
    return page


def create_table(_id):
    global dicts
    table_str = ''
    table_head = '|'
    line_num = 0
    for child in dicts[_id]['children']:
        table_head += dicts[child]['key'][0] + '|'
        if( len(dicts[child]['children']) != 0 ):#有孩子 表格内容
            line_num = max( len(dicts[child]['children']),line_num )
    table_head += '\n'#表头
    table_str += table_head
    #添加表格内容
    for i in range(line_num):#加上i行内容
        table_line = '|'
        for child in dicts[_id]['children']:
            grandson_id = dicts[child]['children'][i]
            table_line += dicts[grandson_id]['key'][0] + '|'
        table_line += '\n'
        table_str += table_line
    return table_str

#创建logseq中的节点
def create_node(_id):
    global dicts
    node = {}
    #print(page)
    node['string'] = ''
    if 'css' in dicts[_id]:#表格或者kanban
        if dicts[_id]['css'] == 'kanban':
            node['string'] += '<kanban>'
        if dicts[_id]['css'] == 'table':#table 比较难写
            node['string'] = create_table(_id)
            node['children'] = []
            return node
    if 'uid' in dicts[_id]:
        node['uid'] = dicts[_id]['uid']
    content = dicts[_id]['key']#list
    #识别文本内容中的markdown内容 list元素只有两种情况 ：一个字符串  或  一个及以上 字典
    for num in content:
        if isinstance(num,str) & len(content) == 1:
            node['string'] += num   ### 注意可能会被修改
        elif isinstance(num,dict):
            #print("特殊格式")
            print(num)
            #四种情况  b,l.u,i
            if 'b' in num:#加粗
                node['string'] =node['string'] + '**' + num['text'] + '**' + ' '
            elif 'l' in num:#斜体
                node['string'] = node['string'] + '*' + num['text'] + '*' + ' '
            elif 'u' in num:#下划线
                node['string'] = node['string'] + '<u>' + num['text'] + '</u>' + ' '
            elif 'h' in num:#高亮
                node['string'] = node['string'] + '<highlight>' + num['text'] + '</highlight>' + ' '
            elif 'type' in num :#latex
                node['string']  = node['string'] + '$' + num['text'] + '$' + ' '
            elif num['i'] == "q":#引用
                if (flag[num['_id']] == 'folder') | (flag[num['_id']] == 'page'): #该引用是floder或page
                    node['string'] = node['string'] + '[[' + dicts[num['_id']]['key'][0] + ']]'
                else :#块引用
                    print('块引用')
                    node['string'] = node['string'] + ' ((' + dicts[num['_id']]['uid'] + '))'
            elif 'url' in num:#图片
                img_url = num['url']
                api_token = "fklasjfljasdlkfjlasjflasjfljhasdljflsdjflkjsadljfljsda"
                filename = download_img(img_url, api_token)
                node['string'] += ' ![1_img.png](' + filename +')'
    if 'rmcard' in dicts[_id]:  # 记忆卡片
            node['string'] += '{{cloze' + dicts[_id]['value'][0] + '}} #card'
    if 'rmblock' in dicts[_id]: #记忆块
            node['string'] += ' #card'

    # if('references' in dicts[_id] ):
    #     node['uid'] = create_uid()
    #     print('node_uid:',node['uid'])
    print('最终内容：',node['string'])
    children = []
    if dicts[_id]['children']:
        for childId in dicts[_id]['children']:
            if childId in dicts.keys():
                children.append(create_node(childId))
    node['children'] = children
    return node


lsq_list = []
#lsq_dict['folderr'] = folderr
#lsq_dict['children'] = []
pages = dicts[folderr_id]['children'] #list ---存储各page的_id
if pages:#folder下面有page
    folder_page = create_folder(pages)#返回一个folder_page(dict)
    lsq_list.append(folder_page)
if pages:#有笔记page，创造page，返回一个dict
    for page in pages:
        if page in dicts.keys():#有的话创建一个笔记page（dict）
            print('page:',page)
            lsq_list.append(create_page(page))
            #lsq_dict['children'].append(create_node(page))

print(lsq_list)

#logseq_roam.json可以识别的json都是[]中


'''
保存到result.json文件中
编码！！！！
'''
json_file_path = 'result.json'
with open(json_file_path,mode='w',encoding='utf-8') as json_file:
    json.dump(lsq_list,json_file,ensure_ascii=False,indent=4)