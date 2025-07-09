from paquetes.order import Order
from paquetes.menu_item import MainCourse, Drinks, Dessert


from collections import namedtuple
from queue import Queue
import random
import json


class MenusManager:
  def __init__(self, menu_jsons=None):
    self.main_course = []
    self.desserts = []
    self.drinks = []
    self.menu = {
      "main_course": self.main_course,
      "desserts": self.desserts,
      "drinks": self.drinks
    }
    if menu_jsons is not None:
      self.menu_jsons = menu_jsons
    else:
      self.menu_jsons = {
        'main_course': 'paquetes/main_course.json',
        'desserts': 'paquetes/desserts.json',
        'drinks': 'paquetes/drinks.json'
      }
    self.item = namedtuple("MenuItem", ["Nombre", "Precio"])
    self._initialize_menus()

  def _initialize_menus(self):
    try:
      for key in self.menu_jsons:
        self.menu[key].clear()  # Limpiar la lista antes de llenarla
        with open(self.menu_jsons[key], "r", encoding="utf-8") as i:
          items = json.load(i)
          for item_dict in items:
            self.menu[key].append(
              self.item(item_dict["Nombre"], item_dict["Precio"])
            )
    except FileNotFoundError:
      print(f"Archivo no encontrado.")
    except json.JSONDecodeError:
      print(f"Error al decodificar el archivo JSON.")

  def delete_item(self):
    print("De que categoria desea eliminar un elemento? (main_course, desserts, drinks)")
    lista_nombre = input("Ingrese el nombre de la lista: ").strip()
    if lista_nombre not in self.menu:
      print("Nombre de lista invalido.")
      return
    lista = self.menu[lista_nombre]
    for numero, item in enumerate(lista):
      print(f"{numero}. {item.Nombre}")
    try:
      item_eliminar = int(input("Ingrese el numero del elemento a eliminar: "))
      eliminado = lista.pop(item_eliminar)
      # No reasignar: self.menu[lista_nombre] = lista  # Esto rompe la referencia
      json_file = self.menu_jsons.get(lista_nombre)
      if json_file:
        try:
          with open(json_file, "r", encoding="utf-8") as d:
            items = json.load(d)
          items = [i for i in items if not (i["Nombre"] == eliminado.Nombre and i["Precio"] == eliminado.Precio)]
          with open(json_file, "w", encoding="utf-8") as d:
            json.dump(items, d, ensure_ascii=False, indent=2)
        except Exception as error:
          print(f"Error al actualizar el archivo JSON: {error}")
      print(f"item {item_eliminar} ha sido eliminado")
    except (IndexError, ValueError):
      print("Entrada invalida. El item no se pudo eliminar.")

  def change_item(self): 
    print("De que categoria desea cambiar el precio?" \
      " (main_course, desserts, drinks)")
    lista_nombre = input("Ingrese el nombre de la lista: ").strip()
    if lista_nombre not in self.menu:
      print("Nombre de lista invalido.")
      return
    lista = self.menu[lista_nombre]
    for numero, item in enumerate(lista):
      print(f"{numero}. {item.Nombre}")
    item_cambiar = int(input("Ingrese el numero del elemento a cambiar: "))
    try:
      json_file = self.menu_jsons.get(lista_nombre)
      if json_file:
        try:
          with open(json_file, "r", encoding="utf-8") as c:
            items = json.load(c)
            nuevo_precio = float(input("Ingrese el nuevo precio: "))
            items[item_cambiar]["Precio"] = nuevo_precio
            with open(json_file, "w", encoding="utf-8") as c:
                json.dump(items, c, ensure_ascii=False, indent=2)
            lista[item_cambiar] = self.item(lista[item_cambiar].Nombre, nuevo_precio)
        except Exception as error:
          print(f"Error al actualizar el archivo JSON: {error}")
      return True
    except ValueError:
      print("Entrada invalida.")
    return False
  
  def agregar_nuevo_item(self):
    print("De que categoria desea agregar un item?" \
          " (main_course, desserts, drinks)"
          )
    lista_nombre = input("Ingrese el nombre de la lista: ").strip()
    if lista_nombre not in self.menu:
      print("Nombre de lista invalido.")
      return
    lista = self.menu[lista_nombre]
    print(f"items en {lista_nombre}:\n\n")
    for numero, item in enumerate(lista):
      print(f"{numero}. {item.Nombre}")
    try:
      json_file = self.menu_jsons.get(lista_nombre)
      if json_file:
        try:
          with open(json_file, "r", encoding="utf-8") as c:
            items = json.load(c)
            nombre = input("Ingrese el nombre: ")
            precio = float(input("Ingrese el  precio: "))
            nuevo_item = {"Nombre": nombre, "Precio": precio}  # Claves corregidas
            items.append(nuevo_item)
            with open(json_file, "w", encoding="utf-8") as c:
                json.dump(items, c, ensure_ascii=False, indent=2)
        except Exception as error:
          print(f"Error al actualizar el archivo JSON: {error}")
      return True
    except ValueError:
      print("Entrada invalida.")
    return False
  
  def revisar_jsons(self):
    self._initialize_menus()
    print("De que categoria desea revisar el json?" \
          " (main_course, desserts, drinks)"
          )
    lista_nombre = input("Ingrese el nombre de la lista: ").strip()
    if lista_nombre not in self.menu:
      print("Nombre de lista invalido.")
      return
    lista = self.menu[lista_nombre]
    print(f"items en {lista_nombre}:\n\n")
    for numero, item in enumerate(lista):
      print(f"{numero}. {item.Nombre}")

  def crear_objetos_menu(self):
      return (
        MainCourse("plato_principal", 0, self.menu.get("main_course")),
        Drinks("bebidas", 0, self.menu.get("drinks")),
        Dessert("postres", 0, self.menu.get("desserts"))
      )

  def inicialice_restaurant(self):
    cola_fifo_principal = Queue(10) # Cola para cosas pesadas / ordenes caras
    cola_fifo_secundaria = Queue(20) # pocos elementos por orden / ordenes barata
    plato_principal, bebidas, postres = self.crear_objetos_menu()
    print("Bienvenido al Restaurante")
    while True:
      print("\n\n OPCIONES: \n\n")
      print("1. Hacer una orden")
      print("2. Simular llegada aleatoria de clientes")
      print("3. Ver estado de la cola")
      print("4. Procesar orden de la cola")
      print("5. Agregar/eliminar/modificar items")
      print("6. Salir\n\n")
      try:
        opcion = int(input("Seleccione una opcion: "))
      except ValueError:
        print("\n\nPor favor ingrese un número válido.")
        continue
      if opcion == 1:
        if not self.menu['main_course'] or not self.menu['drinks'] or not self.menu['desserts']:
          self._initialize_menus()
          plato_principal, bebidas, postres = self.crear_objetos_menu()
        order = Order(plato_principal, bebidas, postres)
        orden = order.chosse_order()
        if len(orden) > 10:
          cola_fifo_principal.put(orden)
        else:
          cola_fifo_secundaria.put(orden)
      elif opcion == 2:
        for _ in range(2):  # Simular clientes
          random_value = random.uniform(0, 1)
          print(f"Probabilidad: {random_value:.3f}")
          if random_value > 0.8: 
            print("spawneo un cliente")
            if not self.menu['main_course'] or not self.menu['drinks'] or not self.menu['desserts']:
              self._initialize_menus()
              plato_principal, bebidas, postres = self.crear_objetos_menu()
            order = Order(plato_principal, bebidas, postres)
            order.chosse_order()
            orden = order.chosse_order()
            if len(orden) > 10:
              cola_fifo_principal.put(orden)
            else:
              cola_fifo_secundaria.put(orden)
          else:
            print("Ningun cliente llego esta vez.")              
      elif opcion == 3:
        print(f"Ordenes en cola: {cola_fifo_principal.qsize()}/{cola_fifo_principal.maxsize}")      
      elif opcion == 4:
        if not cola_fifo_principal.empty():
          orden_procesada = cola_fifo_principal.get()
          process_orders = len(orden_procesada)
          print(f"Procesando orden con {process_orders} elementos...")
          for i in range(process_orders):
            print("procesando orden...")
          print("Orden completada y entregada.")
        else:
          print("No hay ordenes en la cola para procesar.")
      elif opcion == 5:
        print("que desea hacer?"\
              "\n 1. modificar" \
              "\n 2. agregar" \
              "\n 3. eliminar" \
              "\n 4. revisar jsons"
              )
        seleccion = int(input("ingresar opcion:"))
        if seleccion == 1:
          self.change_item()
        elif seleccion == 2:
          self.agregar_nuevo_item()
        elif seleccion == 3:
          self.delete_item()
        elif seleccion == 4:
          self.revisar_jsons()
        else:
          print("Opcion invalida.")
      elif opcion == 6:
        print("Gracias por visitarnos")
        break
      else:
        print("Opcion invalida. Seleccione un número del 1 al 5.")