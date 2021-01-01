import glob, os
os.chdir("images/classified")
print(len(glob.glob("*")))
for f in glob.glob("*"):
    if f[0:2] == "1_" or f[0:2] == "0_":
        pass
    else:
        os.remove('images/classified/' + f)