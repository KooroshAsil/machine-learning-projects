import pandas as pd
import seaborn
import matplotlib.pyplot as plt
file_load= pd.read_csv("Dry_Bean.csv")
hot_encoded= pd.get_dummies(file_load)
dataframe = hot_encoded.drop(columns=hot_encoded.columns[-7:])
correlations = dataframe.corr()
plt.figure(figsize=(20,20))
seaborn.heatmap(correlations, linewidths=1, annot=True, cmap="jet")
plt.title("Hatmap of correlations")
plt.show()

"""
annot : showing the value of every color shade if set TRUE inside the color shade
plt.figure : resizing the window that opens for a better display
linewidths : setting a gap between the color shades 
"""