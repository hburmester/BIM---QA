Feature: Compra de productos en la aplicación

  Background: Usuario autenticado
    Given la aplicación está abierta
    When inicio sesión con "bob@example.com" y "10203040"

  Scenario: Compra de 4 productos luego del login
    When selecciono 4 productos y los agrego al carrito
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
      | Card Number    | 3258126575687896|
      | Expiration Date| 03/25           |
      | Security Code  | 123             |
    Then revisar por última vez la orden y presionar Place Order
    And aparece pantalla de confirmación de compra
    When logout