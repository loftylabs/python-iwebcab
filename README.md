# python-iwebcab
Python client library for interacting with the iWebCab API.

## Examples

Here's an example of things breaking when you use a bad API key, or omit parameters but it should explain the syntax/basic usage.

    >>> from iwebcab import client
    >>> iwebcab_client = client('my-api-key')
    >>> iwebcab_client.create_customer()
    
    ValueError: API endpoint https://cp.iwebcab.com/public_api/create_customer.json requires missing parameters: phone_number, new_pin
    
    >>> response = iwebcab_client.create_customer(phone_number="1234567890", new_pin="1234")
    
    iwebcab.exceptions.iWebCabError: Invalid Hash ID 
    
