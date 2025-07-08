from paquetes.Menu_manager import MenusManager

if __name__ == "__main__":
    menu_jsons = {
        'main_course': 'paquetes/main_course.json',
        'desserts': 'paquetes/desserts.json',
        'drinks': 'paquetes/drinks.json'
    }
    manager = MenusManager(menu_jsons=menu_jsons)
    manager.inicialice_restaurant()