import re

def body (tag, text):
  if ">" not in text:
    new_body = f"<{tag}>" + text + f"</{tag}>"

  else:
    match = re.search(">(\w+)",text)
    if match:
      string = str(match.group(1))
      new_str = text.split(string)
      new_body = new_str[0] + f"<{tag}>" + string + f"</{tag}>" + new_str[-1]

  return new_body

def getter(code):
  return code.get_argument()

class Format:
    def __init__(self,argument1,argument2=""):
        self.argument1 = argument1
        self.argument2 = argument2

    def get_argument(self):
        #text = self.get_argument()
        return (self.argument1 + self.argument2)
      # can I/ how do I use *args with getter?

    @property
    def div(self):
        text = self.get_argument()
        new_text = body("div",text)
        return Format(new_text)

    @property
    def p(self):
        text = self.get_argument()
        new_text = body("p",text)
        return Format(new_text)


    @property
    def span(self):
        text = self.get_argument()
        new_text = body("span",text)
        return Format(new_text)


    @property
    def h1(self):
        text = self.get_argument()
        new_text = body("h1",text)
        return Format(new_text)


'''part 1'''
#test = Format("foo")
test = Format("foo","bar")
print(getter(test.div.p))
#print(test.div.p.span())
#print(test.p())
#print(test.span())
#print(test.h1())
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
#print(test.p())
#print(test.p.span())
test = div("foo","bar")
print(test.p())
#print(test.p.span())




