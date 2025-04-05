import pandas as pd

df = pd.read_excel('labelmaker/Item list.xlsx') # can also index sheet by name or fetch all sheets
mylist = df['ITEM DESCRIPTION'].tolist()

cleaned_list = []
for my in mylist:
    cleaned_list.append(str(my))
    
a=[x for x in cleaned_list if x != "nan"]
print(a)