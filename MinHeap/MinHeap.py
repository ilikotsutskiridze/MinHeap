import sys
import re

class KvPair:
    __slots__ = ['_key', '_value']

    def __init__(self, k:int, v:str):
        self._key = k
        self._value = v

    def key(self):
        return self._key

    def value(self):
        return self._value
    
    def set_key(self, k):
        self._key = k

    def set_value(self, v):
        self._value = v

    def __gt__(self, other):
        return self._key > other.key()

    def __lt__(self, other):
        return self._key < other.key()

    def __repr__(self):
        return '[%s %s]' % (self._key, self._value)

class BinMinHeapKV:
    def __init__(self):
        self.heapList = []
        self.K_dict = {}
        self.size = 0
        self.output = ""

    def add(self, k, v):
        if k in self.K_dict:
            self.output += "error\n"
        else:
            self.heapList.append(KvPair(k, v))
            self.K_dict[k] = len(self.heapList) - 1
            self.swap_up(len(self.heapList) - 1)
    
    def set(self, k, v):
        if k not in self.K_dict:
            self.output += "error\n"
        else:
            self.heapList[self.K_dict[k]].set_value(v)

    def delete(self, k):
        if k not in self.K_dict:
            self.output += "error\n"
        else:
            if self.K_dict[k] == len(self.heapList) - 1 or len(self.heapList) == 1:
                self.heapList.pop()
                del self.K_dict[k]
            else:
                i = self.K_dict[k]
                del self.K_dict[k]
                self.heapList[i] = self.heapList.pop()
                self.K_dict[self.heapList[i].key()] = i
                if (i - 1) // 2 >= 0 and self.heapList[(i - 1) // 2].key() > self.heapList[i].key():
                    self.swap_up(i)
                else:
                    self.swap_down(i)

    def search(self, k):
        if k not in self.K_dict:
            self.output += "0\n"
        else:
            self.output += f"1 {self.K_dict[k]} {self.heapList[self.K_dict[k]].value()}\n"

    def min(self):
        if len(self.heapList) == 0:
            self.output += "error\n"
        else:
            self.output +=f"{self.heapList[0].key()} 0 {self.heapList[0].value()}\n"

    def max(self):
        if len(self.heapList) == 0:
            self.output += "error\n"
        else:
            si = len(self.heapList) // 2
            max_KVPair = self.heapList[si]
            for i in range(si, len(self.heapList)):
                if self.heapList[i].key() > max_KVPair.key():
                    max_KVPair = self.heapList[i]
            self.output += f"{max_KVPair.key()} {self.K_dict[max_KVPair.key()]} {max_KVPair.value()}\n"

    def extract(self):
        if len(self.heapList) == 0:
            self.output += "error\n"
        else:
            rq_kvp = self.heapList[0]
            self.delete(rq_kvp.key())
            self.output += f"{rq_kvp.key()} {rq_kvp.value()}\n"

    def print(self):
        if len(self.heapList) == 0:
            self.output += "_\n"
        else:
            self.output += f"[{self.heapList[0].key()} {self.heapList[0].value()}]\n"
            lvl = 2
            for i in range(1, len(self.heapList)):
                self.output += f"[{self.heapList[i].key()} {self.heapList[i].value()} {self.heapList[(i - 1) // 2].key()}]"
                if i < (2 ** lvl) - 2:
                    self.output += ' '
                elif i == (2 ** lvl) - 2:
                    self.output += '\n'
                    lvl += 1
            if len(self.heapList) - 1 != (2 ** (lvl - 1) - 2):
                self.output += '_' + ' _' * ((2 ** lvl) - len(self.heapList) - 2) + '\n'
    
    def get_output(self):
        print(self.output)

    def swap(self, ci, pi):
        self.heapList[pi], self.heapList[ci] = self.heapList[ci], self.heapList[pi]
        self.K_dict[self.heapList[pi].key()], self.K_dict[self.heapList[ci].key()] = pi, ci
    
    def swap_down(self, i):
        ci = 2 * i + 1
        while ci < len(self.heapList):
            if ci + 1 < len(self.heapList) and self.heapList[ci + 1].key() < self.heapList[ci].key():
                ci += 1
            if self.heapList[ci].key() < self.heapList[i].key():
                self.swap(ci, i)
                i = ci
                ci = 2 * i + 1
            else:
                break

    def swap_up(self, i):
        pi = (i - 1) // 2
        while pi >= 0:
            if self.heapList[pi].key() > self.heapList[i].key():
                self.swap(i, pi)
                i = pi
                pi = (i - 1) // 2
            else:
                break

if __name__ == "__main__":
    array = [line.rstrip() for line in sys.stdin.readlines() if len(line.rstrip()) != 0]
    bh = BinMinHeapKV()
    for i in range(len(array)):
        if array[i].startswith(tuple(["add", "set", "delete", "search", "min", "max", "extract", "print"])):
            if re.match(r"add(\s)(-?)(\d)+(\s)(\S)+$", array[i]):
                bh.add(int(array[i].split(" ")[1]),array[i].split(" ")[2] )
            elif re.match(r"set(\s)(-?)(\d)+(\s)(\S)+$", array[i]):
                bh.set(int(array[i].split(" ")[1]),array[i].split(" ")[2] )
            elif re.match(r"delete(\s)(-?)(\d)+$", array[i]):
                bh.delete(int(array[i].split(" ")[1]))
            elif re.match(r"search(\s)(-?)(\d)+$", array[i]):
                bh.search(int(array[i].split(" ")[1]))
            elif re.match(r"min$", array[i]):
                bh.min()
            elif re.match(r"max$", array[i]):
                bh.max()
            elif re.match(r"extract$", array[i]):
                bh.extract()
            elif re.match(r"print$", array[i]):
                bh.print()
            else:
                print("error")
                sys.exit()
        else:
            print("error")
            sys.exit()
    del array
    bh.get_output()
