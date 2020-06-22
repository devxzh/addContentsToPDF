# -*- coding: UTF-8 -*-
# by devxzh@qq.com or onexzh@gmail.com
import fitz
import sys


def print_help():
    print("""
          Command is as follow:
          >>> python add.py test.pdf list.txt num
          where  'test.pdf' is the target file.
                 'list.txt' is the catalog file to be added.
                 'num' is an integer containing +/- ,the default is 0.
          """)


argc = len(sys.argv)  # Number of input parameters

if argc < 3:
    print_help()
    exit()
else:
    pdfName = sys.argv[1]  # pdf file name
    txtName = sys.argv[2]  # txt file name
    # Offset the deviation between the PDF page number and the actual page number
    offset = 0 if argc == 3 else int(sys.argv[3])

if '.pdf' in pdfName:
    try:
        doc = fitz.open(pdfName)
    except:
        print("Please check the pdf file name and try again!")
        exit()
else:
    print("source file must be .pdf !")
    exit()

toc = []  # doc.getToC()  # get contents

if '.txt' in txtName:
    try:
        contentFile = open(txtName, encoding='UTF-8', errors='ignore')
    except:
        print("Please check the txt file name and try again!")
        exit()

    lines = contentFile.readlines()  # get all lines

    for line in lines:  # get every line
        # Skip blank lines and comment lines
        if line[0] == '#' or len(line.split()) == 0:
            continue
        part = line.split()  # Split line into three elements
        toc.append([int(part[0]), str(part[1]), int(int(part[2]) + int(offset))])

    doc.setToC(toc)  # set contents
    newName = eval(repr(pdfName).replace("\\", "-"))  # Remove the '\' in the path
    partName = newName.split("-")
    newName = 'new-' + partName[-1]
    doc.save(newName)
    print("Added successfully!")

else:
    print("catalog file must be .txt !")
    exit()
