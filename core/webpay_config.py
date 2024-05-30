import uuid
from transbank.webpay.webpay_plus.transaction import WebpayOptions, IntegrationCommerceCodes, IntegrationApiKeys

# Configuración de Webpay
commerce_code = IntegrationCommerceCodes.WEBPAY_PLUS  # Código de comercio de prueba para Webpay Plus
api_key = IntegrationApiKeys.WEBPAY  # Llave secreta de prueba
integration_type = "TEST"

# Opciones de Webpay
webpay_options = WebpayOptions(commerce_code=commerce_code, api_key=api_key, integration_type=integration_type)

def generar_buy_order():
    # Generar un UUID y truncarlo a 26 caracteres para asegurar la longitud máxima permitida
    buy_order = uuid.uuid4().hex[:26]
    return buy_order

#┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
#| Tarjetas de Prueba                                                                                               |
#|                                                                                                                  |
#| VISA                                                                                                             |
#|                                                                                                                  |
#| 4051 8856 0044 6623                                                                                              |
#| CVV 123                                                                                                          |
#| Cualquier fecha de expiración                                                                                    |
#| Cuando aparece un formulario de autenticación con RUT y clave, se debe usar el RUT 11.111.111-1 y la clave 123.  |
#└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘