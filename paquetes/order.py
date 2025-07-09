from paquetes.menu_item import MainCourse,Drinks,Dessert
from paquetes.pagos import Efectivo, Tarjeta

from copy import deepcopy

# Clase que representa la orden del cliente
class Order:
  def __init__(self, main_course_list, drinks_list, dessert_list):
    self.main_course : "MainCourse" =  main_course_list  # Objeto con la lista de platos principales
    self.drink : "Drinks" = drinks_list  # Objeto con la lista de bebidas
    self.dessert : "Dessert" =  dessert_list  # Objeto con la lista de postres
    self.order_total_price = 0  # Precio total acumulado
    self.seleccion = []  # Elementos seleccionados por el usuario

  # Permite al usuario elegir un plato principal
  def _choose_main_course(self):
    lista = self.main_course._maincourse_list
    while True:
      self.main_course.get_maincourse_list()
      try:
        seleccion_1 = int(input("Que desea? "+ " \n(0 para volver): \n-->"))
        if seleccion_1 == 0:
          break
        if 1 <= seleccion_1 <= len(lista):
          item = lista[seleccion_1 - 1]
          self.seleccion.append(MainCourse(item.Nombre, item.Precio, lista))
        else:
          print("Ingrese un numero valido de la lista.")
      except ValueError:
        print("Por favor ingrese un numero.")

  # Permite al usuario elegir una bebida
  def _choose_drink(self):
    lista = self.drink._drink_list
    while True:
      self.drink.get_drinks_list()
      try:
        seleccion_1 = int(input("Que desea? "+ " \n(0 para volver): \n-->"))
        if seleccion_1 == 0:
          break
        if 1 <= seleccion_1 <= len(lista):
          item = lista[seleccion_1 - 1]
          self.seleccion.append(Drinks(item.Nombre, item.Precio, lista))
        else:
          print("Ingrese un numero valido de la lista.")
      except ValueError:
        print("Por favor ingrese un numero.")

  # Permite al usuario elegir un postre
  def _choose_dessert(self):
    lista = self.dessert._dessert_list
    while True:
      self.dessert.get_dessert_list()
      try:
        seleccion_1 = int(input("Que desea? "+ " \n(0 para volver): \n-->"))
        if seleccion_1 == 0:
          break
        if 1 <= seleccion_1 <= len(lista):
          item = lista[seleccion_1 - 1]
          self.seleccion.append(Dessert(item.Nombre, item.Precio, lista))
        else:
          print("Ingrese un numero valido de la lista.")
      except ValueError:
        print("Por favor ingrese un numero.")

  # Menu principal para que el usuario agregue productos a la orden
  def chosse_order(self):
    # Reiniciar la selección para una nueva orden
    self.seleccion = []
    self.order_total_price = 0
    while True:
      if len(self.seleccion) > 20:
        print("muchas ordenes")
        break
      seleccion_2 = input(
        "Que le gustaria agregar a la orden? \n 1. Plato principal \n" \
        " 2. Bebida \n 3. Postre"
        " (si desea terminar la orden escriba 0) \n-->"
      )
      if seleccion_2 == "1":
        self._choose_main_course()
      elif seleccion_2 == "2":
        self._choose_drink()
      elif seleccion_2 == "3":
        self._choose_dessert()
      elif seleccion_2 == "0":
        if self.seleccion:
          self._get_factura()
          self._procesar_pago()
          return self.seleccion.deepcopy()
        else:
          print("No ha seleccionado ningún elemento.")
        break
      else:
        print("Ingrese una opcion valida.")

  # Calcula y muestra la factura final, aplicando descuentos si corresponde
  def _get_factura(self):
    n_bebidas = 0
    n_maincourse = 0
    n_desserts = 0
    print("\n\n___________Factura___________\n\n".center(30))
    # Calcular precio base y contar elementos
    for i in self.seleccion:
      if type(i) == Drinks:
        n_bebidas += 1
      elif type(i) == MainCourse:
        n_maincourse += 1
      elif type(i) == Dessert:
        n_desserts += 1
      print(f"{self.seleccion.index(i)+1}: {i.Nombre} - ${i.Precio}")
      self.order_total_price += i.Precio
    print(f"\nSubtotal: ${self.order_total_price}")
    # Aplicar descuentos según la cantidad de productos
    descuento_total = 0
    if n_bebidas >= 5 or n_maincourse >= 5 or n_desserts >= 10:
      print("\n\n___________Descuentos___________\n\n".center(30))
      if n_bebidas >= 5:
        descuento_bebidas = self.order_total_price * (5/100)
        descuento_total += descuento_bebidas
        print(f"Descuento cantidad de bebidas (5%): -{descuento_bebidas:.2f}")
      if n_maincourse >= 5:
        descuento_platos = self.order_total_price * (10/100)
        descuento_total += descuento_platos
        print(f"Descuento cantidad de platos principales (10%): -{descuento_platos:.2f}")
      if n_desserts >= 10:
        descuento_postres = self.order_total_price * (5/100)
        descuento_total += descuento_postres
        print(f"Descuento cantidad de postres (5%): -{descuento_postres:.2f}")  
      self.order_total_price -= descuento_total     
    print(f"\n\nCANTIDAD A PAGAR: ${self.order_total_price:.2f}")

  # Procesa el pago de la orden
  def _procesar_pago(self, mi_tarjeta:"Tarjeta"):
    print("\n¿Cómo desea pagar?")
    print("1. Tarjeta")
    print("2. Efectivo")
    try:
      opcion = int(input("Seleccione una opción: "))
      if opcion == 1:
        mi_tarjeta.pagar(self.order_total_price)
      elif opcion == 2:
        try:
          monto_entregado = float(input(f"Ingrese el monto en efectivo (Total: ${self.order_total_price:.2f}): "))
          efectivo = Efectivo(monto_entregado)
          efectivo.pagar(self.order_total_price)
        except ValueError:
          print("Monto invalido. No se pudo procesar el pago.")
      else:
        print("Opcion invalida. No se procesó el pago.")
    except ValueError:
      print("Opción inválida. No se procesó el pago.")