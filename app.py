import tkinter as tk
from tkinter import filedialog,messagebox,ttk
from analyzer import analyze
class App:
 def __init__(self,root):
  self.root=root;root.title("Bacteria Curve Analyzer");root.geometry("1000x650")
  ttk.Button(root,text="Open CSV",command=self.open).pack(pady=10)
  self.label=ttk.Label(root,text="No file selected");self.label.pack()
  self.tree=ttk.Treeview(root,columns=("test","R","S","result"),show="headings")
  for c,t in zip(("test","R","S","result"),("Test","Resistance score","Sensitivity score","Result")):
   self.tree.heading(c,text=t);self.tree.column(c,width=200)
  self.tree.pack(fill="x",padx=15,pady=10)
  self.info=ttk.Label(root,text="");self.info.pack()
 def open(self):
  p=filedialog.askopenfilename(filetypes=[("CSV","*.csv")])
  if not p:return
  try:n,r=analyze(p)
  except Exception as e:messagebox.showerror("Error",str(e));return
  self.label.config(text=p)
  for x in self.tree.get_children():self.tree.delete(x)
  for _,x in r.iterrows():self.tree.insert("", "end",values=(x.test,f"{x.resistance_score:.5f}",f"{x.sensitivity_score:.5f}",x.result))
  self.info.config(text="Lower score = more similar. INCONCLUSIVE means the two references are too close.")
tkroot=tk.Tk();App(tkroot);tkroot.mainloop()
