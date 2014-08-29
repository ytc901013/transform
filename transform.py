import re
import pdb
import argparse

class Transform(object):
    def __init__(self):
        self.odlist = []
        self.orstack = []

    def iftopf(self, exp):
        exp = self.format(exp)
        for element in exp:
            if self.isnum(element):
                self.odlist.append(element)
            if self.isop(element):
                self.or_stack(element)
            
        while len(self.orstack):
            self.odlist.append(self.orstack.pop())
        return ''.join(self.odlist)

    def format(self, exp):
        exp = list(exp)
        if self.getlevel(exp[0]) == 1:
            exp.insert(0, '0')

        pos = 0
        for e in exp:
            if self.getlevel(e) == 1 and exp[pos-1] == '(':
                exp.insert(pos, '0')
            pos += 1
        return ''.join(exp)
    
    def isnum(self, e):
        if re.match('[0-9]', e):
            return True
        else:
            return False

    def isop(self, e):
        if e in ['+','-','*','/','(',')']:
            return True
        else:
            return False
    
    def getlevel(self, e):
        if e in ['+', '-']:
            return 1
        elif e in ['*', '/']:
            return 2
        elif e in ['(', ')']:
            return 3

    def compare(self, a, b):
        return self.getlevel(a) > self.getlevel(b)
    
    def or_stack(self, e):
        if len(self.orstack) == 0 or e == "(" or self.orstack[-1] == "(":
            self.orstack.append(e)
            return
    
        if e == ")":
            while True:
                t = self.orstack.pop()
                if t != "(":
                    self.odlist.append(t)
                else:
                    return
    
        if  self.compare(e, self.orstack[-1]):
            self.orstack.append(e)
            return
    
        if not self.compare(e, self.orstack[-1]):
            self.odlist.append(self.orstack.pop())
            self.orstack.append(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', action="store", dest="exp", \
                        required=True, help="infix exprssion")
    results = parser.parse_args()
    exp = results.exp
    transform = Transform()
    print "%s => %s" % (exp, transform.iftopf(exp))
