---

---

## Remnote json 格式

{"key":[结点名称],"_id":"结点唯一标识编号"，"parent":"父节点编号"，"children":["子节点1编号","子节点2编号","子节点3编号","子节点1编号","子节点4编号","子节点5编号"]}

***

**观察得：**每存储一个节点都会将从根节点到该节点上的所有结点再存储一边，因此有很多重复的结点

***

**节点存储：**每个节点都是一个字典，有'key'--字符串 'owner'--字符串   'children'--列表 ‘parent’  字符串    **'_id'** 字符串  等关键字

- [ ] remnote文件夹page下会有两个多余的block:在用到这些信息的时候判断是否在节点字典中，不在的话删除即可



## Logseq json格式

字典列表 递归

title:""

children:[]

文件夹：

```json
"forceIsFolder": true,
"folderOpen": false
```



***

## 流程

~~获取到所有节点，以_id为键值，将所有的节点重新存储一遍~~

~~根据节点存储的关系，~~

从doc中获取需要的信息存储到dicts中

根据dicts中的信息，生成对应的logseq格式文件

### 2022.3.15 

将remnote 各节点 按照 字典的形式存储



***

~~python中可按照列表之列表存储树~~

**根据roam.json的格式用字典存储树**

{

​		'root' : ' '

​		'children' :[

​		]

}

***

## convert

**根据不同数据信息在remnote和logseq存储方式的不同进行转换**

1. ~~rem.json中节点的文本内容是按照list的格式存储的，list中特殊文本例如markdown格式会按照字典的形式存储~~在key中

   - markdown+highlight

     ```json
     {
     	"text": "加粗",
     	"b": true,
     	"i": "m"
     },
     	"  ",
     {
     	"text": "颜色",
     	"h": 4,
     	"i": "m"
     },
     斜体(l)   下划线(u)   高亮(h)
     ```

     

   - latex

     ```json
     {
     	"type": "latex",
     	"block": false,
     	"x": true,
     	"slateIdentifier": 0.25839282510572037,
     	"text": "W_{T}",
     	"i": "m"
     },
     ```

     

2. **笔记中的双向链接问题**    remnote中引用的标识是    ~~remnote中引用的时候会复制一份信息在json中~~

   *在remnote中块引用和文章引用写法一致*  ：

   ```json
   添加一个文章字典？（以_id为键值）
   在无文件夹的情况下："parent": null,
   ```

   ```json
   {
   	"_id": "指向块的id",
   	"i": "q"
   },
   ```

   - **底部有冗余的信息可删除**         

   ​                                                  

3. 记忆卡片

   ```json
   {
               "key": [
                   "记忆卡片"
               ],
               "owner": "62248bb18a6b8000163a8a5d",
               "children": [],
               "subBlocks": [],
               "portalsIn": [
                   "xeu4icH3N4Drt3JSR"
               ],
               "createdAt": 1647826030720,
               "u": 1647826043145,
               "_id": "by4zcoJk7Bz5Td47A",
               "parent": "xeu4icH3N4Drt3JSR",
               "enableBackSR": true,
               "efc": false,
               "type": 1,
               "value": [
                   "记忆卡片内容"
               ]
           },
   ```

   

4. 记忆块

   * **"type": 1,是记忆块和记忆卡片特有的键值 ，其中记忆卡片有value键值**
   * 记忆块的children就是记忆块内容
   
5. 图片

   ```json
   "key":[
       ""
       {
           "i": "i",
           "url": "https://remnote-user-data.s3.amazonaws.com/sWotX47hAPQsNAD-ckIBtNyqJz3wfr-			2kNTvYZWPeqSWVhQihg5f56gUaF4GxufVygUMNfiOuvGOdvD15qaA0fRDcxnhDXG9uAbj9478k5mBISpCJqHSSv9Odxs0ysar.png",
           "width": 764,
           "height": 306,
           "percent": 100,
           "loading": false
       },
   ]
   ```

   

6. table  ！！！！！！！

   * logseq 插入的图片文件名有要求  ***暂时没有解决***

     ```
     ![1_img.png](../assets/1_img_1647950501980_0.png)
     ![1_img.png](../assets/1_img_1_1647950072192_0.png)
     ![1_img.png](../assets/1_img_1_1647950072392_0.png)
     ![1_img.png](..\assets\1_img_1647950072192_0.png)
     
     ![1_img.png](../assets/1_img_1647951701037_0.png)  --手动修改的
     ![1_img.png](../assets/1_img_1647951701034_0.png)  --自动生成的
     ```

     

1. kanban

2. Custom CSS

   * 当使用table，kanban等css标签后，会有一个含有"rcrt": "c",的dict： 如下

     ```
       {
                 "key": [
                     "Custom CSS"
                 ],
                 "owner": "62248bb18a6b8000163a8a5d",
                 "children": [
                     "7KLYd4c87eADZ2rSn",
                     "rrgRecGy48hmWsc6k",
                     "vjLjqGHPwhq3afJHr"
                 ],
                 "subBlocks": [
                     "7KLYd4c87eADZ2rSn",
                     "vjLjqGHPwhq3afJHr",
                     "rrgRecGy48hmWsc6k"
                 ],
                 "portalsIn": [],
                 "createdAt": 1646562244502,
                 "n": 1,
                 "s": 1646886479774,
                 "u": 1646887576057,
                 "_id": "4yAmvvP2xFR3yPaSf",
                 "parent": null,
                 "rcrt": "c",
                 "docUpdated": 1646887576057,
                 "csb": {
                     "rrgRecGy48hmWsc6k": {
                         "rrgRecGy48hmWsc6k": [
                             "6ueb8E9a99zS4f4Kh",
                             "QpQenqb4s6v6WDxSm"
                         ]
                     },
                     "7KLYd4c87eADZ2rSn": {
                         "7KLYd4c87eADZ2rSn": true
                     }
                 }
             },
     ```

     

   * kanban、table 等属于Custom CSS的

     其中**看板**："parent": "4yAmvvP2xFR3yPaSf", 父亲是Custom CSS

     ```
             {
                 "_id": "7KLYd4c87eADZ2rSn",
                 "key": [
                     "kanban"
                 ],
                 "owner": "62248bb18a6b8000163a8a5d",
                 "children": [
                     "Wc8RAb822bDbXpgdG",
                     "hxJLWv5uRcuhzfAxD",
                     "gBWbRjvwtPe6DuRy5"
                 ],
                 "subBlocks": [
                     "Wc8RAb822bDbXpgdG"
                 ],
                 "portalsIn": [
                     "4yAmvvP2xFR3yPaSf"
                 ],
                 "createdAt": 1646886135547,
                 "u": 1647826504378,
                 "crt": {
                     "r": {
                         "s": {
                             "_id": "gBWbRjvwtPe6DuRy5",
                             "s": "H1",
                             "v": [
                                 {
                                     "i": "q",
                                     "_id": "5CFCGDjeDoXX9iZmq"
                                 }
                             ]
                         }
                     },
                     "t": {
                         "s": {
                             "_id": "hxJLWv5uRcuhzfAxD",
                             "s": "Unfinished",
                             "v": [
                                 {
                                     "i": "q",
                                     "_id": "FeYjyK35ToFrRrvtC"
                                 }
                             ]
                         }
                     }
                 },
                 "typeParents": [
                     "26qj7Q83HkHscZcFi",
                     "9v8idLoyn3t9RSARH"
                 ],
                 "excludedTypeParents": [],
                 "parent": "4yAmvvP2xFR3yPaSf",
                 "selectedInSearch": 6,
                 "searchAliases": [],
                 "typeChildren": [
                     "TaH6DvF7Fw9grDng8",
                     "5Gsq5kNkmnaZvznzY"
                 ],
                 "s": 1646886299504
             },
     ```

     **表格**："parent": "4yAmvvP2xFR3yPaSf",  父亲是Custom CSS

     ```
             {
                 "_id": "rrgRecGy48hmWsc6k",
                 "key": [
                     "column table  "
                 ],
                 "owner": "62248bb18a6b8000163a8a5d",
                 "children": [
                     "6ueb8E9a99zS4f4Kh",
                     "k6YomDArd3QN5sfwe",
                     "rti5hs3Em4Mobqfms",
                     "QpQenqb4s6v6WDxSm"
                 ],
                 "subBlocks": [
                     "QpQenqb4s6v6WDxSm",
                     "6ueb8E9a99zS4f4Kh"
                 ],
                 "portalsIn": [
                     "4yAmvvP2xFR3yPaSf"
                 ],
                 "createdAt": 1646801041266,
                 "s": 1646832363110,
                 "u": 1647826281106,
                 "crt": {
                     "r": {
                         "s": {
                             "_id": "rti5hs3Em4Mobqfms",
                             "s": "H1",
                             "v": [
                                 {
                                     "i": "q",
                                     "_id": "5CFCGDjeDoXX9iZmq"
                                 }
                             ]
                         }
                     },
                     "t": {
                         "s": {
                             "_id": "k6YomDArd3QN5sfwe",
                             "s": "Unfinished",
                             "v": [
                                 {
                                     "i": "q",
                                     "_id": "FeYjyK35ToFrRrvtC"
                                 }
                             ]
                         }
                     }
                 },
                 "typeParents": [
                     "26qj7Q83HkHscZcFi",
                     "9v8idLoyn3t9RSARH"
                 ],
                 "excludedTypeParents": [],
                 "parent": "4yAmvvP2xFR3yPaSf",
                 "selectedInSearch": 12,
                 "searchAliases": [],
                 "typeChildren": [
                     "QpQenqb4s6v6WDxSm",
                     "RjecgDMoCgmqwA4Cs",
                     "vG2dZMshQn7RNFKpf",
                     "Nqkic7pyFvxnfF8yF"
                 ],
                 "tcsp": [
                     "QpQenqb4s6v6WDxSm"
                 ],
                 "docUpdated": 1646827751965,
                 "preMigrationTypeChildren": [
                     "QpQenqb4s6v6WDxSm",
                     "RjecgDMoCgmqwA4Cs",
                     "CfH43q5LdyZvtRRxE",
                     "vG2dZMshQn7RNFKpf"
                 ]
             },
     ```

   * 当某一block采用了某些CSS的时候，他的typeParents便是这些CSS的_id 构成的list，如采用了kanban的某一block：

     ```
     "typeParents": [
                     "7KLYd4c87eADZ2rSn"
                 ],
     ```

     

### 文件夹下有文件夹

文件夹特有键值：

```json
"forceIsFolder": true,
```

主文件夹是个page，其中包含对子文件夹的引用





***

## 注意

#### 在remnote中，一次只能需要导出一个文件夹 

当某笔记中有其他笔记的引用的时候需要按照文件夹导出