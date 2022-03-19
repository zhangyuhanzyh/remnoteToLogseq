#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import operator
#从rem.json 中读出数据
#提取需要的信息
#按照规定的格式写到logseq.json中


'''
读取rem.json文件
以字典的形式存储
获取主要的笔记信息，在docs中
'''
with open('rem3.json','r',encoding='utf-8') as file:
    remjson_dict = json.load(file)
#print(remjson_dict)

docs = remjson_dict['docs']  #list 876 元素是dict
#print(docs[0]['_id'])

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


for doc in docs:
    if not doc['_id'] in dicts:
        _id = doc['_id']
        flag[_id] = False #线默认不是page或folder
        key = doc['key']  #列表，存储的是节点内容
        #删除特殊的无用的节点
        if operator.eq(key,['Document']) | operator.eq(key,['Status'])| operator.eq(key,[{'i': 'q', '_id': 'WWor6M9ZxtgsAw69z'}])| operator.eq(key,['Draft']) | operator.eq(key,[{'i': 'q', '_id': 'xeu4icH3N4Drt3JSR'}]) :
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
            dicts[doc['_id']] = {'key':key,'children':children,'parent':parent}
        else:
            dicts[doc['_id']] = {'key': key, 'children': children}
        if "forceIsFolder" in doc:
            dicts[_id]['forceIsFolder'] = doc['forceIsFolder']
        #将节点存入到节点字典中后判断该节点类型
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
            block["string"] = '[[' + dicts[page_id]['key'][0]#page 引用
            block["children"] = []
            page['children'].append(block)
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
def create_node(_id):
    global dicts
    node = {}
    #print(page)
    node['string'] = ''
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
                    node['string'] = node['string'] + '((' + dicts[num['_id']]['key'][0] + '))'
    print('最终内容：',node['string'])
    children = []
    if dicts[_id]['children']:
        for childId in dicts[_id]['children']:
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