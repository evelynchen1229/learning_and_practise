class Format:
    def __init__(self,argument1,argument2=""):
        self.argument1 = argument1
        self.argument2 = argument2

    def get_argument(self):
        return (self.argument1 + self.argument2)

    def div(self):
        text = self.get_argument()
        return f"<div>{text}</div>"

    def p(self):
        text = self.get_argument()
        return f"<p>{text}</p>"


    def span(self):
        text = self.get_argument()
        return f"<span>{text}</span>"


    def h1(self):
        text = self.get_argument()
        return f"<h1>{text}</h1>"



'''part 1'''
#test = Format("foo")
test = Format("foo","bar")
print(test.div())
print(test.p())
print(test.span())
print(test.h1())
# print(Format.div("foo")) error message: str doesn't have attribute get_argument

'''part 2'''

class div(Format):
    def __init__(self, argument1,argument2=""):
        Format.__init__(self, argument1, argument2="")
        #super().__init__(self,argument)

    def p(self):
        text = self.get_argument()
        return f"<div><p>{text}</p><div>"
  #  def p.span(self):
  #      text = self.get_argument()
  #      return "<div><p><span>text</span></p></div>"



test = div("foo")
print(test.p())
#print(test.p.span())
