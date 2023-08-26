class foo:

    _y = 5
    __z = 15


    def __init__(self):
        self.x = 10

    def outp(self):  # TypeError: Method must have 'self'-like variable as first argument, self is always given
        print(self.x)

    def myfunc(self):
        print("stuff")

class bar(foo):
    def __init__(self):
        y = 25

    def sum(self):
        self.x + self.y

class person():
    def __init__(self,name):
        name = self.name

    def say_my_name(self):
        print("My name is, My name is "+self.name)
        

def ex1():
    # NameError:TypeError
    x = int(input("Please enter a number you wish to find the square of :-"))
    print(x * x)


def ex2():
    # NameError:
    y = input("Please enter a word :-")
    x = input("Please enter the word you wish to be added :-")
    print(y+x)


def ex3():
    # ZeroDivisionError:
    print(5/1)


def ex4():
    # FileNotFoundError:
    f = open("scores.txt")
    f.close()


def ex5():
    print("What shall we play today?")


def exF(x):
    #Factorial Function
    # TypeError: ex5() used accidentally, so no arguments expected
    # RecursionError: no non-recurring return value
    if x == 1:
        return 1
    else:
        return x*exF(x-1)


def exO1():
    #what are the OOP errors here?
    Foo = foo()  #UnboundLocalError: Instance name is same name as class, so instance name referenced before assignment
    Foo.outp()


def exO2():
    #What is the error here - why does it occur?
    foo2 = foo()
    print(foo2.__z)


def exO3():
    #What is the error here - what do you need to do to get x to be accessible?
    bar_foo = bar()
    print(bar.x)

def exO4():
    #This doesn't crash, but what does it do?
    bar_foo2 = bar()
    print(bar_foo2.sum)


def exO5():
    #The class is in the code - why wont it work?
    myclass = newClass()


def exO6():
    #You know the drill by now - whats wrong?
    bob = person("Bob")
    rob = Person("Rob")
    dob = person("Dobbie")
    people = [bob,rob,dob]
    for individual in people:
        individual.say_my_name()
    #oh and what fancy things is this bit at the end doing?


#ex1()
#ex2()
#ex3()
#ex4()
#print(exF(6))
#exO1()  # NameError: 'O' not '0' (Zero)
print(foo()._y)
exO2()
#exO3()
#exO4()
#exO5()
#exO6()

class newClass:
    def __init__(self):
        self.x = 100

