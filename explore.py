import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def plot_variable_pairs(df):
    sns.pairplot(data=df, kind='reg', plot_kws={'line_kws':{'color':'black'}}, corner=True);
    
def plot_variable_pairs_cat_hue(df):
    cat_cols = df.select_dtypes('object').columns.tolist()
    for cat in cat_cols:
        sns.pairplot(data=df, hue=cat, corner=True);
        
def plot_categorical_and_continuous_vars(df, cat_cols, num_cols):
    for cat_col in cat_cols:
        
        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(cat_col)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        
        for num_col in num_cols:
            
            print('\n----------------------------------------------------------------------------------------------------------')
            print(num_col)
            print('----------------------------------------------------------------------------------------------------------\n')
           
            fig = plt.figure(figsize = (12,6))
            fig.suptitle(f'{cat_col} vs. {num_col}')
            
            gs = plt.GridSpec(2,3)
            
            ax1 = fig.add_subplot(gs[0,0])
            sns.barplot(x=cat_col, y=num_col, data=df)
            plt.xticks(rotation = 90)
            
            ax2 = fig.add_subplot(gs[0,1])
            sns.swarmplot(x=cat_col, y=num_col, data=df)
            plt.xticks(rotation = 90)
            
            ax3 = fig.add_subplot(gs[0,2])
            sns.stripplot(x=cat_col, y=num_col, data=df)
            plt.xticks(rotation = 90)
            
            ax4 = fig.add_subplot(gs[1,0])
            sns.boxplot(x=cat_col, y=num_col, data=df)
            plt.xticks(rotation = 90)
            
            ax5 = fig.add_subplot(gs[1,1])
            sns.boxenplot(x=cat_col, y=num_col, data=df)
            plt.xticks(rotation = 90)
            
            ax6 = fig.add_subplot(gs[1,2])
            sns.violinplot(x=cat_col, y=num_col, data=df)
            plt.xticks(rotation = 90)
            
            plt.tight_layout()
            plt.show();