## abstract

Remnote中的folder与page，page与block可以抽象为树中父节点与孩子节点的关系，又可以以dict的形式存储



***

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

获取到所有节点，以_id为键值，将所有的节点重新存储一遍

根据节点存储的关系，

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

     

2. **笔记中的双向链接问题**    remnote中引用的标识是：   （ ~~remnote中引用的时候会复制一份信息在json中~~）

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
   块引用的话：被引用的块会有reference键值
    "references": [
                   {
                       "q": "XkvNP5F7nxJBAAmYm",
                       "f": "key"
                   }
               ]
   ```

   - **冗余的信息需删除**   （references）

     - ```json
       无用的链接信息含有键值 'rcrp' 或 'spo'（且仅这些节点里含有）
       ```

       

   - ~~虽然是双向链接，但在logseq中只用在一边添加链接，另一边即可自己生成~~

   - page引用只用在page名外加[[]]即可  page名是唯一标识

   - block引用 不能(())加 block名  要生成一个 uid作为唯一标识 --- **当一个节点被别的节点引用时，需要一个uid**

     - ~~logseq中进行块引用时，((uid))  不起作用~~  ：与文本内容 添加空格


   

   记忆卡片问题

4. 



***

## 注意

#### 在remnote中，一次只能需要导出一个文件夹 

当某笔记中有其他笔记的引用的时候需要按照文件夹导出













文章引用---4693
文章笔记2引用---4175
块引用一级节点3  ---8995
块笔记二级节点3.3引用 ---   9367
文件夹引用  ---- 9605



