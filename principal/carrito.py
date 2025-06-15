class Carrito:
    def __init__(self):
        self.items = {}  # Diccionario con clave = producto_id, valor = cantidad

    def agregar(self, producto_id):
        if producto_id in self.items:
            self.items[producto_id] += 1
        else:
            self.items[producto_id] = 1

    def eliminar(self, producto_id):
        if producto_id in self.items:
            self.items[producto_id] -= 1
            if self.items[producto_id] <= 0:
                del self.items[producto_id]

    def limpiar(self):
        self.items.clear()

    def obtener_items(self):
        return self.items
