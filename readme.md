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
* remnote特有格式及处理方法：
  * 高亮：会在高亮内容的两端加上<highlight> </highlight>
  * 文件夹： remnote中的文件夹在logseq中体现为：含有对应**笔记链接**的**page**

## 三、注意事项

1. remnote必须以文件夹(folder）为单位导出（含有双向链接的page放在同一folder下同时导出）