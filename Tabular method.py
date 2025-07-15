import tkinter as tk
from tkinter import messagebox
from collections import defaultdict

def count_ones(t):return t.count('1')

def diff_by_one_bit(a,b):
 diff=0
 for i in range(len(a)):
  if a[i]!=b[i]:
   if a[i]=='-'or b[i]=='-':return False,None
   diff+=1
   if diff>1:return False,None
 return diff==1,None


def combine_terms(a,b):
 r=''
 for i in range(len(a)):
  r+=a[i]if a[i]==b[i]else'-'
 return r


def get_prime_implicants(minTerms,numVars):
 ts=[format(m,f'0{numVars}b')for m in minTerms]
 p_imp=set()
 gs=defaultdict(list)
 for t in ts:gs[count_ones(t)].append((t,[int(t,2)]))

 while gs:
  new_gs=defaultdict(list)
  used_Before=set()
  g_codes=sorted(gs.keys())
  for i in range(len(g_codes)-1):
   g1=gs[g_codes[i]]
   g2=gs[g_codes[i+1]]
   for t1,origin1 in g1:
    for t2,origin2 in g2:
     diffOneBit,_=diff_by_one_bit(t1,t2)
     if diffOneBit:
      combined=combine_terms(t1,t2)
      new_origin=sorted(set(origin1+origin2))
      new_gs[count_ones(combined.replace('-',''))].append((combined,new_origin))
      used_Before.add(t1)
      used_Before.add(t2)

  for g in gs.values():
   for t,origin in g:
    if t not in used_Before:p_imp.add((t,tuple(origin)))

  if not new_gs:break
  gs=defaultdict(list)
  for g in new_gs.values():
   for t,origin in g:gs[count_ones(t.replace('-',''))].append((t,origin))
 return p_imp


def term_to_boolean(t):
 variables='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
 return''.join([variables[i]if ch=='1'else variables[i]+"'"if ch=='0'else''for i,ch in enumerate(t)])


def maxterm_to_pos(t):
 variables='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
 r=[]
 for i,ch in enumerate(t):
  if ch=='1':r.append(variables[i]+"'")
  elif ch=='0':r.append(variables[i])

 return'('+'+'.join(r)+')'


def term_to_pos(t):
 variables='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
 r=[]
 for i,ch in enumerate(t):
  if ch=='1':r.append(variables[i]+"'")
  elif ch=='0':r.append(variables[i])

 return'('+'+'.join(r)+')'


def find_essential_prime_implicants(p_imp,minterms):
 chart=defaultdict(list)
 for t,origin in p_imp:
  for m in origin:
   if m in minterms:chart[m].append(t)

 esPrime=set()
 for m,covers in chart.items():
  if len(covers)==1:esPrime.add(covers[0])

 return esPrime


root=tk.Tk()
root.title("Tabular Method Tool")
root.geometry("1280x1080")

num_vars=tk.StringVar()
terms_input=tk.StringVar()
dontcares_input=tk.StringVar()
selected_mode=tk.StringVar()
selected_exp=tk.StringVar()
startup_frame=tk.Frame(root)
home_frame=tk.Frame(root)
input_frame=tk.Frame(root)

def show_startup():
 home_frame.pack_forget()
 input_frame.pack_forget()
 startup_frame.pack(pady=100)

def show_home(operation):
 selected_exp.set(operation)
 startup_frame.pack_forget()
 input_frame.pack_forget()
 clear_all()
 home_frame.pack(pady=100)

def show_input(mode):
 selected_mode.set(mode)
 label_terms.config(text="\nEnter Minterms (comma-separated):"if mode=='minterm'else"\n Enter Maxterms (comma-separated):")
 home_frame.pack_forget()
 input_frame.pack(pady=20)
 if mode=='maxterm':hint_label.pack(pady=5)
 else:hint_label.pack_forget()

def clear_all():
 num_vars.set('')
 terms_input.set('')
 dontcares_input.set('')
 output.config(state='normal')
 output.delete('1.0',tk.END)
 output.config(state='disabled')


def runTheProgram():
 try:
  numVars=int(num_vars.get())
  ts=[int(x.strip())for x in terms_input.get().split(',')if x.strip().isdigit()]
  dcares=[int(x.strip())for x in dontcares_input.get().split(',')]if dontcares_input.get()else[]
  if any(m>=2**numVars for m in ts+dcares):
   messagebox.showerror("Error",f"All values must be less than 2^{numVars}")
   return
  
  if selected_exp.get()=='Min SOP':
   minterms=[i for i in range(2**numVars)if i not in ts and i not in dcares]if selected_mode.get()=='maxterm'else ts
   all_ts=sorted(set(minterms+dcares))
   raw_ps=get_prime_implicants(all_ts,numVars)
   ps={t for t,_ in raw_ps}
   essentials=find_essential_prime_implicants(raw_ps,minterms)
   covered=set()

   for t,origin in raw_ps:
    if t in essentials:covered.update(set(origin)&set(minterms))

   remaining=set(minterms)-covered
   additional_pis=set()
   while remaining:
    best_pi=None
    DOremain=set()

    for t,origin in raw_ps:
     if t in essentials or t in additional_pis:continue
     coverage=set(origin)&remaining
     if len(coverage)>len(DOremain):
      best_pi=t
      DOremain=coverage

    if not best_pi:break
    additional_pis.add(best_pi)
    remaining-=DOremain
   total_terms=essentials.union(additional_pis)

   output.config(state='normal')
   output.delete('1.0',tk.END)
   output.insert(tk.END,f"Number of Prime Implicants: {len(ps)}\nPrime Implicants:\n")

   for p in sorted(ps):output.insert(tk.END,f"\t\t\t\t{term_to_boolean(p)}\n")

   output.insert(tk.END,f"\nNumber of Essential Prime Implicants: {len(essentials)}\nEssential Prime Implicants:\n")
   for e in sorted(essentials):output.insert(tk.END,f"\t\t\t\t{term_to_boolean(e)}\n")

   if total_terms:
    min_sop=' + '.join(term_to_boolean(e)for e in sorted(total_terms))
    output.insert(tk.END,f"\nMin SOP Expression: {min_sop}\n")

   output.config(state='disabled')
  elif selected_exp.get()=='POS':
   maxterms=ts if selected_mode.get()=='maxterm'else[i for i in range(2**numVars)if i not in ts and i not in dcares]
   all_ts=sorted(set(maxterms+dcares))
   raw_ps=get_prime_implicants(all_ts,numVars)
   ps={t for t,_ in raw_ps}
   essentials=find_essential_prime_implicants(raw_ps,maxterms)
   covered=set()
   for t,origin in raw_ps:
    if t in essentials:covered.update(set(origin)&set(maxterms))

   remaining=set(maxterms)-covered
   additional_pis=set()

   while remaining:
    best_pi=None
    DOremain=set()

    for t,origin in raw_ps:
     if t in essentials or t in additional_pis:continue
     coverage=set(origin)&remaining

     if len(coverage)>len(DOremain):
      best_pi=t
      DOremain=coverage

    if not best_pi:break
    additional_pis.add(best_pi)
    remaining-=DOremain
   total_terms=essentials.union(additional_pis)

   output.config(state='normal')
   output.delete('1.0',tk.END)
   output.insert(tk.END,f"Number of Prime Implicants: {len(ps)}\nPrime Implicants:\n")

   for p in sorted(ps):output.insert(tk.END,f"\t\t\t\t{term_to_pos(p)}\n")

   output.insert(tk.END,f"\nNumber of Essential Prime Implicants: {len(essentials)}\nEssential Prime Implicants:\n")
   for e in sorted(essentials):output.insert(tk.END,f"\t\t\t\t{term_to_pos(e)}\n")

   if total_terms:
    pos_expr=''.join(term_to_pos(t)for t in sorted(total_terms))
    output.insert(tk.END,f"\nMin POS Expression: {pos_expr}\n")

   output.config(state='disabled')

 except ValueError:
  messagebox.showerror("Error","Please enter valid numeric values!!")

tk.Label(startup_frame,text="Faculty of Engineering, Alexandria University ",font=("Courier",12)).pack(side="top")
tk.Label(startup_frame,text="Department of CCE\n",font=("Courier",12)).pack(pady=1)
tk.Label(startup_frame,text="\n\n\nName: Pola Nasser Ayoub\t\t\t\n ID: 9505\t\t\t\t  ",font=("Courier",15)).pack(side="bottom")
tk.Label(home_frame,text="Faculty of Engineering, Alexandria University ",font=("Courier",12)).pack(side="top")
tk.Label(home_frame,text="Department of CCE\n",font=("Courier",12)).pack(pady=1)
tk.Label(home_frame,text="\n\n\nName: Pola Nasser Ayoub\t\t\t\n ID: 9505\t\t\t\t  ",font=("Courier",15)).pack(side="bottom")
tk.Label(startup_frame,text="Choose a way to represent Boolean expressions:",font=("Arial",15)).pack(pady=20)
tk.Button(startup_frame,text="SOP",font="15",width=30,bg="OliveDrab1",command=lambda:show_home('Min SOP')).pack(pady=10)
tk.Button(startup_frame,text="POS",font="15",width=30,bg="turquoise1",command=lambda:show_home('POS')).pack(pady=10)
tk.Button(startup_frame,text="Exit",font="15",width=30,command=root.destroy,bg="lightcoral").pack(pady=10)
tk.Label(home_frame,text="Select Input Type:",font=("Arial",15)).pack(pady=20)
tk.Button(home_frame,text="Prime Implicants for Minterms",width=30,height=1,font="10",bg="Pale Turquoise1",command=lambda:show_input('minterm')).pack(pady=10)
tk.Button(home_frame,text="Prime Implicants for Maxterms",width=30,height=1,font="10",bg="aquamarine",command=lambda:show_input('maxterm')).pack(pady=10)
tk.Button(home_frame,text="Back",width=30,height=1,font="10",bg="bisque2",command=show_startup).pack(pady=10)

output=tk.Text(input_frame,height=25,width=95,state='disabled')
output.pack()

hint_label=tk.Label(input_frame,text="Note: For large variable (Greater than 5 variables) counts with few maxterms, processing may take time.",fg="red",font=("Arial",10,"italic"))

tk.Label(input_frame,text="\nEnter the number of variables:").pack()
tk.Entry(input_frame,textvariable=num_vars,width=52).pack()

label_terms=tk.Label(input_frame)
label_terms.pack()

tk.Entry(input_frame,textvariable=terms_input,width=52).pack()
tk.Label(input_frame,text="\nEnter Don't Cares (optional) (comma-separated):").pack()
tk.Entry(input_frame,textvariable=dontcares_input,width=52).pack()
tk.Button(input_frame,text="Calculate",command=runTheProgram,bg="lightgreen").pack(pady=10)

button_frame=tk.Frame(input_frame)
button_frame.pack(pady=10)

tk.Button(button_frame,text="Again",bg="purple",fg="white",width=20,height=1,command=clear_all).grid(row=0,column=0,padx=10)
tk.Button(button_frame,text="Back",bg="red",fg="white",width=20,height=1,command=lambda:show_home(selected_exp.get())).grid(row=0,column=1,padx=10)

show_startup()
root.mainloop()
