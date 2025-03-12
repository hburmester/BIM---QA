Feature: Múltiples escenarios de compra de productos

  Background: Usuario autenticado
    Given la aplicación está abierta
    When inicio sesión con "bob@example.com" y "10203040"

  Scenario: comprar 4 productos
    When compro "4" productos:
      | Field          | Value           |
      | Full Name      | Rebecca Winter  |
      | Address Line 1 | Av. Mexico 123  |
      | City           | Lima            |
      | Zip Code       | 09090           |
      | Country        | Jamaica         |
      | Card Number    | 3258126575687896|
      | Expiration Date| 03/25           |
      | Security Code  | 123             |
    When logout
  Scenario: comprar 1 producto
    When compro "1" productos:
      | Field          | Value           |
      | Full Name      | Rebecca Winter  |
      | Address Line 1 | Av. Mexico 123  |
      | City           | Lima            |
      | Zip Code       | 09090           |
      | Country        | Jamaica         |
      | Card Number    | 3258126575687896|
      | Expiration Date| 03/25           |
      | Security Code  | 123             |
    When logout
  Scenario: Borrar todos los productos del carrito
    When selecciono 3 productos y los agrego al carrito
    When abro el carrito
    When visualizo el numero de productos
    Then borro todos los productos
    When logout
  Scenario: Compra fallida por datos de tarjeta inválidos
    When selecciono 1 productos y los agrego al carrito
    When abro el carrito
    When procedo al pago
    When agrego una dirección:
      | Field          | Value           |
      | Full Name      | Rebecca Winter  |
      | Address Line 1 | Av. Mexico 123  |
      | City           | Lima            |
      | Zip Code       | 09090           |
      | Country        | Jamaica         |
    When agrego un método de pago:
      | Field          | Value           |
      | Full Name      | Rebecca Winter  |
      | Card Number    |                 |
      | Expiration Date| 03/25           |
      | Security Code  | 123             |
    Then validar mensajes de error
    When logout