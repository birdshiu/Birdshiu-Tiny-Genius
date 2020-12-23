#用來翻譯的軟體,這個版本不會把選取的單字存到資料庫
#
#

from pynput.mouse import Listener, Button
import pyperclip
import pyautogui
import time
import requests
from bs4 import BeautifulSoup as bfs
import threading
import tkinter as tk
pyautogui.FAILSAFE=False
"""這不設成 False 的話 滑鼠點到邊邊會出事"""

class App(threading.Thread): #那個小視窗,從其它地方co來的程式碼,這樣顯示視窗時才不會卡死
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def do_nothing(arg): 
        pass
    
    def run(self):
        self.root = tk.Tk()
        self.root.geometry(str(windowW)+"x"+str(windowH)+'+'+str(mouseX)+'+'+str(mouseY))
        self.root.protocol("WM_DELETE_WINDOW", self.do_nothing)
        self.root.resizable(0, 0)
        self.root.title('翻譯')
        self.root.withdraw()
        
        self.text=tk.StringVar()
        self.text.set("text")

        self.textbox_string=tk.StringVar()
        
        self.label = tk.Label(self.root, textvariable=self.text)
        self.label.pack()
        
        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox=tk.Listbox(self.root, yscrollcommand=self.scrollbar.set)
        self.listbox.configure(state=tk.DISABLED)
        self.listbox.pack()
        
        
        self.root.mainloop()

screenW, screenH = pyautogui.size()
windowW, windowH = 200, 100
mouseX, mouseY, =0, 0
window=App()

click=0
pre_text=""   
    
def show_window(situation):
    if situation:
        window.root.geometry('+%d+%d'%(mouseX, mouseY))
        window.root.deiconify()

def reptile(text):
    global window
    chinese=list()
    window.listbox.configure(state=tk.NORMAL)
    window.listbox.delete(0,tk.END)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    html=requests.get('https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/'+text, headers=headers)
    html=bfs(html.text, 'html.parser')
    target=html.find_all("span",attrs={"lang":"zh-Hant", "class":"trans dtrans dtrans-se"})

    for t in target:
        context=t.string
        context=context.split('，')
        chinese.append(context)
    for_text2=""

    for c in chinese:
        c=str(c)
        c=c.replace('[','')
        c=c.replace(']','')
        c=c.replace("'",'')
        index=10

        if len(c) > 11:
            right=0
            left=10
            while len(c) > left+1:
                window.listbox.insert(tk.END, c[right:left+1])
                right=left+1
                left+=11
            window.listbox.insert(tk.END, c[right:])
        else:
            window.listbox.insert(tk.END, c)
    
        window.listbox.insert(tk.END, ' ')
    
    window.listbox.configure(state=tk.DISABLED)
    window.text.set(text)
    
def on_click(x, y, button, presse):
    global click
    if button == Button.left:
        click+=1
        if click%2 == 0:
            global window,mouseX,mouseY
                
            mouseX, mouseY=pyautogui.position()
            pyautogui.hotkey('ctrl','c')
            time.sleep(0.1)
            text=pyperclip.paste()
            text=text.lower()
            pyperclip.copy('')
            window.root.withdraw()
            
            global pre_text
            
            if text and pre_text!=text:
                reptile(text)
                show_window(True)
                pre_text=text
            
with Listener(on_click=on_click) as listen:
    listen.join()
    
