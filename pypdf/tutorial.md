

# 用Python为PDF添加目录

## **1 起因**

我们在网络上找的PDF，通常会遇到很多扫描版的，而且大多没有目录，手动添加效率太低所以试着找资料做了个脚本，目前功能比较单一，目录可以采用OCR或者书籍商城爬取。然后手动修改调整。(使用EverEdit修改)

## **2 安装**

使用 pip 用以下命令就可以装上了（Anaconda 上也有）。

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pymupdf
```

或者在 conda 环境下执行上面的命令安装（建议在 conda 下用 pip 安装）

## 3 导入模块

导入模块，并显示版本信息。

```python
>>> import fitz
>>> print(fitz.__doc__)
PyMuPDF 1.17.1: Python bindings for the MuPDF 1.17.0 library.
Version date: 2020-06-13 07:54:31.
Built for Python 3.7 on win32 (64-bit).
```

## 3 **完整示例代码及效果**

```python
import fitz
doc = fitz.open('test.pdf') 
toc = doc.getToC() 
toc.clear()
toc.append([1, '目录', 1]) # 修改 toc
doc.setToC(toc) # 替换 PDF 目录
doc.save('new.pdf') # 保存修改后的 PDF 文档为 new.pdf
```

## **4 打开/保存 PDF 文件**

首先引入 PyMuPDF 包：

```python
import fitz
```

我们可以用 `open()` 打开当前目录下的一个 PDF 文件。

```python
doc = fitz.open('test.pdf')
```

这个 `doc` 变量是 `Document` 类，可以通过它获得/修改 PDF 文件的很多参数。比如 `doc.pageCount` 为 PDF 总页数，`doc.metadata` 包含文档的名称、作者等各种属性。

但对 `doc` 所做的这些修改是不会自动保存到文件上的。 要保存修改，可调用 `save()` 将修改后的内容保存为文件：

```text
doc.save('new.pdf')
```

## 5 [文档](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#document)的部分方法和属性

| **方法/属性**                                                | **描述**  (类型)                                             |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| [`Document.pageCount`](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#Document.pageCount) | 页数（*int*）                                                |
| [`Document.metadata`](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#Document.metadata) | 元数据（*dict*）                                             |
| [`Document.getToC()`](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#Document.getToC) | 获取目录（*list*）                                           |
| [`Document.loadPage()`](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#Document.loadPage) | 阅读[页面](https://pymupdf.readthedocs.io/en/latest/page/&usg=ALkJrhhBc6SCGxi0eli-bwKefP3NjdzVnw#page) |

## 6 访问元数据

PyMuPDF完全支持标准元数据。[`Document.metadata`](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#Document.metadata)是具有以下键的Python字典。它适用于**所有文档类型**，尽管并非所有条目都可能始终包含数据。有关其含义和格式的详细信息，请参阅相应的手册，例如[Adobe PDF Reference](https://pymupdf.readthedocs.io/en/latest/app4/&usg=ALkJrhiRtby1NrKdERGlgx24jccHSv4HAQ#adobemanual) for PDF。更多信息也可以在[文档](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#document)章节中找到。

| **键**       | **值**                      |
| :----------- | :-------------------------- |
| producer     | 生产商（生产软件）          |
| format       | 格式：“ PDF-1.4”，“ EPUB”等 |
| encryption   | 加密方式（如果有）          |
| author       | 作者                        |
| modDate      | 最后修改日期                |
| keywords     | 关键字                      |
| title        | 标题                        |
| creationDate | 创建日期                    |
| creator      | 创建应用                    |
| subject      | 主题                        |

## **7 获得/修改 PDF 目录大纲**

在打开 PDF 文件后，可以用 `getToC()` 获取 PDF 目录：

```text
toc = doc.getToC()
```

`toc` 变量是一个序列，其中每个元素都是一个三维**序列**：`[lvl, title, page]` 。

其中 `lvl` 表示目录项的层级数目(从1开始)，即可以有一级目录、二级目录等，`title` 表示目录项的标题，`page` 为目录项链接的页数(从1开始)。

我们可以直接修改 `toc` 变量，最后用 `doc.setToC(toc)` 来替换原来的目录。同样这个修改不会自动保存到文件。

在添加目录时请**注意目录项在 `toc` 序列中的顺序**，生成的 PDF 中目录严格按照 `toc` 中的顺序排列，而不会根据链接页码排序。

## 8 使用页面

[Page](https://pymupdf.readthedocs.io/en/latest/page/&usg=ALkJrhhBc6SCGxi0eli-bwKefP3NjdzVnw#page)-页面处理是MuPDF功能的核心。

- 您可以将页面渲染为光栅或矢量（SVG）图像，可以选择缩放，旋转，移动或剪切页面。
- 您可以提取多种格式的页面文本和图像，然后搜索文本字符串。
- 对于PDF文档，有许多其他方法可用于向页面添加文本或图像。

首先，必须创建一个页面[[Page](https://pymupdf.readthedocs.io/en/latest/page/&usg=ALkJrhhBc6SCGxi0eli-bwKefP3NjdzVnw#page)]。这是文档[[Document](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#document)]的一种方法：

```python
# 加载文档的页码“pno”（从0开始）
page = doc.loadPage(pno)  
# 缩写
page = doc[pno]  
```

在这里，*pno*是介于*-inf~pageCount*的任何整数。负数从末尾开始倒数，因此*doc [-1]*是最后一页，与Python列表一样。

一些更高级的方法是使用文档作为页面的循环：

```python
for page in doc:
    # do something with 'page'

# ... 或反向读
for page in reversed(doc):
    # do something with 'page'

# ... 或使用切片 'slicing'
for page in doc.pages(start, stop, step):
    # do something with 'page'
```

拥有页面后，通常会执行以下操作：

## 9 检查页面的链接，注释或表单字段

使用某些查看器软件显示文档时，链接显示为“热点区域”。如果在光标显示手形符号的情况下单击，你将会打开该链接的网页。以下是获取所有链接的方法：

```python
# 获取页面上的所有链接
links = page.getLinks()
```

*links*是字典的Python列表。有关详细信息，请参见[`Page.getLinks()`](https://pymupdf.readthedocs.io/en/latest/page/&usg=ALkJrhhBc6SCGxi0eli-bwKefP3NjdzVnw#Page.getLinks)。

您还可以使用 每次发出一个链接的循环[也叫迭代器]：

```
for link in page.links():
    # do something with 'link'
```

如果处理PDF文档页面，则可能还存在注释（[Annot](https://pymupdf.readthedocs.io/en/latest/annot/&usg=ALkJrhgNdu1C_aCkQDufeh7o4FnESsLDbg#annot)）或表单字段（[Widget](https://pymupdf.readthedocs.io/en/latest/widget/&usg=ALkJrhgoFoW4kx8SB66mHk-IjTPqYgTC0w#widget)），每个注释都有自己的循环：

```
for annot in page.annots():
    # do something with 'annot'

for field in page.widgets():
    # do something with 'field'
```

## 10 呈现页面

本示例创建页面内容的**光栅**图像：

```
pix = page.getPixmap()
```

*pix*是一个[Pixmap](https://pymupdf.readthedocs.io/en/latest/pixmap/&usg=ALkJrhjoQxC6qjVVOBvJFkf9FahV0ABvhg#pixmap)对象（在本例中）包含页面的**RGB**图像，可以用于多种用途。方法[`Page.getPixmap()`](https://pymupdf.readthedocs.io/en/latest/page/&usg=ALkJrhhBc6SCGxi0eli-bwKefP3NjdzVnw#Page.getPixmap)提供了多种控制图像的方法：分辨率，色彩空间（例如，生成灰度图像或具有减色方案的图像），透明度，旋转，镜像，偏移，剪切等。例如：创建**RGBA**图像（即包含Alpha通道），请指定*pix = page.getPixmap（alpha = True）*。

一个像素图[[Pixmap](https://pymupdf.readthedocs.io/en/latest/pixmap/&usg=ALkJrhjoQxC6qjVVOBvJFkf9FahV0ABvhg#pixmap)]包含了许多方法和属性，这些方法和属性在下面引用。其中有宽度width、高度height(以像素为单位)和步长stride(一条水平图像线的字节数)。属性样本sample表示图像数据(Python bytes对象)的矩形字节区域。

<!--注意-->

您还可以使用[`Page.getSVGimage()`](https://pymupdf.readthedocs.io/en/latest/page/&usg=ALkJrhhBc6SCGxi0eli-bwKefP3NjdzVnw#Page.getSVGimage)创建页面的矢量图像。有关详细[信息](https://github.com/pymupdf/PyMuPDF/wiki/Vector-Image-Support&usg=ALkJrhgC1Foerg5dNAx8XD4WSoGGkXOHiw)，请参阅此[Wiki](https://github.com/pymupdf/PyMuPDF/wiki/Vector-Image-Support&usg=ALkJrhgC1Foerg5dNAx8XD4WSoGGkXOHiw)。

## 11 将页面图像保存到文件中

我们可以容易地将图像存储在PNG文件中：

```python
pix.writeImage("page-%i.png" % page.number)
```

## 12 提取文本和图像

我们还可以以许多不同的形式和详细程度提取页面的所有文本，图像和其他信息：

```
text = page.getText(opt)
```

使用以下字符串之一来*选择*获取不同的格式[[2\]](https://pymupdf.readthedocs.io/en/latest/tutorial/&usg=ALkJrhj46Gz7G5r1qx3xyPSkKur5c87nfg#f2)：

- *“text”*：（默认）带换行符的纯文本。没有格式，没有文本位置细节，没有图像。
- *“bolcks”*：生成文本块（=段落）列表。
- *“words”*：生成单词列表（不包含空格的字符串）。
- *“ html”*：创建页面的完整视觉版本，包括所有图像。这可以在您的Internet浏览器中显示。
- *“ dict”* / *“ json”*：与HTML相同的信息级别，但作为Python字典或resp提供。JSON字符串。见[`TextPage.extractDICT()`](https://pymupdf.readthedocs.io/en/latest/textpage/&usg=ALkJrhheUIJqWdyGby6eRQTwXVPgceF54Q#TextPage.extractDICT)RESP。[`TextPage.extractJSON()`](https://pymupdf.readthedocs.io/en/latest/textpage/&usg=ALkJrhheUIJqWdyGby6eRQTwXVPgceF54Q#TextPage.extractJSON)有关其结构的详细信息。
- *“ rawdict”*：的超集[`TextPage.extractDICT()`](https://pymupdf.readthedocs.io/en/latest/textpage/&usg=ALkJrhheUIJqWdyGby6eRQTwXVPgceF54Q#TextPage.extractDICT)。此外，它还提供字符详细信息，如XML。有关[`TextPage.extractRAWDICT()`](https://pymupdf.readthedocs.io/en/latest/textpage/&usg=ALkJrhheUIJqWdyGby6eRQTwXVPgceF54Q#TextPage.extractRAWDICT)其结构的详细信息，请参见。
- *“ xhtml”*：文本信息级别，为TEXT版本，但包含图像。也可以通过Internet浏览器显示。
- *“ xml”*：不包含图像，但包含每个单个文本字符的完整位置和字体信息。使用XML模块进行解释。

为了让您对这些替代方案的输出有一个了解，我们提供了文本示例摘录。请参阅[附录2：有关文本提取的详细信息](https://pymupdf.readthedocs.io/en/latest/app2/&usg=ALkJrhjYdhzWc9XIfOhCgrhBgHci34zDvg#appendix2)。

## 13 [搜索文本](https://pymupdf.readthedocs.io/en/latest/tutorial/&usg=ALkJrhj46Gz7G5r1qx3xyPSkKur5c87nfg#searching-for-text)

您可以找出特定文本字符串在页面上的确切位置：

```
areas = page.searchFor("mupdf", hit_max = 16)
```

这将提供多达16个矩形的列表（请参见[Rect](https://pymupdf.readthedocs.io/en/latest/rect/&usg=ALkJrhiUMXM4Ucndpn8gmAndTMTKl_b35w#rect)），每个[矩形](https://pymupdf.readthedocs.io/en/latest/rect/&usg=ALkJrhiUMXM4Ucndpn8gmAndTMTKl_b35w#rect)都包含一个字符串“ mupdf”（不区分大小写）。您可以使用此信息来突出显示这些区域（仅PDF）或创建文档的交叉引用。

也请[参阅“一起工作：DisplayList和TextPage”](https://pymupdf.readthedocs.io/en/latest/coop_low/&usg=ALkJrhinqQcKZEKcJyR_MK6DVeXkCZOtxw#cooperation)一章[，](https://pymupdf.readthedocs.io/en/latest/coop_low/&usg=ALkJrhinqQcKZEKcJyR_MK6DVeXkCZOtxw#cooperation)以及演示程序[demo.py](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/demo/demo.py&usg=ALkJrhgt6PKkYG-AkBOQOXbI2N1C-foLUA)和[demo-lowlevel.py](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/demo/demo-lowlevel.py&usg=ALkJrhiZFGAWPEVx18dbdv0F4Z0pnngnMQ)。除了其他内容外，它们还包含有关如何将[TextPage](https://pymupdf.readthedocs.io/en/latest/textpage/&usg=ALkJrhheUIJqWdyGby6eRQTwXVPgceF54Q#textpage)，[Device](https://pymupdf.readthedocs.io/en/latest/device/&usg=ALkJrhgaLNFXAcaO3lLMSFpH6Sw_kG51Rw#device)和[DisplayList](https://pymupdf.readthedocs.io/en/latest/displaylist/&usg=ALkJrhgJvpCv2cLRyu5-hHFXgowGvGO2Uw#displaylist)类用于更直接控制的详细信息，例如，出于性能方面的考虑。

## 14 PDF维护

PDF是唯一可以使用PyMuPDF **修改的**文档类型。其他文件类型是只读的。

但是，您可以将**任何文档**（包括图像）转换为PDF，然后将所有PyMuPDF功能应用于转换结果。在此处找到更多信息[`Document.convertToPDF()`](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#Document.convertToPDF)，并查看演示脚本[pdf-converter.py](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/demo/pdf-converter.py&usg=ALkJrhjG8Lh8ERtVOlrZIMwgCxqeAZIEzQ)，该脚本可以将任何受支持的文档转换为PDF。

[`Document.save()`](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#Document.save) 始终将PDF当前状态（可能已修改）存储在磁盘上。

通常，您可以选择是保存到新文件，还是将修改附加到现有文件上（“增量保存”），这通常会快得多。

下面介绍如何处理PDF文档。此描述绝不是完整的：更多内容可以在以下章节中找到。

## 15 修改，创建，重新整理和删除页面

有几种方法来操纵PDF 的所谓的**页面树**（一种描述所有页面的结构）：

[`Document.deletePage()`](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#Document.deletePage)并[`Document.deletePageRange()`](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#Document.deletePageRange)删除页面。

[`Document.copyPage()`](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#Document.copyPage)，[`Document.fullcopyPage()`](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#Document.fullcopyPage)然后[`Document.movePage()`](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#Document.movePage)将页面复制或移动到同一文档中的其他位置。

Document.select()将PDF缩小到所选页面。参数是要保留的页码的序列[3]。这些整数必须全部在0 <= i <pageCount范围内。执行后，此列表中所有缺少的页面将被删除。其余页面将按顺序出现，并按您指定的次数（！）进行。

因此，您可以轻松地使用

- 前10页或后10页，
- 仅奇数页或偶数页（用于双面打印），
- 该页面**做**或**不**包含给定文本，
- 反转页面顺序，…

…无论您想到什么。

保存的新文档将包含仍然有效的链接，注释和书签（指向所选页面或某些外部资源的链接）。

[`Document.insertPage()`](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#Document.insertPage)并[`Document.newPage()`](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#Document.newPage)插入新页面。

此外，页面本身可以通过多种方法（例如页面旋转，注释和链接维护，文本和图像插入）进行修改。

## 16 合并和分割PDF文档

方法[`Document.insertPDF()`](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#Document.insertPDF)在不同的PDF文档之间复制页面。这是一个简单的合并**示例（*doc1*和*doc2*是打开的PDF）：

```python
# 将整个doc2附加到doc1的末尾
doc1.insertPDF(doc2)
```

这是**分割** *doc1*的代码段。它会创建一个新文档，其前十页和后十页：

```python
doc2 = fitz.open()                 # 新的空PDF
doc2.insertPDF(doc1, to_page = 9)  # 前十页
doc2.insertPDF(doc1, from_page = len(doc1) - 10) # 后十页
doc2.save("first-and-last-10.pdf")
```

可以在“ [文档”](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#document)一章中找到更多[信息](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#document)。还可以看看[PDFjoiner.py](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/examples/PDFjoiner.py&usg=ALkJrhi7R0y0f417K-tMIybY2aUH9mHoow)。

## 17 嵌入数据

PDF可以用作任意数据（可执行文件，其他PDF，文本或二进制文件等）的容器，就像ZIP档案一样。

PyMuPDF通过[Document](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#document) *EmbeddedFile *方法和属性完全支持此功能。对于一些细节参考[附录3：嵌入式文件注意事项](https://pymupdf.readthedocs.io/en/latest/app3/&usg=ALkJrhjoIfSdOjupF-j_amCAs2NcRAVrbQ#appendix-3)，请查阅维基[嵌入文件](https://github.com/pymupdf/PyMuPDF/wiki/Dealing-with-Embedded-Files&usg=ALkJrhjuZYFKspEP1mh-lNCwumxT_xTXtw)，或示例脚本[embedded-copy.py](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/examples/embedded-copy.py&usg=ALkJrhiZL4c-GrB1MYJb1216-eLrB1Yliw)，[embedded-export.py](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/examples/embedded-export.py&usg=ALkJrhhOW5JQM1TNSaNQjnYLoggNT6mbkQ)，[embedded-import.py](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/examples/embedded-import.py&usg=ALkJrhgb9QXxMhwJFL2DTepLAkB46UfRXg)和[embedded-list.py](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/examples/embedded-list.py&usg=ALkJrhhPWXCOi-hA84nZZMa3gSBqz6n6KA)。

## 18 保存选项

如上所述，[`Document.save()`](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#Document.save)将**始终**将文档保存为当前状态。

通过指定选项incremental=True，可以将更改写回原始PDF。这个过程(通常)非常快，因为更改被附加到原始文件中，而不需要完全重写它。

[`Document.save()`](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#Document.save)选项与MuPDF的命令行实用程序*mutool clean的*选项相对应，请参见下表。

| **保存选项** | **mutool** | **效果**                                                     |
| :----------- | :--------- | :----------------------------------------------------------- |
| garbage= 1   | g          | 垃圾收集未使用的对象                                         |
| garbage= 2   | gg         | 除1外，[`xref`](https://pymupdf.readthedocs.io/en/latest/glossary/&usg=ALkJrhg0i68k50cekdaGZMuW59xVmiHpoA#xref)参数表 |
| garbage= 3   | gg         | 除2，合并重复的对象                                          |
| garbage= 4   | gggg       | 除3外，跳过重复的流                                          |
| clean= 1     | cs         | 清洁和消毒内容流                                             |
| deflate= 1   | z          | 压缩未压缩的流                                               |
| ascii = 1    | a          | 将二进制数据转换为ASCII格式                                  |
| linear= 1    | I          | 创建线性化的版本                                             |
| expand= 1    | i          | 解压缩图像                                                   |
| expand= 2    | f          | 解压缩字体                                                   |
| expand= 255  | d          | 解压全部                                                     |

例如，*mutool clean -ggggz file.pdf*产生出色的压缩结果。它对应于

*doc.save（filename，garbage= 4，deflate = 1）*。

## 19 结束

在程序继续执行的同时，通常需要“关闭”文档以将对基础文件的控制权交予OS。

这可以通过该[`Document.close()`](https://pymupdf.readthedocs.io/en/latest/document/&usg=ALkJrhh48ixS3bylIkQ6HLM_URzKw0Sbeg#Document.close)方法来实现。除了关闭基础文件之外，与文档关联的缓冲区也将被释放。



# 附录

## 从命令行获取文件名

```python
import sys, fitz  # import the binding
fname = sys.argv[1]  # get filename from command line
doc = fitz.open(fname)  # open document
```

## 将所有图片合并为pdf (或文件)

We show here **three scripts** that take a list of (image and other) files and put them all in one PDF.

**Method 1: Inserting Images as Pages**

The first one converts each image to a PDF page with the same dimensions. The result will be a PDF with one page per image. It will only work for supported image file formats:

```python
import os, fitz
import PySimpleGUI as psg  # for showing a progress bar
doc = fitz.open()  # PDF with the pictures
imgdir = "D:/2012_10_05"  # where the pics are
imglist = os.listdir(imgdir)  # list of them
imgcount = len(imglist)  # pic count

for i, f in enumerate(imglist):
    img = fitz.open(os.path.join(imgdir, f))  # open pic as document
    rect = img[0].rect  # pic dimension
    pdfbytes = img.convertToPDF()  # make a PDF stream
    img.close()  # no longer needed
    imgPDF = fitz.open("pdf", pdfbytes)  # open stream as PDF
    page = doc.newPage(width = rect.width,  # new page with ...
                       height = rect.height)  # pic dimension
    page.showPDFpage(rect, imgPDF, 0)  # image fills the page
    psg.EasyProgressMeter("Import Images",  # show our progress
        i+1, imgcount)

doc.save("all-my-pics.pdf")
```

This will generate a PDF only marginally larger than the combined pictures’ size. Some numbers on performance:

The above script needed about 1 minute on my machine for 149 pictures with a total size of 514 MB (and about the same resulting PDF size).

## 如何转换图片格式

| **Input Formats** | **Output Formats** | **Description**                  |
| :---------------- | :----------------- | :------------------------------- |
| BMP               | .                  | Windows Bitmap                   |
| JPEG              | .                  | Joint Photographic Experts Group |
| JXR               | .                  | JPEG Extended Range              |
| JPX               | .                  | JPEG 2000                        |
| GIF               | .                  | Graphics Interchange Format      |
| TIFF              | .                  | Tagged Image File Format         |
| PNG               | PNG                | Portable Network Graphics        |
| PNM               | PNM                | Portable Anymap                  |
| PGM               | PGM                | Portable Graymap                 |
| PBM               | PBM                | Portable Bitmap                  |
| PPM               | PPM                | Portable Pixmap                  |
| PAM               | PAM                | Portable Arbitrary Map           |
| .                 | PSD                | Adobe Photoshop Document         |
| .                 | PS                 | Adobe Postscript                 |

The general scheme is just the following two lines:

```python
pix = fitz.Pixmap("input.xxx")  # any supported input format
pix.writeImage("output.yyy")  # any supported output format
```

**Remarks**

1. The **input** argument of *fitz.Pixmap(arg)* can be a file or a bytes / io.BytesIO object containing an image.
2. Instead of an output **file**, you can also create a bytes object via *pix.getImageData(“yyy”)* and pass this around.
3. As a matter of course, input and output formats must be compatible in terms of colorspace and transparency. The *Pixmap* class has batteries included if adjustments are needed.

### 如何将图片添加到PDF

There are two methods to add images to a PDF page: [`Page.insertImage()`](https://pymupdf.readthedocs.io/en/latest/page/#Page.insertImage) and [`Page.showPDFpage()`](https://pymupdf.readthedocs.io/en/latest/page/#Page.showPDFpage). Both methods have things in common, but there also exist differences.

| **Criterion**                | [`Page.insertImage()`](https://pymupdf.readthedocs.io/en/latest/page/#Page.insertImage) | [`Page.showPDFpage()`](https://pymupdf.readthedocs.io/en/latest/page/#Page.showPDFpage) |
| :--------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| displayable content          | image file, image in memory, pixmap                          | PDF page                                                     |
| display resolution           | image resolution                                             | vectorized (except raster page content)                      |
| rotation                     | multiple of 90 degrees                                       | any angle                                                    |
| clipping                     | no (full image only)                                         | yes                                                          |
| keep aspect ratio            | yes (default option)                                         | yes (default option)                                         |
| transparency (water marking) | depends on image                                             | yes                                                          |
| location / placement         | scaled to fit target rectangle                               | scaled to fit target rectangle                               |
| performance                  | automatic prevention of duplicates; MD5 calculation on every execution | automatic prevention of duplicates; faster than [`Page.insertImage()`](https://pymupdf.readthedocs.io/en/latest/page/#Page.insertImage) |
| multi-page image support     | no                                                           | yes                                                          |
| ease of use                  | simple, intuitive; performance considerations apply for multiple insertions of same image | simple, intuitive; **usable for all document types** (including images!) after conversion to PDF via [`Document.convertToPDF()`](https://pymupdf.readthedocs.io/en/latest/document/#Document.convertToPDF) |

Basic code pattern for [`Page.insertImage()`](https://pymupdf.readthedocs.io/en/latest/page/#Page.insertImage). **Exactly one** of the parameters **filename / stream / pixmap** must be given:

```python
page.insertImage(
    rect,                  # where to place the image (rect-like)
    filename=None,         # image in a file
    stream=None,           # image in memory (bytes)
    pixmap=None,           # image from pixmap
    rotate=0,              # rotate (int, multiple of 90)
    keep_proportion=True,  # keep aspect ratio
    overlay=True,          # put in foreground
)
```

Basic code pattern for [`Page.showPDFpage()`](https://pymupdf.readthedocs.io/en/latest/page/#Page.showPDFpage). Source and target PDF must be different [Document](https://pymupdf.readthedocs.io/en/latest/document/#document) objects (but may be opened from the same file):

```python
page.showPDFpage(
    rect,                  # where to place the image (rect-like)
    src,                   # source PDF
    pno=0,                 # page number in source PDF
    clip=None,             # only display this area (rect-like)
    rotate=0,              # rotate (float, any value)
    keep_proportion=True,  # keep aspect ratio
    overlay=True,          # put in foreground
)
```

## 如何提取所有文本内容

This script will take a document filename and generate a text file from all of its text.

The document can be any supported type like PDF, XPS, etc.

The script works as a command line tool which expects the document filename supplied as a parameter. It generates one text file named “filename.txt” in the script directory. Text of pages is separated by a line “—–”:

```python
import sys, fitz
fname = sys.argv[1]  # get document filename
doc = fitz.open(fname)  # open document
out = open(fname + ".txt", "wb")  # open text output
for page in doc:  # iterate the document pages
    text = page.getText().encode("utf8")  # get plain text (is in UTF-8)
    out.write(text)  # write text of page
    out.write(bytes((12,)))  # write page delimiter (form feed 0x0C)
out.close()
```

The output will be plain text as it is coded in the document. No effort is made to prettify in any way. Specifally for PDF, this may mean output not in usual reading order, unexpected line breaks and so forth.

You have many options to cure this – see chapter [Appendix 2: Details on Text Extraction](https://pymupdf.readthedocs.io/en/latest/app2/#appendix2). Among them are:

1. Extract text in HTML format and store it as a HTML document, so it can be viewed in any browser.
2. Extract text as a list of text blocks via *Page.getText(“blocks”)*. Each item of this list contains position information for its text, which can be used to establish a convenient reading order.
3. Extract a list of single words via *Page.getText(“words”)*. Its items are words with position information. Use it to determine text contained in a given rectangle – see next section.

## 搜索和标记文本

There is a standard search function to search for arbitrary text on a page: [`Page.searchFor()`](https://pymupdf.readthedocs.io/en/latest/page/#Page.searchFor). It returns a list of [Rect](https://pymupdf.readthedocs.io/en/latest/rect/#rect) objects which surround a found occurrence. These rectangles can for example be used to automatically insert annotations which visibly mark the found text.

This method has advantages and drawbacks. Pros are

- the search string can contain blanks and wrap across lines
- upper or lower cases are treated equal
- return may also be a list of [Quad](https://pymupdf.readthedocs.io/en/latest/quad/#quad) objects to precisely locate text that is **not parallel** to either axis.

Disadvantages:

- you cannot determine the number of found items beforehand: if *hit_max* items are returned you do not know whether you have missed any.

But you have other options:

```python
import sys
import fitz

def mark_word(page, text):
    """Underline each word that contains 'text'.
    """
    found = 0
    wlist = page.getTextWords()        # make the word list
    for w in wlist:                    # scan through all words on page
        if text in w[4]:               # w[4] is the word's string
            found += 1                 # count
            r = fitz.Rect(w[:4])       # make rect from word bbox
            page.addUnderlineAnnot(r)  # underline
    return found

fname = sys.argv[1]                    # filename
text = sys.argv[2]                     # search string
doc = fitz.open(fname)

print("underlining words containing '%s' in document '%s'" % (word, doc.name))

new_doc = False                        # indicator if anything found at all

for page in doc:                       # scan through the pages
    found = mark_word(page, text)      # mark the page's words
    if found:                          # if anything found ...
        new_doc = True
        print("found '%s' %i times on page %i" % (text, found, page.number + 1))

if new_doc:
    doc.save("marked-" + doc.name)
```

This script uses [`Page.getTextWords()`](https://pymupdf.readthedocs.io/en/latest/functions/#Page.getTextWords) to look for a string, handed in via cli parameter. This method separates a page’s text into “words” using spaces and line breaks as delimiters. Therefore the words in this lists contain no spaces or line breaks. Further remarks:

- If found, the **complete word containing the string** is marked (underlined) – not only the search string.
- The search string may **not contain spaces** or other white space.
- As shown here, upper / lower cases are **respected**. But this can be changed by using the string method *lower()* (or even regular expressions) in function *mark_word*.
- There is **no upper limit**: all occurrences will be detected.
- You can use **anything** to mark the word: ‘Underline’, ‘Highlight’, ‘StrikeThrough’ or ‘Square’ annotations, etc.
- Here is an example snippet of a page of this manual, where “MuPDF” has been used as the search string. Note that all strings **containing “MuPDF”** have been completely underlined (not just the search string).

## 拆分单个页面

This deals with splitting up pages of a PDF in arbitrary pieces. For example, you may have a PDF with *Letter* format pages which you want to print with a magnification factor of four: each page is split up in 4 pieces which each go to a separate PDF page in *Letter* format again:

```python
"""
Create a PDF copy with split-up pages (posterize)
---------------------------------------------------
License: GNU GPL V3
(c) 2018 Jorj X. McKie

Usage
------
python posterize.py input.pdf

Result
-------
A file "poster-input.pdf" with 4 output pages for every input page.

Notes
-----
(1) Output file is chosen to have page dimensions of 1/4 of input.

(2) Easily adapt the example to make n pages per input, or decide per each
    input page or whatever.

Dependencies
------------
PyMuPDF 1.12.2 or later
"""
from __future__ import print_function
import fitz, sys
infile = sys.argv[1]  # input file name
src = fitz.open(infile)
doc = fitz.open()  # empty output PDF

for spage in src:  # for each page in input
    r = spage.rect  # input page rectangle
    d = fitz.Rect(spage.CropBoxPosition,  # CropBox displacement if not
                  spage.CropBoxPosition)  # starting at (0, 0)
    #--------------------------------------------------------------------------
    # example: cut input page into 2 x 2 parts
    #--------------------------------------------------------------------------
    r1 = r * 0.5  # top left rect
    r2 = r1 + (r1.width, 0, r1.width, 0)  # top right rect
    r3 = r1 + (0, r1.height, 0, r1.height)  # bottom left rect
    r4 = fitz.Rect(r1.br, r.br)  # bottom right rect
    rect_list = [r1, r2, r3, r4]  # put them in a list

    for rx in rect_list:  # run thru rect list
        rx += d  # add the CropBox displacement
        page = doc.newPage(-1,  # new output page with rx dimensions
                           width = rx.width,
                           height = rx.height)
        page.showPDFpage(
                page.rect,  # fill all new page with the image
                src,  # input document
                spage.number,  # input page number
                clip = rx,  # which part to use of input page
            )

# that's it, save output file
doc.save("poster-" + src.name,
         garbage = 3,                       # eliminate duplicate objects
         deflate = True)                    # compress stuff where possible
```

This shows what happens to an input page:

![../_images/img-posterize.png](https://pymupdf.readthedocs.io/en/latest/_images/img-posterize.png)



## 合并多个页面到一个

This deals with joining PDF pages to form a new PDF with pages each combining two or four original ones (also called “2-up”, “4-up”, etc.). This could be used to create booklets or thumbnail-like overviews:

```python
'''
Copy an input PDF to output combining every 4 pages
---------------------------------------------------
License: GNU GPL V3
(c) 2018 Jorj X. McKie

Usage
------
python 4up.py input.pdf

Result
-------
A file "4up-input.pdf" with 1 output page for every 4 input pages.

Notes
-----
(1) Output file is chosen to have A4 portrait pages. Input pages are scaled
    maintaining side proportions. Both can be changed, e.g. based on input
    page size. However, note that not all pages need to have the same size, etc.

(2) Easily adapt the example to combine just 2 pages (like for a booklet) or
    make the output page dimension dependent on input, or whatever.

Dependencies
-------------
PyMuPDF 1.12.1 or later
'''
from __future__ import print_function
import fitz, sys
infile = sys.argv[1]
src = fitz.open(infile)
doc = fitz.open()                      # empty output PDF

width, height = fitz.PaperSize("a4")   # A4 portrait output page format
r = fitz.Rect(0, 0, width, height)

# define the 4 rectangles per page
r1 = r * 0.5                           # top left rect
r2 = r1 + (r1.width, 0, r1.width, 0)   # top right
r3 = r1 + (0, r1.height, 0, r1.height) # bottom left
r4 = fitz.Rect(r1.br, r.br)            # bottom right

# put them in a list
r_tab = [r1, r2, r3, r4]

# now copy input pages to output
for spage in src:
    if spage.number % 4 == 0:           # create new output page
        page = doc.newPage(-1,
                      width = width,
                      height = height)
    # insert input page into the correct rectangle
    page.showPDFpage(r_tab[spage.number % 4],    # select output rect
                     src,               # input document
                     spage.number)      # input page number

# by all means, save new file using garbage collection and compression
doc.save("4up-" + infile, garbage = 3, deflate = True)
```

Example effect:

![../_images/img-4up.png](https://pymupdf.readthedocs.io/en/latest/_images/img-4up.png)



## 将任何文档转换为PDF

Here is a script that converts any PyMuPDF supported document to a PDF. These include XPS, EPUB, FB2, CBZ and all image formats, including multi-page TIFF images.

It features maintaining any metadata, table of contents and links contained in the source document:

```python
from __future__ import print_function
"""
Demo script: Convert input file to a PDF
-----------------------------------------
Intended for multi-page input files like XPS, EPUB etc.

Features:
---------
Recovery of table of contents and links of input file.
While this works well for bookmarks (outlines, table of contents),
links will only work if they are not of type "LINK_NAMED".
This link type is skipped by the script.

For XPS and EPUB input, internal links however **are** of type "LINK_NAMED".
Base library MuPDF does not resolve them to page numbers.

So, for anyone expert enough to know the internal structure of these
document types, can further interpret and resolve these link types.

Dependencies
--------------
PyMuPDF v1.14.0+
"""
import sys
import fitz
if not (list(map(int, fitz.VersionBind.split("."))) >= [1,14,0]):
    raise SystemExit("need PyMuPDF v1.14.0+")
fn = sys.argv[1]

print("Converting '%s' to '%s.pdf'" % (fn, fn))

doc = fitz.open(fn)

b = doc.convertToPDF()                      # convert to pdf
pdf = fitz.open("pdf", b)                   # open as pdf

toc= doc.getToC()                           # table of contents of input
pdf.setToC(toc)                             # simply set it for output
meta = doc.metadata                         # read and set metadata
if not meta["producer"]:
    meta["producer"] = "PyMuPDF v" + fitz.VersionBind

if not meta["creator"]:
    meta["creator"] = "PyMuPDF PDF converter"
meta["modDate"] = fitz.getPDFnow()
meta["creationDate"] = meta["modDate"]
pdf.setMetadata(meta)

# now process the links
link_cnti = 0
link_skip = 0
for pinput in doc:                # iterate through input pages
    links = pinput.getLinks()     # get list of links
    link_cnti += len(links)       # count how many
    pout = pdf[pinput.number]     # read corresp. output page
    for l in links:               # iterate though the links
        if l["kind"] == fitz.LINK_NAMED:    # we do not handle named links
            print("named link page", pinput.number, l)
            link_skip += 1        # count them
            continue
        pout.insertLink(l)        # simply output the others

# save the conversion result
pdf.save(fn + ".pdf", garbage=4, deflate=True)
# say how many named links we skipped
if link_cnti > 0:
    print("Skipped %i named links of a total of %i in input." % (link_skip, link_cnti))
```

## PDF加密

Starting with version 1.16.0, PDF decryption and encryption (using passwords) are fully supported. You can do the following:

- Check whether a document is password protected / (still) encrypted ([`Document.needsPass`](https://pymupdf.readthedocs.io/en/latest/document/#Document.needsPass), [`Document.isEncrypted`](https://pymupdf.readthedocs.io/en/latest/document/#Document.isEncrypted)).

- Gain access authorization to a document ([`Document.authenticate()`](https://pymupdf.readthedocs.io/en/latest/document/#Document.authenticate)).

- Set encryption details for PDF files using [`Document.save()`](https://pymupdf.readthedocs.io/en/latest/document/#Document.save) or [`Document.write()`](https://pymupdf.readthedocs.io/en/latest/document/#Document.write) and

  > - decrypt or encrypt the content
  > - set password(s)
  > - set the encryption method
  > - set permission details

Note

A PDF document may have two different passwords:

- The **owner password** provides full access rights, including changing passwords, encryption method, or permission detail.
- The **user password** provides access to document content according to the established permission details. If present, opening the PDF in a viewer will require providing it.

Method [`Document.authenticate()`](https://pymupdf.readthedocs.io/en/latest/document/#Document.authenticate) will automatically establish access rights according to the password used.

The following snippet creates a new PDF and encrypts it with separate user and owner passwords. Permissions are granted to print, copy and annotate, but no changes are allowed to someone authenticating with the user password:

```python
import fitz

text = "some secret information"  # keep this data secret
perm = int(
    fitz.PDF_PERM_ACCESSIBILITY  # always use this
    | fitz.PDF_PERM_PRINT  # permit printing
    | fitz.PDF_PERM_COPY  # permit copying
    | fitz.PDF_PERM_ANNOTATE  # permit annotations
)
owner_pass = "owner"  # owner password
user_pass = "user"  # user password
encrypt_meth = fitz.PDF_ENCRYPT_AES_256  # strongest algorithm
doc = fitz.open()  # empty pdf
page = doc.newPage()  # empty page
page.insertText((50, 72), text)  # insert the data
doc.save(
    "secret.pdf",
    encryption=encrypt_meth,  # set the encryption method
    owner_pw=owner_pass,  # set the owner password
    user_pw=user_pass,  # set the user password
    permissions=perm,  # set permissions
)
```

Opening this document with some viewer (Nitro Reader 5) reflects these settings:

[![../_images/img-encrypting.jpg](https://pymupdf.readthedocs.io/en/latest/_images/img-encrypting.jpg)](https://pymupdf.readthedocs.io/en/latest/_images/img-encrypting.jpg)

**Decrypting** will automatically happen on save as before when no encryption parameters are provided.

To **keep the encryption method** of a PDF save it using *encryption=fitz.PDF_ENCRYPT_KEEP*. If *doc.can_save_incrementally() == True*, an incremental save is also possible.

To **change the encryption method** specify the full range of options above (encryption, owner_pw, user_pw, permissions). An incremental save is **not possible** in this case.

## 访问PDF目录

This is a central (“root”) object of a PDF. It serves as a starting point to reach important other objects and it also contains some global options for the PDF:

```bash
>>> import fitz
>>> doc=fitz.open("PyMuPDF.pdf")
>>> cat = doc._getPDFroot()            # get xref of the /Catalog
>>> print(doc.xrefObject(cat))     # print object definition
<<
    /Type/Catalog                 % object type
    /Pages 3593 0 R               % points to page tree
    /OpenAction 225 0 R           % action to perform on open
    /Names 3832 0 R               % points to global names tree
    /PageMode /UseOutlines        % initially show the TOC
    /PageLabels<</Nums[0<</S/D>>2<</S/r>>8<</S/D>>]>> % names given to pages
    /Outlines 3835 0 R            % points to outline tree
>>
```

Note

Indentation, line breaks and comments are inserted here for clarification purposes only and will not normally appear. For more information on the PDF catalog see section 3.6.1 on page 137 of the [Adobe PDF References](https://pymupdf.readthedocs.io/en/latest/app4/#adobemanual).