from iwebcab.transactions import BaseAPITransaction, BasicAPITransaction, CustomerAPITransaction


class iWebCabClient(object):
    """
    Client library for iWebCab.  Initialize with creds and call some methods!
    """

    def __init__(self, api_key):
        """
        :param api_key:
        :param api_secret:
        :return: None
        """

        # Attach the API Key to each transaction/endpoint
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, BaseAPITransaction):
                attr.api_key = api_key

    # Declare all API endpoints
    create_customer = BasicAPITransaction("create_customer",
        requires=['phone_number', 'new_pin'])

    validate_customer_hash = CustomerAPITransaction("validate_customer_hash")
    validate_sec_code = CustomerAPITransaction("validate_sec_code", requires=['sec_code'])
    reset_sec_code = CustomerAPITransaction("reset_sec_code")
    update_customer_profile = CustomerAPITransaction("update_customer_profile",
        requires=['first_name', 'last_name', 'new_mobile', 'email'])

    check_live_bookings = CustomerAPITransaction("check_live_bookings")
    create_booking = CustomerAPITransaction("create_booking",
        requires=['pickup_address', 'pickup_lat', 'pickup_long'])

    cancel_booking = CustomerAPITransaction("cancel_booking", requires=['job_id'])
    booking_feedback = CustomerAPITransaction( "booking_feedback", requires=['job_id', 'rating'])
    send_email = CustomerAPITransaction('send_email', requires=['message'])
    drivers = BasicAPITransaction('drivers')
    pickup_estimate = BasicAPITransaction('pickup_estimate')
    favourites = CustomerAPITransaction('favourites')
    update_credit_card = CustomerAPITransaction('update_credit_card',
        requires=['card_number', 'card_expiration'])

    customer_bookings = CustomerAPITransaction('customer_bookings')
    reset_pin_code = BasicAPITransaction('reset_pin_code', requires=['phone_number'])

# Make the client class easy to import.
client = iWebCabClient