import pandas as pd
import os

path = f"{os.getcwd()}"

files = [
    "PS1Interface.csv",
    "PS1Mid-oxycline.csv",
    "PS1SCM.csv",
    "PS1Surface.csv",
    "PS1Top of oxycline.csv",
    "PS2Base of ODZ.csv",
    "PS2Deep ODZ core.csv",
    "PS2Deep oxycline.csv",
    "PS2Interface.csv",
    "PS2PNM.csv",
    "PS2SCM.csv",
    "PS2SNM.csv",
    "PS2Top of oxycline.csv",
    "PS3Deep ODZ core.csv",
    "PS3Deep oxycline.csv",
    "PS3Interface.csv",
    "PS3Interface2.csv",
    "PS3Mid-oxycline.csv",
    "PS3SCM.csv",
    "PS3SNM.csv",
    "PS3Top of oxycline.csv",
]

output = pd.DataFrame([])

for f in files:
    data = pd.read_csv(f"{path}/{f}")
    data["Station"] = f[0:3]
    data["Feature"] = f[3:-4]
    output = pd.concat([output, data])

output.to_csv(f"{path}/montecarlocompiled.csv")
