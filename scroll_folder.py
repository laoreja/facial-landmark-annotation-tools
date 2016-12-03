#!/usr/bin/python
import Tkinter as tk
from PIL import Image, ImageTk
import sys, os

try:
	path = sys.argv[1]
#	path = 'try'
except IndexError:
	print "Usage: python key_point.py <path-to-imgs>"
	sys.exit(1)
	
try:
	files = os.listdir(path)
except OSError:
	print "Unable to access the directory!"	

path_parts = [split_part for split_part in os.path.split(path) if split_part != '']
image_folder_name = path_parts[-1]
print "image_folder_name: ", image_folder_name
annotationPath = os.path.join(path, '..', image_folder_name+'_annotations')
if not os.path.exists(annotationPath):
	os.makedirs(annotationPath)    

N_points = 7
point_now = 0
point_pos = [None for i in range(N_points)]
Buttons = []
annotationInfo = ['TL ', 'BR ', 'LE ', 'RE ', 'NO ', 'LM ', 'RM ']
rect = [None for i in range(N_points)]
bbox = None


for img_name in files:
	point_now = 0
	point_pos = [None for i in range(N_points)]
	Buttons = []
	rect = [None for i in range(N_points)]
	bbox = None
	
	out_name = img_name.split('.')[0]
	try:
		img = Image.open(open(os.path.join(path, img_name), 'rb'))
	except IOError:
		print "Unable to open image: " + os.path.join(path, img_name)
		exit(1)
	img_size = img.size

	def reDraw(num):
		print "reDraw: ", annotationInfo[num]
		global rect
		global N_points
		global bbox
		if rect[num] != None:
			canv.delete(rect[num])
			rect[num] = None
		if point_pos[num] != None:
			pt = point_pos[num][0]
			currentScrollPos = point_pos[num][1]
			rect[num] = canv.create_rectangle(pt[0]+int(img_size[0]*currentScrollPos[0])-2, pt[1]+int(img_size[1]*currentScrollPos[1])-2, pt[0]+int(img_size[0]*currentScrollPos[0])+2, pt[1]+int(img_size[1]*currentScrollPos[1])+2, fill="green")
			
			print "rect x: ", pt[0]+int(img_size[0]*currentScrollPos[0])
			print "rect y: ", pt[1]+int(img_size[1]*currentScrollPos[1])
		if num == 1 and rect[0] is not None:
			drawBBox()
		if num == 0 and rect[1] is not None:
			drawBBox()            

	def drawBBox():
		print 'drawBBox'
		global point_pos
		global bbox
		TL_point = point_pos[0]
		BR_point = point_pos[1]
		
		topLeft = (int(TL_point[0][0]+img_size[0]*(TL_point[1][0])), int(TL_point[0][1]+img_size[1]*(TL_point[1][1])))
		bottomRight = (int(BR_point[0][0]+img_size[0]*(BR_point[1][0])), int(BR_point[0][1]+img_size[1]*(BR_point[1][1])))
		if bbox != None:
			canv.delete(bbox)
		bbox = canv.create_rectangle(topLeft[0], topLeft[1], bottomRight[0], bottomRight[1], outline="blue")
		
	def clearPoint(num):
		print 'clear point: ', num
		global rect
		global bbox
		if rect[num] != None:
			canv.delete(rect[num])
			rect[num] = None
		if bbox != None and (rect[0] == None or rect[1] == None):
			canv.delete(bbox)	
			
	def getCoord(event):
		global point_pos
		point_pos[point_now] = [(event.x, event.y), (sbarH.get()[0], sbarV.get()[0])]
		print 'point_pos: ', point_pos[point_now]
		reDraw(point_now)

	def btn1_c():
		global point_now
		point_now = 0

	def btn2_c():
		global point_now
		point_now = 1

	def btn3_c():
		global point_now
		point_now = 2   

	def btn4_c():
		global point_now
		point_now = 3  

	def btn5_c():
		global point_now
		point_now = 4 

	def btn6_c():
		global point_now
		point_now = 5 

	def btn7_c():
		global point_now
		point_now = 6 

	def btn0_c():
		global point_pos
		point_pos[point_now] = None
		clearPoint(point_now)

	def btnx_c():
		print 'Next Image'
		top.destroy()		
	
	def key(event):
		print "pressed", repr(event.char)
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

	top = tk.Tk()

	toolbox = tk.Toplevel(top)
	btn1 = tk.Button(toolbox, text="Head top left(1)", command=btn1_c)
	Buttons.append(btn1)
	btn2 = tk.Button(toolbox, text="Head bottom right(2)", command=btn2_c)
	Buttons.append(btn2)
	btn3 = tk.Button(toolbox, text="left eye(3)", command=btn3_c)
	Buttons.append(btn3)
	btn4 = tk.Button(toolbox, text="right eye(4)", command=btn4_c)
	Buttons.append(btn4)
	btn5 = tk.Button(toolbox, text="nose(5)", command=btn5_c)
	Buttons.append(btn5)
	btn6 = tk.Button(toolbox, text="left mouse(6)", command=btn6_c)
	Buttons.append(btn6)
	btn7 = tk.Button(toolbox, text="right mouse(7)", command=btn7_c)
	Buttons.append(btn7)
	btn0 = tk.Button(toolbox, text="Clear this point(c)", command=btn0_c)
	Buttons.append(btn0)
	btnx = tk.Button(toolbox, text="Next Image(n)", command=btnx_c)
	Buttons.append(btnx)
	btnd = tk.Button(toolbox, text="Draw Bbox(d)", command=drawBBox)
	Buttons.append(btnd)

	top.wm_title(img_name)

	canv = tk.Canvas(top, relief=tk.SUNKEN)
	canv.config(width=1290, height=900)
	canv.config(highlightthickness=0)
	sbarV = tk.Scrollbar(top, orient=tk.VERTICAL)
	sbarH = tk.Scrollbar(top, orient=tk.HORIZONTAL)

	sbarV.config(command=canv.yview)
	sbarH.config(command=canv.xview)

	canv.config(yscrollcommand=sbarV.set)
	canv.config(xscrollcommand=sbarH.set)

	sbarV.pack(side=tk.RIGHT, fill=tk.Y)
	sbarH.pack(side=tk.BOTTOM, fill=tk.X)

	canv.config(scrollregion=(0,0,img_size[0], img_size[1]))
	displayImage = ImageTk.PhotoImage(img, master=canv)
	imgtag=canv.create_image(0,0,anchor="nw",image=displayImage)

	def _on_mousewheel(event):
		canv.yview_scroll(-event.delta, "units")
		
	canv.bind_all("<MouseWheel>", _on_mousewheel)
	canv.bind("<Button-1>",getCoord)
	canv.bind("<Key>", key)    
	canv.focus_set()

	canv.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

	for b in Buttons:
		b.pack()

	top.geometry('%dx%d+%d+%d' % (1290, 900, 150, 0))
	top.mainloop()
		
	fout = open(os.path.join(annotationPath, out_name+'.txt'), 'w')
	for i in range(N_points):
		if point_pos[i] != None:
			fout.write(annotationInfo[i]+str(int(point_pos[i][0][0]+img_size[0]*point_pos[i][1][0]))+" "+str(int(point_pos[i][0][1]+img_size[1]*point_pos[i][1][1]))+"\n")
		else:
			fout.write(annotationInfo[i]+"-1 -1"+"\n")
	fout.close()
	
