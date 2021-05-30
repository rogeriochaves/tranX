import os

path = os.path.join(os.path.dirname(__file__))
datagens = os.listdir(path)
for folder in datagens:
    if "__" in folder or not os.path.isdir(os.path.join(path, folder)):
        continue
    print("generating", folder)
    os.system("python3 " + os.path.join(path, folder, "generate.py"))