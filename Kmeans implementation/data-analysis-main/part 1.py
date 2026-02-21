import pandas as pd
import numpy as np
file_load= pd.read_csv("Dry_Bean.csv")
dtframe = pd.DataFrame(file_load)
print(dtframe.describe())