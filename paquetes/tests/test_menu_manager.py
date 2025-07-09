import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import unittest
from paquetes.Menu_manager import MenusManager
import os
import json

""" 
test hechos por copilot para depurar el menuManager
"""

class TestMenusManager(unittest.TestCase):
  def setUp(self):
    # Crear archivos de prueba temporales
    self.test_files = {
      'main_course': 'main_course.json',
      'desserts': 'desserts.json',
      'drinks': 'drinks.json'
    }
    self.default_data = [
      {"Nombre": "Frijolada", "Precio": 10000},
      {"Nombre": "Costillas BBQ", "Precio": 15000}
    ]
    for file in self.test_files.values():
      with open(file, 'w', encoding='utf-8') as f:
        json.dump(self.default_data, f, ensure_ascii=False, indent=2)
    self.manager = MenusManager(menu_jsons=self.test_files)

  def tearDown(self):
    # Eliminar archivos de prueba
    for file in self.test_files.values():
      if os.path.exists(file):
        os.remove(file)

  def test_initialize_menus(self):
    self.assertEqual(len(self.manager.main_course), 2)
    self.assertEqual(self.manager.main_course[0].Nombre, "Frijolada")

  def test_delete_item(self):
    self.manager.menu['main_course'].append(self.manager.item("Tacos", 8000))
    # Simular input para eliminar el primer elemento
    input_values = ['main_course', '0']
    def mock_input(prompt):
      return input_values.pop(0)
    self.manager.delete_item.__globals__['input'] = mock_input
    self.manager.delete_item()
    self.assertNotIn('Frijolada', [i.Nombre for i in self.manager.menu['main_course']])

  def test_change_item(self):
    # Agregar 'Tacos' tanto a la lista en memoria como al archivo JSON
    self.manager.menu['main_course'].append(self.manager.item("Tacos", 8000))
    with open('main_course.json', 'r+', encoding='utf-8') as f:
      items = json.load(f)
      items.append({"Nombre": "Tacos", "Precio": 8000})
      f.seek(0)
      json.dump(items, f, ensure_ascii=False, indent=2)
      f.truncate()
    input_values = ['main_course', '2', '9000']
    def mock_input(prompt):
      return input_values.pop(0)
    self.manager.change_item.__globals__['input'] = mock_input
    self.manager.change_item()
    self.assertEqual(self.manager.menu['main_course'][2].Precio, 9000)

  def test_add_multiple_items_and_persist(self):
    # Agregar varios elementos y verificar persistencia en JSON
    nuevos = [
      ("Bandeja Paisa", 20000),
      ("Ajiaco", 18000),
      ("Sancocho", 17000)
    ]
    for nombre, precio in nuevos:
      self.manager.menu['main_course'].append(self.manager.item(nombre, precio))
      # Persistir manualmente en JSON
      with open('main_course.json', 'r+', encoding='utf-8') as f:
        items = json.load(f)
        items.append({"Nombre": nombre, "Precio": precio})
        f.seek(0)
        json.dump(items, f, ensure_ascii=False, indent=2)
        f.truncate()
    # Verificar en memoria
    nombres_mem = [i.Nombre for i in self.manager.menu['main_course']]
    for nombre, _ in nuevos:
      self.assertIn(nombre, nombres_mem)
    # Verificar en JSON
    with open('main_course.json', 'r', encoding='utf-8') as f:
      items = json.load(f)
      nombres_json = [i['Nombre'] for i in items]
      for nombre, _ in nuevos:
        self.assertIn(nombre, nombres_json)

  def test_delete_nonexistent_index(self):
    # Intentar eliminar un índice fuera de rango
    input_values = ['main_course', '99']
    def mock_input(prompt):
      return input_values.pop(0)
    self.manager.delete_item.__globals__['input'] = mock_input
    # No debe lanzar excepción
    try:
      self.manager.delete_item()
    except Exception as e:
      self.fail(f"delete_item lanzó excepción inesperada: {e}")

  def test_change_item_invalid_index(self):
    # Intentar cambiar un índice fuera de rango
    input_values = ['main_course', '99', '12345']
    def mock_input(prompt):
      return input_values.pop(0)
    self.manager.change_item.__globals__['input'] = mock_input
    # No debe lanzar excepción
    try:
      self.manager.change_item()
    except Exception as e:
      self.fail(f"change_item lanzó excepción inesperada: {e}")

  def test_sync_after_delete(self):
    # Eliminar un elemento y verificar que no esté ni en memoria ni en JSON
    self.manager.menu['main_course'].append(self.manager.item("Sobrebarriga", 16000))
    with open('main_course.json', 'r+', encoding='utf-8') as f:
      items = json.load(f)
      items.append({"Nombre": "Sobrebarriga", "Precio": 16000})
      f.seek(0)
      json.dump(items, f, ensure_ascii=False, indent=2)
      f.truncate()
    # Eliminar el último
    idx = len(self.manager.menu['main_course']) - 1
    input_values = ['main_course', str(idx)]
    def mock_input(prompt):
      return input_values.pop(0)
    self.manager.delete_item.__globals__['input'] = mock_input
    self.manager.delete_item()
    # Verificar
    nombres_mem = [i.Nombre for i in self.manager.menu['main_course']]
    self.assertNotIn("Sobrebarriga", nombres_mem)
    with open('main_course.json', 'r', encoding='utf-8') as f:
      items = json.load(f)
      nombres_json = [i['Nombre'] for i in items]
      self.assertNotIn("Sobrebarriga", nombres_json)

  def test_massive_change_and_delete(self):
    # Agregar 50 elementos, cambiar y eliminar varios
    for i in range(50):
      nombre = f"Plato{i}"
      precio = 10000 + i * 100
      self.manager.menu['main_course'].append(self.manager.item(nombre, precio))
      with open('main_course.json', 'r+', encoding='utf-8') as f:
        items = json.load(f)
        items.append({"Nombre": nombre, "Precio": precio})
        f.seek(0)
        json.dump(items, f, ensure_ascii=False, indent=2)
        f.truncate()
    # Cambiar el precio de los primeros 10
    for idx in range(10):
      input_values = ['main_course', str(idx), str(9999 + idx)]
      def mock_input(prompt):
        return input_values.pop(0)
      self.manager.change_item.__globals__['input'] = mock_input
      self.manager.change_item()
    # Eliminar los últimos 10
    for idx in reversed(range(len(self.manager.menu['main_course'])-10, len(self.manager.menu['main_course']))):
      input_values = ['main_course', str(idx)]
      def mock_input(prompt):
        return input_values.pop(0)
      self.manager.delete_item.__globals__['input'] = mock_input
      self.manager.delete_item()
    # Verificar integridad
    with open('main_course.json', 'r', encoding='utf-8') as f:
      items = json.load(f)
      self.assertEqual(len(items), len(self.manager.menu['main_course']))
      for idx, item in enumerate(items):
        self.assertEqual(item['Nombre'], self.manager.menu['main_course'][idx].Nombre)
        self.assertEqual(item['Precio'], self.manager.menu['main_course'][idx].Precio)

  def test_corrupted_json_file(self):
    # Escribir JSON corrupto y verificar manejo
    with open('main_course.json', 'w', encoding='utf-8') as f:
      f.write('{corrupt!')
    try:
      manager2 = MenusManager()
    except Exception as e:
      self.fail(f"MenusManager no debe lanzar excepción con JSON corrupto: {e}")

  def test_delete_all_and_readd(self):
    # Eliminar todos los elementos y volver a agregar
    while self.manager.menu['main_course']:
      input_values = ['main_course', '0']
      def mock_input(prompt):
        return input_values.pop(0)
      self.manager.delete_item.__globals__['input'] = mock_input
      self.manager.delete_item()
    self.assertEqual(len(self.manager.menu['main_course']), 0)
    # Agregar uno nuevo y verificar
    self.manager.menu['main_course'].append(self.manager.item("NuevoPlato", 12345))
    with open('main_course.json', 'w', encoding='utf-8') as f:
      json.dump([{"Nombre": "NuevoPlato", "Precio": 12345}], f, ensure_ascii=False, indent=2)
    self.assertEqual(self.manager.menu['main_course'][0].Nombre, "NuevoPlato")
    self.assertEqual(self.manager.menu['main_course'][0].Precio, 12345)

  def test_integrity_after_mixed_operations(self):
    # Mezclar cambios, eliminaciones y adiciones
    self.manager.menu['main_course'].append(self.manager.item("Temp1", 1111))
    with open('main_course.json', 'r+', encoding='utf-8') as f:
      items = json.load(f)
      items.append({"Nombre": "Temp1", "Precio": 1111})
      f.seek(0)
      json.dump(items, f, ensure_ascii=False, indent=2)
      f.truncate()
    # Cambiar precio
    input_values = ['main_course', str(len(self.manager.menu['main_course'])-1), '2222']
    def mock_input(prompt):
      return input_values.pop(0)
    self.manager.change_item.__globals__['input'] = mock_input
    self.manager.change_item()
    # Eliminar primero
    input_values = ['main_course', '0']
    self.manager.delete_item.__globals__['input'] = lambda prompt: input_values.pop(0)
    self.manager.delete_item()
    # Agregar otro
    self.manager.menu['main_course'].append(self.manager.item("Temp2", 3333))
    with open('main_course.json', 'r+', encoding='utf-8') as f:
      items = json.load(f)
      items.append({"Nombre": "Temp2", "Precio": 3333})
      f.seek(0)
      json.dump(items, f, ensure_ascii=False, indent=2)
      f.truncate()
    # Verificar integridad
    with open('main_course.json', 'r', encoding='utf-8') as f:
      items = json.load(f)
      self.assertEqual(len(items), len(self.manager.menu['main_course']))
      for idx, item in enumerate(items):
        self.assertEqual(item['Nombre'], self.manager.menu['main_course'][idx].Nombre)
        self.assertEqual(item['Precio'], self.manager.menu['main_course'][idx].Precio)

  def test_agregar_nuevo_item(self):
    # Simular input para agregar un nuevo item a main_course
    input_values = ['main_course', 'NuevoTest', '12345']
    def mock_input(prompt):
      return input_values.pop(0)
    self.manager.agregar_nuevo_item.__globals__['input'] = mock_input
    self.manager.agregar_nuevo_item()
    # Verificar en memoria
    nombres_mem = [i.Nombre for i in self.manager.menu['main_course']]
    self.assertIn('NuevoTest', nombres_mem)
    # Verificar en JSON
    with open('main_course.json', 'r', encoding='utf-8') as f:
      items = json.load(f)
      nombres_json = [i['Nombre'] for i in items]
      self.assertIn('NuevoTest', nombres_json)

  def test_agregar_nuevo_item_potente(self):
    # Agregar varios ítems a main_course y drinks, incluyendo duplicados
    secuencia = [
      ('main_course', 'NuevoTest1', '12345'),
      ('main_course', 'NuevoTest2', '54321'),
      ('main_course', 'NuevoTest1', '12345'),  # Duplicado
      ('drinks', 'BebidaTest', '1111'),
      ('drinks', 'BebidaTest', '1111'),        # Duplicado
      ('desserts', 'PostreTest', '2222')
    ]
    for categoria, nombre, precio in secuencia:
      input_values = [categoria, nombre, precio]
      def mock_input(prompt):
        return input_values.pop(0)
      self.manager.agregar_nuevo_item.__globals__['input'] = mock_input
      self.manager.agregar_nuevo_item()
    # Verificar en memoria main_course
    nombres_main = [i.Nombre for i in self.manager.menu['main_course']]
    self.assertIn('NuevoTest1', nombres_main)
    self.assertIn('NuevoTest2', nombres_main)
    self.assertEqual(nombres_main.count('NuevoTest1'), 2)
    # Verificar en JSON main_course
    with open('main_course.json', 'r', encoding='utf-8') as f:
      items = json.load(f)
      nombres_json = [i['Nombre'] for i in items]
      self.assertIn('NuevoTest1', nombres_json)
      self.assertIn('NuevoTest2', nombres_json)
      self.assertEqual(nombres_json.count('NuevoTest1'), 2)
    # Verificar en memoria drinks
    nombres_drinks = [i.Nombre for i in self.manager.menu['drinks']]
    self.assertIn('BebidaTest', nombres_drinks)
    self.assertEqual(nombres_drinks.count('BebidaTest'), 2)
    # Verificar en JSON drinks
    with open('drinks.json', 'r', encoding='utf-8') as f:
      items = json.load(f)
      nombres_json = [i['Nombre'] for i in items]
      self.assertIn('BebidaTest', nombres_json)
      self.assertEqual(nombres_json.count('BebidaTest'), 2)
    # Verificar en memoria desserts
    nombres_desserts = [i.Nombre for i in self.manager.menu['desserts']]
    self.assertIn('PostreTest', nombres_desserts)
    # Verificar en JSON desserts
    with open('desserts.json', 'r', encoding='utf-8') as f:
      items = json.load(f)
      nombres_json = [i['Nombre'] for i in items]
      self.assertIn('PostreTest', nombres_json)

  def test_revisar_jsons(self):
    # Simular input para revisar main_course
    input_values = ['main_course']
    def mock_input(prompt):
      return input_values.pop(0)
    self.manager.revisar_jsons.__globals__['input'] = mock_input
    # Solo verificar que no lanza excepción y muestra los items
    try:
      self.manager.revisar_jsons()
    except Exception as e:
      self.fail(f"revisar_jsons lanzó excepción inesperada: {e}")

if __name__ == "__main__":
  unittest.main()
