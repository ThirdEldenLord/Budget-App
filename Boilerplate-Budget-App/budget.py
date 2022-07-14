class Category:
  def __init__(self, name):
    self.name = name
    self.ledger = []
    self.Cash = 0

  def __str__(self):
    title = self.name.center(30, "*") + "\n"
    the_list = ""
    for item in self.ledger:
      the_amount = "{:>7.2f}".format(item["amount"])
      the_description = "{:<23}".format(item["description"])
      the_list += "{}{}\n".format(the_description[:23], the_amount[:7])
    total = "Total: {:.2f}".format(self.Cash)  
    return title + the_list + total

  def deposit(self, amount, description = ""):
    self.ledger.append({"amount": amount, "description": description})
    self.Cash = self.Cash + amount

  def withdraw(self, amount, description = ""):
    if self.Cash > amount:
      self.ledger.append({"amount": -amount, "description": description})
      self.Cash = self.Cash - amount
      return True
    else:
      return False  

  def get_balance(self):
    return self.Cash 
    
  def transfer(self, amount, another_category):
    if self.Cash > amount:
      self.withdraw(amount, "Transfer to " + another_category.name)
      another_category.deposit(amount, "Transfer from " + self.name)
      return True
    else:
      return False  

  def check_funds(self, amount):
    if amount > self.Cash:
      return False
    else:
      return True 
  
def create_spend_chart(categories):
  all_spents = []
  for category in categories:
    spent = 0
    for item in category.ledger:
      if item["amount"] < 0:
        spent = spent + abs(item["amount"])
    all_spents.append(round(spent, 2))

  total_spent = round(sum(all_spents), 2)
  spent_percentage = list(map(lambda amount: int((((amount / total_spent) * 10) // 1) * 10), all_spents))

  title = "Percentage spent by category\n"
  chart = ""
  for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        for percent in spent_percentage:
            if percent >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

  footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
  descriptions = list(map(lambda category: category.name, categories))
  max_length = max(map(lambda description: len(description), descriptions))
  descriptions = list(map(lambda description: description.ljust(max_length), descriptions))
  for x in zip(*descriptions):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

  return (title + chart + footer).rstrip("\n")