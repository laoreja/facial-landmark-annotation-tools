# -*- coding: utf-8 -*-
"""
Created on Dec 28 2015

@author: Chenhao Zhang

Example:  python eye.py orl_faces/s1/
"""
import sys, os
from PIL import Image, ImageTk
import Tkinter as tk
import math

try:
    path = sys.argv[1]
except IndexError:
    print "Usage: python key_point.py <path-to-imgs>"
    sys.exit(1)

#path = '_30_Jul16_horse_face'
try:
    files = os.listdir(path)
except OSError:
    print "Unable to access the directory!"
files = [f for f in files if f[0]!='.' and not f.endswith('csv') and not f.endswith('txt')]

N_points = 7
point_now = 0
point_pos = [None for i in range(N_points)]
Buttons = []
#cnt = 0
#eye = [0,0]

path_parts = [split_part for split_part in os.path.split(path) if split_part != '']
image_folder_name = path_parts[-1]
print "image_folder_name: ", image_folder_name
canvas_path = os.path.join(path, '..', image_folder_name+'_canvas')
annotationPath = os.path.join(path, '..', image_folder_name+'_annotations')
if not os.path.exists(canvas_path):
    os.makedirs(canvas_path)
if not os.path.exists(annotationPath):
    os.makedirs(annotationPath)    

annotationInfo = ['TL ', 'BR ', 'LE ', 'RE ', 'NO ', 'LM ', 'RM ']

for a_file in files:
    out_name = a_file.split('.')[0]
    
    point_now = 0
    point_pos = [None for i in range(N_points)]
    Buttons = []
    
    try:
    #    img = Image.open(path+a_file)
        img = Image.open(open(os.path.join(path, a_file), 'rb'))
    except IOError:
        print "Unable to open image: " + path + a_file
        continue
        
    top = tk.Tk()
    top.wm_title(a_file)
    
    resized = False
    resize_multiple = 1  
    size = img.size
    print "original size: ", size
    img_size = list(size)
    
    if size[0] > 1350 or size[1] > 850:
        print 'resized'
        resized = True
        resize_multiple = max([math.ceil(size[0]/1400.0), math.ceil(size[1]/900.0)])
        print 'resize multiple: ', resize_multiple
        img_size[0] = int(size[0] / resize_multiple)
        img_size[1] = int(size[1] / resize_multiple)
        img = img.resize(tuple(img_size), Image.ANTIALIAS)
        
    displayImage = ImageTk.PhotoImage(img)
    canvas = tk.Canvas(top, width=img_size[0], height=img_size[1])
    imagesprite = canvas.create_image(img_size[0]/2, img_size[1]/2, image=displayImage)    
    
    rect = [None for i in range(N_points)]
    bbox = None
    def reDraw(num):
        print "reDraw: ", annotationInfo[num]
        global rect
        global N_points
        global bbox
        if rect[num] != None:
            canvas.delete(rect[num])
            rect[num] = None
        if point_pos[num] != None:
            pt = point_pos[num]
            rect[num] = canvas.create_rectangle(pt[0]-2, pt[1]-2, pt[0]+2, pt[1]+2, fill="green")
        if num == 1 and rect[0] is not None:
            drawBBox()
        if num == 0 and rect[1] is not None:
            drawBBox()            
            
            
    def drawBBox():
        print 'drawBBox'
        global point_pos
        global bbox
        topLeft = point_pos[0]
        bottomRight = point_pos[1]
        if bbox != None:
            canvas.delete(bbox)
        bbox = canvas.create_rectangle(topLeft[0], topLeft[1], bottomRight[0], bottomRight[1], outline="blue")
            
    def clearPoint(num):
        print 'clear point: ', num
        global rect
        global bbox
        if rect[num] != None:
            canvas.delete(rect[num])
            rect[num] = None
        if bbox != None and (rect[0] == None or rect[1] == None):
            canvas.delete(bbox)
                   
        
    def getCoord(event):
        point_pos[point_now] = (event.x, event.y)
        reDraw(point_now)
    
        
    toolbox = tk.Toplevel()
    
    def btn1_c():
        global point_now
        point_now = 0
#        reDraw(point_now)
    btn1 = tk.Button(toolbox, text="Head top left(1)", command=btn1_c)
    Buttons.append(btn1)

    
    def btn2_c():
        global point_now
        point_now = 1
#        reDraw(point_now)
    btn2 = tk.Button(toolbox, text="Head bottom right(2)", command=btn2_c)
    Buttons.append(btn2)
    
    def btn3_c():
        global point_now
        point_now = 2   
#        reDraw(point_now)
    btn3 = tk.Button(toolbox, text="left eye(3)", command=btn3_c)
    Buttons.append(btn3)

    
    def btn4_c():
        global point_now
        point_now = 3  
#        reDraw(point_now)
    btn4 = tk.Button(toolbox, text="right eye(4)", command=btn4_c)
    Buttons.append(btn4)
    
    def btn5_c():
        global point_now
        point_now = 4 
#        reDraw(point_now)
    btn5 = tk.Button(toolbox, text="nose(5)", command=btn5_c)
    Buttons.append(btn5)
    
    
    def btn6_c():
        global point_now
        point_now = 5 
#        reDraw(point_now)
    btn6 = tk.Button(toolbox, text="left mouse(6)", command=btn6_c)
    Buttons.append(btn6)
    
    def btn7_c():
        global point_now
        point_now = 6 
#        reDraw(point_now)
    btn7 = tk.Button(toolbox, text="right mouse(7)", command=btn7_c)
    Buttons.append(btn7)
    
    
    def btn0_c():
        global point_pos
        point_pos[point_now] = None
        clearPoint(point_now)
    btn0 = tk.Button(toolbox, text="Clear this point(c)", command=btn0_c)
    Buttons.append(btn0)
    
    def btnx_c():
#        global point_pos
        print 'Next Image'
        canvas.postscript(file=os.path.join(canvas_path, out_name+".ps"), colormode='color')    
        top.destroy()
    btnx = tk.Button(toolbox, text="Next Image(n)", command=btnx_c)
    Buttons.append(btnx)
    

    btnd = tk.Button(toolbox, text="Draw Bbox(d)", command=drawBBox)
    Buttons.append(btnd)


    def key(event):
#        print "pressed", repr(event.char)
        if event.char == '1':
            btn1_c()
        elif event.char == '2':
            btn2_c()
        elif event.char == '3':
            btn3_c()
        elif event.char == '4':
            btn4_c()
        elif event.char == '5':
            btn5_c()
        elif event.char == '6':
            btn6_c()
        elif event.char == '7':
            btn7_c()
        elif event.char == 'c':
            btn0_c()
        elif event.char == 'n':
            btnx_c()
        elif event.char == 'd':
            drawBBox()
            
    
    for b in Buttons:
        b.pack()
    
    
    canvas.bind("<Button-1>",getCoord)
    canvas.bind("<Key>", key)    
    canvas.pack()
    
    canvas.focus_set()
    
    top.geometry('%dx%d+%d+%d' % (img_size[0], img_size[1], 150, 0))
    
    top.mainloop()
    
        
    fout = open(os.path.join(annotationPath, out_name+'.txt'), 'w')
    for i in range(N_points):
        if point_pos[i] != None:
            if resized:
                fout.write(annotationInfo[i]+str(int(point_pos[i][0]*resize_multiple))+" "+str(int(point_pos[i][1]*resize_multiple))+"\n")
            else:
                fout.write(annotationInfo[i]+str((point_pos[i][0]))+" "+str((point_pos[i][1]))+"\n")
        else:
            fout.write(annotationInfo[i]+"-1 -1"+"\n")
    fout.close()