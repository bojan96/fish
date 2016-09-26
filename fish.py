import argparse
import random
import sys
import logging
import traceback

class FishInvalidOperation(Exception):
    pass

class StackRegPair:
    
    def __init__(self):
        self.register = None
        self.stack = []

class Interpreter:


    def __init__(self,codebox):
        
        self.directionY = 0
        self.directionX = 1
        self.stackRegList = [StackRegPair()]
        self.ipY = 0
        self.ipX = 0
        self.codebox = codebox
        self.codeboxH = len(codebox)
        self.codeboxW = len(codebox[0])
        self.stringMode = False
        self.endExec = False
        self.stringQuote = False
        self.stringDbQuote = False
        self.fp = open("input.txt")
        


        self.instructionTable = {

            "<": self.OPgoLeft,
            ">": self.OPgoRight,
            "^": self.OPgoUp,
            "v": self.OPgoDown,
            "x": self.OPgoRandom,
            "/": self.OPmirrorSlash,
            "\\": self.OPmirrorBackslash,
            "|": self.OPmirrorVertical,
            "_": self.OPmirrorHorizontal,
            "#": self.OPmirrorHash,
            "!": self.OPtramp,
            "?": self.OPcondTramp,
            ".": self.OPjump,
            "0": self.OPpushVal,
            "1": self.OPpushVal,
            "2": self.OPpushVal,
            "3": self.OPpushVal,
            "4": self.OPpushVal,
            "5": self.OPpushVal,
            "6": self.OPpushVal,
            "7": self.OPpushVal,
            "8": self.OPpushVal,
            "9": self.OPpushVal,
            "a": self.OPpushVal,
            "b": self.OPpushVal,
            "c": self.OPpushVal,
            "d": self.OPpushVal,
            "e": self.OPpushVal,
            "f": self.OPpushVal,
            "+": self.OPadd,
            "-": self.OPsub,
            "*": self.OPmul,
            ",": self.OPdiv,
            "%": self.OPmod,
            "=": self.OPequals,
            ")": self.OPgreater,
            "(": self.OPless,
            "'": self.OPstringQuote,
            "\"": self.OPstringDbQuote,
            ":": self.OPduplicateVal,
            "~": self.OPremoveVal,
            "$": self.OPswapVal,
            "@": self.OPswap3Val,
            "}": self.OPshiftRight,
            "{": self.OPshiftLeft,
            "r": self.OPreverseStack,
            "l": self.OPstackLen,
            "[": self.OPnewStack,
            "]": self.OPremStack,
            "o": self.OPprintChar,
            "n": self.OPprintNum,
            "i": self.OPreadChar,
            "&": self.OPreg,
            "g": self.OPgetCell,
            "p": self.OPputCell,
            ";": self.OPend,
            " ": self.OPnoop,
            #"\0": self.OPnoop
            
            
            }


        self.directions = ( (1,0), (-1,0), (0,1), (0,-1) ) 


    def updateIP(self):

        self.ipY = (self.ipY + self.directionY) % self.codeboxH
        self.ipX = (self.ipX + self.directionX) % self.codeboxW

    def pushStack(self,val):
        
        self.stackRegList[-1].stack.append(val)

    def popStack(self):

        try:
            
            val = self.stackRegList[-1].stack.pop()

        except IndexError as err:
            raise FishInvalidOperation() from err

        return val

    def OPgoLeft(self):

        self.directionY = 0
        self.directionX = -1

    def OPgoRight(self):

        self.directionY = 0
        self.directionX = 1

    def OPgoUp(self):

        self.directionY = -1
        self.directionX = 0

    def OPgoDown(self):

        self.directionY = 1
        self.directionX = 0

    def OPgoRandom(self):

        direction = random.choice(self.directions)
        self.directionY = direction[0]
        self.directionX = direction[1]
        
    def OPmirrorSlash(self):

        self.directionY, self.directionX = -self.directionX, -self.directionY

    def OPmirrorBackslash(self):

        self.directionY, self.directionX = self.directionX, self.directionY

    def OPmirrorVertical(self):

        if self.directionX:
            self.directionX = -self.directionX

    def OPmirrorHorizontal(self):

        if self.directionY:
            self.directionY = -self.directionY
        
    def OPmirrorHash(self):

        self.directionY = -self.directionY
        self.directionX = -self.directionX

    def OPtramp(self):

        self.updateIP()

    def OPcondTramp(self):

        if (not self.popStack()):
            self.updateIP()

    def OPjump(self):

        self.ipY = self.popStack()
        self.ipX = self.popStack()

    def OPpushVal(self):

        val = self.codebox[self.ipY][self.ipX]

        if val.isdigit():
            self.pushStack(int(val))

        else:
            self.pushStack(ord(val) - 87)

    def OPadd(self):

        a = self.popStack()
        b = self.popStack()

        self.pushStack(a + b)

    def OPsub(self):

        a = self.popStack()
        b = self.popStack()

        self.pushStack(b - a)

    def OPmul(self):

        a = self.popStack()
        b = self.popStack()

        self.pushStack(a * b)
        
    def OPdiv(self):

        a = self.popStack()
        b = self.popStack()

        try:

            self.pushStack(b / a)

        except ZeroDivisionError as err:

            raise FishInvalidOperation() from err

    def OPmod(self):

        a = self.popStack()
        b = self.popStack()

        try:

            self.pushStack(b % a)

        except ZeroDivisionError as err:

            raise FishInvalidOperation() from err

    def OPequals(self):

        a = self.popStack()
        b = self.popStack()

        self.pushStack(int(a == b))

    def OPgreater(self):

        a = self.popStack()
        b = self.popStack()

        self.pushStack(int(b > a))

    def OPless(self):

        a = self.popStack()
        b = self.popStack()

        self.pushStack(int(b < a))
        

    def OPstringQuote(self):

        self.stringQuote = not self.stringQuote

    def OPstringDbQuote(self):

        self.stringDbQuote = not self.stringDbQuote
    
    def OPduplicateVal(self):

        try:

            stack = self.stackRegList[-1].stack
            stack.append(stack[-1])

        except IndexError as err:

            raise FishInvalidOperation() from err
        

    def OPremoveVal(self):

        self.popStack()

    def OPswapVal(self):

        try:

            stack = self.stackRegList[-1].stack
            stack[-1], stack[-2] = stack[-2], stack[-1]

        except IndexError as err:

            raise FishInvalidOperation() from err 
        
    def OPswap3Val(self):

        try:

            stack = self.stackRegList[-1].stack
            stack[-3], stack[-2], stack[-1] = stack[-1], stack[-3], stack[-2]

        except IndexError as err:

            raise FishInvalidOperation() from err
        

    def OPshiftRight(self):

        stack = self.stackRegList[-1].stack

        temp = [0] * len(stack)

        for i in range(len(stack)):

            temp[(i+1) % len(stack)] = stack[i]

        self.stackRegList[-1].stack = temp
        

    def OPshiftLeft(self):

        stack = self.stackRegList[-1].stack

        temp = [0] * len(stack)

        for i in range(len(stack)):

            temp[(i-1) % len(stack)] = stack[i]

        self.stackRegList[-1].stack = temp

    def OPreverseStack(self):

        self.stackRegList[-1].stack.reverse()

    def OPstackLen(self):

        self.pushStack(len(self.stackRegList[-1].stack))

    def OPnewStack(self):

    
         toPop = self.popStack()
         newStackReg = StackRegPair()

         for val in range(toPop):
             newStackReg.stack.append(self.popStack())

         self.stackRegList.append(newStackReg)
        
    def OPremStack(self):

        if len(self.stackRegList) == 1:
            raise FishInvalidOperation()

        toRemove = self.stackRegList[-1].stack

        for i in range(len(toRemove)):
            self.stackRegList[-2].stack.append(toRemove.pop())
        
        self.stackRegList.pop()

    def OPprintNum(self):

        print(self.popStack(),end = "")

    def OPprintChar(self):

        print(chr(self.popStack()),end = "")
              
    def OPreadChar(self):

        ch = self.fp.read(1)

        if ch == "":
            self.pushStack(-1)
            return

        if ch == "\n":
            ch = self.fp.read(1)


        self.pushStack(ord(ch))


    def OPreg(self):

        if self.stackRegList[-1].register == None:
            self.stackRegList[-1].register = self.popStack()

        else:
            self.pushStack(self.stackRegList[-1].register)
            self.stackRegList[-1].register = None
            
    def OPgetCell(self):

        y = self.popStack()
        x = self.popStack()

        if y >= self.codeboxH or x >= self.codeboxW or x < 0 or y < 0:
            self.pushStack(0)

       #if self.codebox[y][x] == " ":
           #self.pushStack(0)

        else:
            self.pushStack(ord(self.codebox[y][x]))

    def OPputCell(self):

        y = self.popStack()
        x = self.popStack()
        val = self.popStack()

        self.codebox[y][x] = chr(val)
        
    def OPend(self):

        self.endExec = True

    def OPnoop(self):
        pass

    def InvalidInstruction(self):

        raise FishInvalidOperation()

    def isQuote(self):

        quote = self.codebox[self.ipY][self.ipX]

        return quote == "\"" or quote == "'"


    def dbgPrintStack(self):

        logging.debug("Stack: {0}\n".format(str(self.stackRegList[-1].stack)))

    def dbgPrintInstr(self):

        logging.debug("Instr: {0}".format(self.codebox[self.ipY][self.ipX]))

    def run(self):

        
        while (not self.endExec):


            element = self.codebox[self.ipY][self.ipX]
            
            if (self.stringQuote and element != "'") or (self.stringDbQuote and element != "\""):

                self.pushStack(ord(element))
            
            else:

                #self.dbgPrintInstr()
                nextInstruction = self.instructionTable.get(element, self.InvalidInstruction)
                nextInstruction()

            #self.dbgPrintStack()
            self.updateIP()
            
            
    



def initArgparse():

    parser = argparse.ArgumentParser()
    parser.add_argument("script",help = "Script to execute")

    return parser


def parseScript(script):


    codebox = []

    with open(script) as fileScript:

        lines = fileScript.read().splitlines()
        maxLine = 0

        for line in lines:
            
            if len(line) > maxLine:
                maxLine = len(line)

        for line in lines:

            codebox.append(list(line) + [" "] * (maxLine - len(line)))

    return codebox


def main():

    try:

        logging.basicConfig(filename = "fish.log",level = logging.DEBUG, filemode = "w")
        
        parser = initArgparse()
        args = parser.parse_args()

        codebox = parseScript(args.script)

        interpreter = Interpreter(codebox)

        interpreter.run()

        print()

    
    except OSError as err:

        print("Error: Could not open the script: \"{0}\" ".format(err.filename)
              , file = sys.stderr)

    except FishInvalidOperation:

        print("Error: Something smells fishy", file = sys.stderr)
        logging.debug(traceback.format_exc())

    finally:
        pass
        

if __name__ == "__main__":
    main()
    
