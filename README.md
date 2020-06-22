# 用Python为扫描版的PDF添加目录

### 安装

```bash
>>> pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pymupdf
```

### 指令(先切换到指定目录)  

```bash
>>> python add.py test.pdf list.txt num
```

其中 `test.pdf `是待修改的pdf ,`list.txt`是目录文件,`num`是一个有符号整数，默认为0

### 说明

1. 路径文件可用`tab`补全

2. `list.txt` 文件说明

   ```
   # 目录可在各大图书网站爬取，并稍做修改，后续可能添加OCR和自动处理模块
   # 目录的每一行 包含三个元素 (以空格为间隔)
   # 第一个字符串(程序中转换为数字) 表示目录级别，如1表示一级标题，2表示二级标题
   # 第二个字符串 表示目录名 该版本仅支持中间没有空格的名称如 开 始 ，则程序可能出错
   # 第三个字符串表示 页码 (始于1)
   ```

3. `num`是一个用于抵消PDF页码和实际页码的整数。不加则默认为0，无符号则表是往后添加，'-'表是往前。





# Add contents to pdf using pymupdf

### Installation

```bash
>>> pip install pymupdf
```

### Command(first switch to the specified directory)

```bash
>>> python add.py test.pdf list.txt num
```

Where `test.pdf` is the pdf to be modified, `list.txt` is the catalog file, and `num` is a signed integer, the default is 0

### Description

1. The path file can be completed with `tab`

2. Description of `list.txt` file

   ```
   # The catalogue can be crawled on major book sites and modified slightly, and OCR and automatic processing modules may be added in the future.
   # Each line of the directory contains three elements (separated by spaces)
   # The first string (converted to numbers in the program) indicates the directory level, such as 1 for the first level heading and 2 for the second level heading.
   # The second string represents the directory name. This version only supports names without spaces in the middle.
   # The third string represents the page number (starting at 1).
   ```

3. `num` is an integer used to offset the PDF page number and the actual page number. If it is not added, the default is 0. If it is unsigned, the table is added backwards, and the'-' table is forwards.

