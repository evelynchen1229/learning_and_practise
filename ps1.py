## part A - House Hunting: how long to save enough deposit
#import numpy
#import matplotlib
#
#total_cost = float(input("what's the cost of your dream house? "))
#portion_down_payment = 0.25
#deposit = total_cost * portion_down_payment
#annual_salary = float(input("what's your annual salary? "))
#portion_saved = float(input("how much % would you save? decimal number please: "))
#monthly_salary = annual_salary/12
#r = 0.04 #annual_retun
#
#month = 0
#current_saving = 0
##should loop until current saving is enough for the deposit
#
#while current_saving < deposit:
#
#  current_saving = current_saving * (1 + r/12) + monthly_salary * portion_saved
#  #by the end oh month_0,the beginning of month_1
#
#  month += 1
#  if month > 200:
#    break
#
##print (month)
##print(current_saving)
#
#
##part b - saving with a raise: salary rises every 6 months
#
#total_cost = float(input("what's the cost of your dream house? "))
#portion_down_payment = 0.25
#deposit = total_cost * portion_down_payment
#annual_salary = float(input("what's your annual salary? "))
#portion_saved = float(input("how much % would you save? decimal number please: "))
#monthly_salary = annual_salary/12
#r = 0.04 #annual_retun
#
#semi_annual_raise = float(input("what the % pay rise? (decimal) "))
#
#
#month = 0
#current_saving = 0
##should loop until current saving is enough for the deposit
#
#while current_saving < deposit:
#  if month % 6 == 0 and month >0:
#    monthly_salary = monthly_salary * (1 + semi_annual_raise)
#
#  current_saving = current_saving * (1 + r/12) + monthly_salary * portion_saved
#  #by the end oh month_0,the beginning of month_1
#
#  month += 1
#  if month > 300:
#    break
#
##print (month)
##print(current_saving)
#
##part c: finding the right amount to save away bisection search

try:
  print("let's see whether you can get a $1m house in three years\n")
  annual_salary = int(input("how much do you earn per year? "))
  def comparison(saving_portion): # return the different between deposit - current_saving
  #get current saving in 3 years
    month = 0
    deposit = 1000000*.25
    monthly_salary =annual_salary/12
    current_saving = 0
    while current_saving < deposit:
      if month % 6 == 0 and month >0:
          monthly_salary = monthly_salary* (1 + .07)
      current_saving = current_saving * (1 + .04/12) + monthly_salary * (int(saving_portion))/10000
      month += 1
    #    print(month)
     #   print(monthly_salary)
      if month > 35:
        break
    diff = int(current_saving - deposit)
  #  print(diff)
    #print(current_saving)
    #print(month)
    #print(saving_portion)
   # print(diff)

    return diff


  def saving_rate(saving_per = 5000, step=1,high=10000,low=0):
    compare_point = comparison(saving_per)
  #  print('compare_point', compare_point)

    if compare_point >= 0 and compare_point <= 100:
      result = str(int(saving_per)/100) + "%"
      #return {"monthly saving portion": result, "steps": step}
      print("\nYes you can as long as you have monthly saving portion shown below\n")

      return result

    if compare_point > 10:
      new_high = saving_per
      new_saving_per = (low + new_high) / 2
      #forgot to use "new_high", same with "new_low" below - results in duplicating calculation steps;

      return saving_rate(new_saving_per, step + 1, new_high, low)

    new_low = saving_per
    new_saving_per = (new_low + high) / 2

    return saving_rate(new_saving_per, step + 1, high, new_low)


  a = saving_rate()
  print(a)

except RecursionError :
  if  annual_salary < 1000000:
    print("\nThere's no way you can get a $1m house with your salary man.")
  else:
    print("\nMan, not even joking, less than a year mate!!!!")
#the codes below returns "None" because of parameter names being mutated for the new values
# should assign new variable names if the diffult value has changed

#if 0 <= compare_point and compare_point <= 100:
  #  result=int(saving_per)
  #  print('saving_per', result)
  #  return str(result)
  #elif compare_point > 10: #saving rate being too high
  #  high = saving_per
  #  saving_per = (low+high)/2
  #  step +=1
  #  saving_rate(saving_per,step,high,low)
  #else: # saving rat being too low
  #  low = saving_per
  #  saving_per = (low+high)/2
  #  step +=1
  #  saving_rate(saving_per,step,high,low)



