import pandas as pd

file_load= pd.read_csv("Dry_Bean.csv")
hot_encoded= pd.get_dummies(file_load)
dataframe = hot_encoded.drop(columns=hot_encoded.columns[-7:])
correlations = dataframe.corr().abs()
high_corr = correlations[correlations > 0.8]
cols = high_corr.columns.tolist()

groups = []
while cols:
    group = [cols.pop(0)]
    for col in cols:
        if all(high_corr.loc[group, col] > 0.8):
            group.append(col)
    groups.append(group)
largest_group = max(groups, key=len)
print("The largest collection of columns with correlation greater than 0.8 is: \n", largest_group) 