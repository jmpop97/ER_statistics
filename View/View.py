import os
import platform


def clear_terminal():
    if "Windows" == platform.system():
        os.system("cls")
    else:
        os.system("clear")


class ViewDownLoading:
    def __init__(self) -> None:
        self.end = 0
        self.clear = ""
        self.download = ""
        self.bug_memory = []
        self.count = -1

    def display(self):
        clear_terminal()
        print(f"saved file name - {self.clear}")
        print(f"{self.count}/{self.end} ({self.count/self.end*100:.0f}%)")
        print(f"download - {self.download}")
        print(f"errorlist")
        if self.bug_memory:
            for bug in self.bug_memory:
                print(f"    {bug}")
        else:
            print("    None")

    def bug(self):
        self.bug_memory.append(self.download)

    def start(self, download):
        self.count += 1
        self.download = download

    def file_name(self, file_name):
        self.clear = file_name
