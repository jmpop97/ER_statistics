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
        self.type_skip_memory = []
        self.duplication_skip_memory = []
        self.count = -1

    def display(self):
        clear_terminal()
        print(f"saved file name - {self.clear}")
        print(f"{self.count}/{self.end} ({self.count/self.end*100:.0f}%)")
        print(f"download - {self.download}")
        if self.bug_memory:
            print(f"error list")
            for bug in self.bug_memory:
                print(f"    {bug}")

        if self.type_skip_memory:
            print(f"type skip list")
            for skip in self.type_skip_memory:
                print(f"    {skip}")

        if self.duplication_skip_memory:
            print(f"duplication skip list")
            for skip in self.duplication_skip_memory:
                print(f"    {skip}")

    def bug(self):
        self.bug_memory.append(self.download)

    def type_skip(self, skip):
        self.type_skip_memory.append(skip)

    def duplication_skip(self, skip):
        self.duplication_skip_memory.append(skip)

    def start(self, download):
        self.count += 1
        self.download = download

    def file_name(self, file_name):
        self.clear = file_name
