# import os
# from importlib.machinery import SourceFileLoader
# paths = []
# ignores = [".git", "venv", ".vscode", "__pycache__", "base_datas", "datas"]
# for folder, _, files in os.walk("./"):
#     ig = True
#     for ignore in ignores:
#         if ignore in folder:
#             ig = False
#     if ig:
#         for file in files:
#             if "test" in file:
#                 paths.append(folder + "/" + file)
# paths.remove(".//test.py")
# print(paths)

import ER_apis.test
