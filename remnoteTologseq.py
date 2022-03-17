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
with open('rem1.json','r',encoding='utf-8') as file:
    remjson_dict = json.load(file)
#print(remjson_dict)

docs = remjson_dict['docs']  #list 876 元素是dict
#print(docs[0]['_id'])

'''
从docs存储的各节点中获取需要的笔记内容及其他信息
以_id为键值存在节点字典中
'''
dicts = {}
for doc in docs:
    if not doc['_id'] in dicts:
        _id = doc['_id']
        key = doc['key']  #列表，存储的是节点内容
        #删除特殊的无用的节点
        if operator.eq(key,['Document']) | operator.eq(key,['Status'])| operator.eq(key,[{'i': 'q', '_id': 'WWor6M9ZxtgsAw69z'}])| operator.eq(key,['Draft']) :
            continue
        #key_str = '' #列表内容拼接为字符串
        #keyStr = [str(i) for i in key]
        #print(key_str.join(keyStr))
        children = doc['children']  #列表，存储的是该节点的子节点_id
        parent = doc['parent']  # 字符串，存储的是节点的父节点_id
        dicts[doc['_id']] = {'key': key, 'children': children, 'parent': parent}
        #可能存在没有parent属性的情况
        # if 'parent' in doc:
        #     parent = doc['parent']  #字符串，存储的是节点的父节点_id
        #     dicts[doc['_id']] = {'key':key,'children':children,'parent':parent}
        # else:
        #     dicts[doc['_id']] = {'key': key, 'children': children}
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
title = list(dicts.values())[0]['key'][0]
print(title)
title_id = list(dicts.keys())[0]
print(title_id)
root_flag = True
'''
以笔记标题节点为根节点，将所有节点存储到lsq_dict中
用一个递归函数创造节点
'''
def create_node(child_id):
    global dicts
    node = {}
    #print(child_id)
    node['string'] = ''
    content = dicts[child_id]['key']#list
    #识别文本内容中的markdown内容 list元素只有两种情况 ：一个字符串  或  一个及以上 字典
    for num in content:
        if isinstance(num,str) & len(content) == 1:
            node['string'] = num
        elif isinstance(num,dict):
            print("markdown文本")
            #四种情况  b,l.u,i
            if 'b' in num:#加粗
                node['string'] =node['string'] + '**' + num['text'] + '**' + ' '
            elif 'l' in num:#斜体
                node['string'] = node['string'] + '***' + num['text'] + '***' + ' '
            elif 'u' in num:#下划线
                node['string'] = node['string'] + '<u>' + num['text'] + '</u>' + ' '
            else:#高亮
                node['string'] = node['string'] + '<highlight>' + num['text'] + '</highlight>' + ' '
            print(node['string'])
    children = []
    if dicts[child_id]['children']:
        for childId in dicts[child_id]['children']:
            children.append(create_node(childId))
    node['children'] = children
    return node

lsq_dict['title'] = title
lsq_dict['children'] = []
first_childs = dicts[title_id]['children']
if first_childs:#笔记有节点的话添加到dict['children']中
    for child_id in first_childs:
        if child_id in dicts.keys():
            lsq_dict['children'].append(create_node(child_id))

print(lsq_dict)

#logseq_roam.json可以识别的json都是[]中
lsq_list = [lsq_dict]

'''
保存到result.json文件中
编码！！！！
'''
json_file_path = 'result.json'
with open(json_file_path,mode='w',encoding='utf-8') as json_file:
    json.dump(lsq_list,json_file,ensure_ascii=False,indent=4)