# Clase abstracta para medios de pago
class MedioPago:
  def __init__(self):
    pass

  def pagar(self, monto):
    raise NotImplementedError("Subclases deben implementar pagar()")

# Clase para pago con tarjeta
class Tarjeta(MedioPago):
  def __init__(self, numero, cvv, password, por_contacto = False):
    super().__init__()
    self.numero = numero  # Numero de la tarjeta
    self.__cvv = str(cvv)  # CVV privado
    self.por_contacto = por_contacto  # Si es pago por contacto
    self.__password : str = password  # Contrasena privada

  def pagar(self, monto):
    if self.por_contacto:
      print(f"Pagando por contacto {monto} con tarjeta {self.numero}")
      print("transaccion completada")
    else:
      n_intentos = 3
      while True:
        if n_intentos > 0:
          print(f"Descontando {monto} de la tarjeta: {self.numero}")
          password = input("Ingrese su password: ")
          cvv = input("Ingrese su cvv: ")
          if password == self.__password and cvv == self.__cvv:
            print("Transaccion completada")
            break
          else:
            n_intentos -=  1
            print(f"Password o CVV incorrectos, le queda {n_intentos} intentos")
            if n_intentos == 0:
              break

# Clase para pago en efectivo
class Efectivo(MedioPago):
  def __init__(self, monto_entregado):
    super().__init__()
    self.monto_entregado = monto_entregado  # Dinero entregado por el cliente

  def pagar(self, monto):
    if self.monto_entregado >= monto:
      print(f"Pago realizado en efectivo. Cambio: {self.monto_entregado - monto}")
    else:
      print(f"Fondos insuficientes. Faltan {monto - self.monto_entregado} para completar el pago.")
