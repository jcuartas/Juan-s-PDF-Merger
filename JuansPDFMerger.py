#! /usr/bin/env python3

import os
import PyPDF2
import tkinter as tk
from tkinter import filedialog

fileName = []


def loadFiles():
    filex = True
    while filex:
        filex = addFile()


def addFile():   
    fName = filedialog.askopenfilename(title="File ",defaultextension=".pdf", filetypes =[("Portable Document Format","*.pdf")])
    if fName != "":
        fileName.append(fName)
        mylistbox.insert(tk.END, fName)
        return True
    else:
        return False

def delFile():
    try:
        index = mylistbox.curselection()[0]
        mylistbox.delete(index)
        del fileName[index]
    except:
        index = 0  
    
def extractName(route):
    ix = len(route) - 1 - route[::-1].index("/")
    ix += 1
    name = route[ix:]
    return name
    
def mergeFiles():
    pdfFile = []
    reader = []
    writer = PyPDF2.PdfFileWriter()
    mylistboxProgress.delete(0, tk.END)
    if mylistbox.size() > 1:
        for i in range(0, len(fileName)):
            #print(reader[i])
            pdfFile.append(open(fileName[i], 'rb'))
            reader.append(PyPDF2.PdfFileReader(pdfFile[i]))
            mylistboxProgress.insert(i, extractName(fileName[i]+" - Progress: " + str(((i+1)/len(fileName))*100)+" %"))
            
            for pageNum in range(reader[i].numPages):
                page = reader[i].getPage(pageNum)
                writer.addPage(page)
           #pdfFile[i].close()

        outputName = filedialog.asksaveasfile(title="Save As...", mode='a', defaultextension=".pdf", filetypes =[("Portable Document Format","*.pdf")])
        if outputName:
            outputFile = open(outputName.name, 'wb')
            writer.write(outputFile)
            outputFile.close()
            mylistboxProgress.insert(tk.END, "File saved as: "+outputName.name)
        else:
            mylistboxProgress.insert(tk.END, "File not saved")
        for i in range(0, len(pdfFile)):
            pdfFile[i].close()
    return

def upindex():
    try:
        index = mylistbox.curselection()[0]
        if index > 0:
            element0 = mylistbox.get(index)
            elementm1 = mylistbox.get(index - 1)
            mylistbox.delete(index)
            mylistbox.insert(index, elementm1)
            mylistbox.delete(index - 1)
            mylistbox.insert(index - 1, element0)
            mylistbox.activate(index - 1)
            mylistbox.selection_set(index - 1)
            mylistbox.selection_anchor(index - 1)
            listMove(fileName, index, "up")
    except:
        index = 0

def downindex():
    try:
        index = mylistbox.curselection()[0]
        if index < mylistbox.size() - 1:
            element0 = mylistbox.get(index)
            element1 = mylistbox.get(index + 1)
            mylistbox.delete(index + 1)
            mylistbox.insert(index + 1, element0)
            mylistbox.delete(index)
            mylistbox.insert(index, element1)
            mylistbox.activate(index + 1)
            mylistbox.selection_set(index + 1)
            mylistbox.selection_anchor(index + 1)
            listMove(fileName, index, "down")
    except:
        index = 0
        
def listMove(listStr, index, operation):
    if index > 0:
        if operation == "up":
            element0 = listStr[index]
            elementm1 = listStr[index-1]
            listStr[index] = elementm1
            listStr[index - 1] = element0
        elif operation == "down":
            element0 = listStr[index]
            element1 = listStr[index + 1]
            listStr[index] = element1
            listStr[index+1] = element0

root = tk.Tk()

root.title("Juan's PDF Merger")
root.geometry('800x360')
mylabel = tk.Label(root,text="Juan's PDF merger. Press 'start' button to choose the files you want to merge \rif you press 'cancel', you stop loading files.")
mybutton = tk.Button(root,text="Start", command=loadFiles)
mylistbox = tk.Listbox(root, width=500)
scrollbarH = tk.Scrollbar(mylistbox, orient=tk.HORIZONTAL)
scrollbarV = tk.Scrollbar(mylistbox, orient=tk.VERTICAL)
frame = tk.Frame(root)
mybuttonUp = tk.Button(frame, text="Up", command=upindex)
mybuttonDown = tk.Button(frame, text="Down", command=downindex)
mybuttonAdd = tk.Button(frame, text="Add", command=addFile)
mybuttonDelete = tk.Button(frame, text="Delete", command=delFile)
mybuttonMerge = tk.Button(frame, text="Merge", command=mergeFiles)
mylistboxProgress = tk.Listbox(root, width=500)
scrollbarPH = tk.Scrollbar(mylistboxProgress, orient=tk.HORIZONTAL)
scrollbarPV = tk.Scrollbar(mylistboxProgress, orient=tk.VERTICAL)
mylabel.pack()
mybutton.pack()
mylistbox.pack()
frame.pack(side=tk.TOP)
mybuttonUp.pack(side=tk.LEFT)
mybuttonDown.pack(side=tk.LEFT)
mybuttonAdd.pack(side=tk.LEFT)
mybuttonDelete.pack(side=tk.LEFT)
mybuttonMerge.pack(side = tk.LEFT)
mylistboxProgress.pack() 

#root.withdraw()

    
root.mainloop()
   
