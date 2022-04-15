import pandas as pd
from pandas import DataFrame
import numpy as np
import string
import csv
import random

'''A. Сгенерировать csv файл из 1024 записей по 6 столбцов, 
заполненных строками случайных символов (цифры и латинские буквы) 
 длиной по 8 символов. '''
columns=list('ABCDEF')
# df = pd.DataFrame(np.random.randn(1025, 6), columns=columns)
# for row in df[columns]:
#     for i in range(1, 1025):
#         row_list = [random.choice
#             (string.ascii_letters+ string.digits) 
#                 for i in range(8)]
#         df.loc[i, row] = ''.join(row_list)
# data = df.drop(labels=0, axis=0)

# print(data)
# data.to_csv('tcsv.csv', index=False)
   
'''B. Считать содержимое файла, заменить нечетные цифры символом #, 
удалить записи, в которых любая из шести строк начинается с 
гласной буквы, сохранить отредактированный файл с другим именем. '''
df = pd.read_csv('tcsv.csv')

vowel_list = ['a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U', 'y', 'Y']
for i in vowel_list:
    for x in df[columns]:
        df = df[~df[x].astype(str).str.startswith(i)]
   
   
print(df)
df.to_csv('tcsv21.csv', index=False)
data = pd.read_csv('tcsv21.csv')



    



