import getopt
import sys

import lexer
import parser

def print_help():
    pass

try:
    opts, args = getopt.gnu_getopt(
        args = sys.argv,
        shortopts = "hi:o:",
        longopts = ["ifile=","ofile=", "help"])

except getopt.GetoptError:
    pass

tstream = lexer.screen(lexer.lex("""\
trait Furry <F>
    def furriness -> F

class Animal
    def name -> string
    def action

// () not needed, added for clarity
class Cat (var _name = "Kitty") extends Animal with Furry<int>

    // Class methods have an implicit self pointer
    // Secondary constructor
    init def str _name, boo
        init(_name)
        print(_name, boo)

    def name = _name

    // Literally the same as
    // def name self = self._name

    def furriness = 20

    def action
        print $"Meow $furriness"

// Static methods and variables
var Cat.baz = "Foo"

def Cat.foo str bar
    print (bar)

// accessors
get var foo
    // code here

// get bar
// get int baz

set var foo v
    // code here

"""))

for token in tstream:
    print(str(token).replace("\n", "\\n"))


