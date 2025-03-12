Feature: Iniciar Sesión en la aplicación

  Scenario: Usuario inicia sesión exitosamente
    Given la aplicación está abierta
    When ingreso a la pantalla de inicio de sesión
    When ingreso el usuario "bob@example.com"
    And ingreso la contraseña "10203040"
    And presiono el botón de inicio de sesión
    Then debería ver la pantalla de inicio
    When logout