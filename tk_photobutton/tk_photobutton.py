#%%
from re import T
from tkinter import *
import tkinter as tk

root=tk.Tk()
root.title("Order tkinter")
root.geometry("600x400+200+200")  #  창크기: 가로x세로 + 창 출력위치 좌표
#%%
Label(root, text="메뉴를 선택해 주세요",font=("Arial", 25)). pack(side="top")
Button(root, text="주문하기",font=("Arial", 15)). pack(side="bottom")

#버튼에 사진 넣는 기능
photo1=tk.PhotoImage(file="kr_food_bt.png")
photo2=tk.PhotoImage(file="cn_food_bt.png")
photo3=tk.PhotoImage(file="jp_food_bt.png")

#버튼 화면배치
button1 = tk.Button(root,image=photo1,text="한식",width=160,height=180)
button1.place(x=30,y=100)
button2 = tk.Button(root,image=photo2,text="중식",width=160,height=180)
button2.place(x=220,y=100)
button3 = tk.Button(root,image=photo3,text="일식",width=160,height=180)
button3.place(x=410,y=100)
#%%
root.mainloop()
# %%
