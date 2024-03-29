# -*- coding: utf-8 -*-
"""JupyterNotebook-PM2.5-csv.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WGCj1p5SpqLcyUpggMBtNiqWd5LftsmW
"""

import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/KevinTruong02/E11-Lab-Kevin-Ryan-Nick/9fc85a1cca17a5730dd8ad6f8c75fc3c4e16371f/aq_data.csv")
df.head ()
print(df.columns)
print(df.head())

import matplotlib.pyplot as plt
plt.figure(figsize= (10,6))
plt.hist(df['PM2.5'], bins= 15, color= 'skyblue', edgecolor='black')
plt.title('PM2.5 Frequenct Distribution')
plt.xlabel('PM2.5 Level')
plt.ylabel('Frequency')
plt.grid(True)
plt.show
