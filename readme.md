# RemNote to Logseq

## 一、功能及说明

* **功能**：实现remnote笔记向logseq笔记转换。

* **说明**：logseq是一款开源的笔记工具，具有免费，关注用户隐私，支持双向链接等特点。如果你想将remnote中的笔记导入到logseq中，可以使用本程序。

## 二、使用介绍

* 转换仅支持remnote和logseq都具备的格式和功能。目前有：
  * 普通的page、block笔记
  * markdown语法
  * latex公式
  * 双向链接
  * 表格(table)
    * remnote中，table采用CSS样式生成，需要自己添加。
    * logseq中，table采用markdown语法。
    * 目前表格中支持latex语法和markdown语法。
  * 记忆卡片和记忆块
  * Todo （待办和已完成）
  * 图片 (会将remnote图床中的图片下载到本地)
    *  ~~在logseq中插入图片的时候可能会引用失效，猜测是和图片名有关系，目前没有解决~~
    * 遇到失效的情况建议手动将图片拖动到该处
* remnote特有格式及处理方法：
  * 高亮：会将高亮内容的两端加上 ***粗斜体***
  * 文件夹： remnote中的文件夹在logseq中体现为：含有对应**笔记链接**的**page**
  * kanban：因为logseq暂不支持kanban，会在kanban块前面加上 kanban 作为标识

## 三、文件说明

1. test中是从remnote中导出的各种测试rem.json文件（从开始简单的格式到含有比较复杂的格式）
2. remnoteToLogseq.md 文件含有编写程序中记录的各种信息及遇到的问题和解决方法
2. result.json文件是最终生成的文件，可以导入到logseq中

## 四、注意事项

1. 支持remnote整体导出
1. 打开的文件为你导出的rem.json文件(默认就是)
1. 程序中的download_img方法中的路径需要是你的logseq中存储图片的路径（logseq/assets/)