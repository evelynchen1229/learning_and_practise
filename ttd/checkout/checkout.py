import math
class Checkout:
    class Discount:
        def __init__(self,nbrItem,price):
            self.nbrItem = nbrItem
            self.price = price
    
    def __init__(self):
        self.prices = {}
        self.discounts = {}
        self.items = {}
        self.total = 0
    
    def addDiscount(self,item,nbrItem,price):
        discount = self.Discount(nbrItem,price)
        self.discounts[item] = discount      

    def addItemPrice(self,item,price):
        self.prices[item] = price

    def addItem(self,item):
        if item in self.items:
            self.items[item] += 1
        else:
            self.items[item] = 1

    def caculateTotal(self):
        for item,cnt in self.items.items():
            if item in self.discounts:
                discount = self.discounts[item]
                if cnt >= discount.nbrItem:
                    nbrDiscount = math.floor(cnt/discount.nbrItem)
                    self.total += nbrDiscount * discount.price
                    remaining = cnt%discount.nbrItem
                    self.total += remaining * self.prices[item]
                else:
                    self.total = cnt * self.prices[item]
            else:
                self.total += cnt * self.prices[item]
        return self.total


