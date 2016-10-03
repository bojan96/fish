#!/usr/bin/env python3

import argparse
import random
import sys
import logging
import traceback

class FishError(Exception):
    pass

class StackRegPair:
    
    def __init__(self):
        self.register = None
        self.stack = []

class Interpreter:


    def __init__(self,codebox,initialStack):
        
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
        self.instrCount = 0
        self.outsideCodebox = {}
        self.stackRegList[-1].stack = initialStack
        

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
            "\0": self.OPnoop
            
            
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
            
            raise FishError from err

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

        if chr(val).isdigit():
            
            self.pushStack(int(chr(val)))

        else:
            
            self.pushStack(val - 87)

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

            raise FishError from err

    def OPmod(self):

        a = self.popStack()
        b = self.popStack()

        try:

            self.pushStack(b % a)

        except ZeroDivisionError as err:

            raise FishError from err

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

            raise FishError from err
        

    def OPremoveVal(self):

        self.popStack()

    def OPswapVal(self):

        try:

            stack = self.stackRegList[-1].stack
            stack[-1], stack[-2] = stack[-2], stack[-1]

        except IndexError as err:

            raise FishError from err 
        
    def OPswap3Val(self):

        try:

            stack = self.stackRegList[-1].stack
            stack[-3], stack[-2], stack[-1] = stack[-1], stack[-3], stack[-2]

        except IndexError as err:

            raise FishError from err
        

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
            
            raise FishError

        toRemove = self.stackRegList[-1].stack

        for i in range(len(toRemove)):
            
            self.stackRegList[-2].stack.append(toRemove.pop())
        
        self.stackRegList.pop()

    def OPprintNum(self):

        print(self.popStack(),end = "")

    def OPprintChar(self):

        try:

            print(chr(self.popStack()),end = "")

        except TypeError as err:

            raise FishError from err
              
    def OPreadChar(self):

        ch = sys.stdin.read(1)

        while ch == "\n":
            
            ch = sys.stdin.read(1)

        if ch == "":
            
            self.pushStack(-1)

        else:

            self.pushStack(ord(ch))


    def OPreg(self):

        if self.stackRegList[-1].register == None:
            
            self.stackRegList[-1].register = self.popStack()

        else:
            
            self.pushStack(self.stackRegList[-1].register)
            self.stackRegList[-1].register = None
            
    def OPgetCell(self):

        y = int(self.popStack())
        x = int(self.popStack())

        if y >= self.codeboxH or x >= self.codeboxW or y < 0 or x < 0:

            key = (y,x)

            self.pushStack(self.outsideCodebox.get(key,0))
            
        else:
            
            self.pushStack(self.codebox[y][x])

    def OPputCell(self):

        y = int(self.popStack())
        x = int(self.popStack())
        val = self.popStack()

        if y >= self.codeboxH or x >= self.codeboxW or y < 0 or x < 0:

            key = (y,x)
            self.outsideCodebox[key] = val

        else:
            
            self.codebox[y][x] = val
        
    def OPend(self):

        self.endExec = True

    def OPnoop(self):
        pass

    def invalidInstruction(self):

        raise FishError

    
    def getNextInstr(self):

        # int() to guard against float
        instr = chr(int(self.codebox[self.ipY][self.ipX]))

        return instr

    def dbgPrintStack(self):

        logging.debug("Stack: {0}\n".format(str(self.stackRegList[-1].stack)))

    def dbgPrintInstr(self):

        self.instrCount += 1

        try:

            logging.debug("Instr: [{0}] N: {1}".format(chr(self.codebox[self.ipY][self.ipX]),self.instrCount))

        except TypeError:

            logging.debug("Instr: [{0}] N: {1}".format(self.codebox[self.ipY][self.ipX],self.instrCount))
            

    def run(self):

        
        while (not self.endExec):


            instr = self.getNextInstr()

            #self.dbgPrintInstr()
            
            if (self.stringQuote and instr != "'") or (self.stringDbQuote and instr != "\""):

                if instr == "\0":
                    
                    self.pushStack(ord(" "))

                else:

                    self.pushStack(ord(instr))         
            
            else:

                nextInstruction = self.instructionTable.get(instr,self.invalidInstruction)
                nextInstruction()

            #self.dbgPrintStack()
            self.updateIP()

            
            

class ParseInitialStack(argparse.Action):

    def __call__(self,parser,namespace,values,option_string):

        parsedList = []

        if option_string == "-v":

            parsedList = values

        else:

            parsedList = [ord(ch) for arg in values for ch in arg]


        setattr(namespace,self.dest,getattr(namespace,self.dest) + parsedList)
        


def initArgparse():

    parser = argparse.ArgumentParser(usage = "<script> [options]")
    parser.add_argument("script",metavar = "<script>",help = "Script to execute")
    
    parser.add_argument("-v",action = ParseInitialStack,nargs = "+",type = float,default = [],metavar = "<number>",
                        dest = "initialStack",help = "Specify initial integer values on top of the stack")
    
    parser.add_argument("-s",action = ParseInitialStack,nargs = "+",type = str,default = [],metavar = "<string>",
                        dest = "initialStack",help = "Specify initial character values on top of the stack")
    
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

            codebox.append([ord(ch) if ch != " " else 0 for ch in line] + [0] * (maxLine - len(line)))

    return codebox


def main():

    try:

        #logging.basicConfig(filename = "fish.log",level = logging.DEBUG,filemode = "w")

        parser = initArgparse()
        args = parser.parse_args()

        codebox = parseScript(args.script)

        interpreter = Interpreter(codebox,args.initialStack)

        interpreter.run()

        print()

    
    except OSError as err:

        print("Error: Could not open the script: \"{0}\" ".format(err.filename)
              , file = sys.stderr)

    except FishError:

        print("Something smells fishy", file = sys.stderr)
        #logging.debug(traceback.format_exc())

    except KeyboardInterrupt:
        pass
    
        

if __name__ == "__main__":
    main()
    
