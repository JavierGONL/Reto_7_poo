# Definimos la clase MenuItem como la clase base para los elementos del menu
class MenuItem:
  def __init__(self, name, price):
    self.name = name  # Nombre del elemento
    self.price = price  # Precio del elemento 
  
  # Calcula el precio total segun la cantidad
  def total_price(self, number_of_items):
    return self.price * number_of_items

# Clase para los platos principales
class MainCourse(MenuItem):
  def __init__(self, name:str, price:int, course_list:list):
    super().__init__(name, price)
    self._maincourse_list = course_list  # Lista de platos principales disponibles
  
  def get_maincourse_list(self):
    if not self._maincourse_list:
      print("No hay platos principales disponibles.")
    else:
      for idx, i in enumerate(self._maincourse_list, 1):
        print(f"{idx}. {i.Nombre} ${i.Precio}")

# Clase para las bebidas
class Drinks(MenuItem):
  def __init__(self, name:str, price:int, drink_list:list):
    super().__init__(name, price)
    self._drink_list = drink_list # Lista de bebidas disponibles
  
  def get_drinks_list(self):
    if not self._drink_list:
      print("No hay bebidas disponibles.")
    else:
      for idx, i in enumerate(self._drink_list, 1):
        print(f"{idx}. {i.Nombre} ${i.Precio}")

# Clase para los postres
class Dessert(MenuItem):
  def __init__(self, name:str, price:int, dessert_list:list):
    super().__init__(name, price)
    self._dessert_list = dessert_list  # Lista de postres disponibles
  
  def get_dessert_list(self):
    if not self._dessert_list:
      print("No hay postres disponibles.")
    else:
      for idx, i in enumerate(self._dessert_list, 1):
        print(f"{idx}. {i.Nombre} ${i.Precio}")
