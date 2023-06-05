import pandas as pd
from ortoolpy import model_min, addbinvars, addvals
from pulp import lpSum
from japanmap import pref_names, adjacent, pref_map
import matplotlib.pyplot as plt
import subprocess
m = model_min()
df = pd.DataFrame([(i, pref_names[i], j) for i in range(1, 48) for j in range(4)], 
                  columns=['Code', '県', '色'])
addbinvars(df) 
for i in range(1, 48):
    m += lpSum(df[df.Code == i].Var) == 1
    for j in adjacent(i):
        for k in range(4):
            m += lpSum(df.query('Code.isin([@i, @j]) and 色 == @k').Var) <= 1
m.solve()
addvals(df)
四色 = ['red', 'blue', 'green', 'yellow']
cols = df[df.Val > 0].色.apply(四色.__getitem__).reset_index(drop=True)
fig, ax= plt.subplots(figsize=(8, 6))
pref_map(range(1, 48), cols=cols, width=2.5)