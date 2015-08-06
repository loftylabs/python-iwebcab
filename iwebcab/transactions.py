import json
import requests

from iwebcab.exceptions import iWebCabError


class BaseAPITransaction(object):
    """
    Transaction base class.  Implements behavior that is consistent across all types of API
    Transactions.
    """
    requires_extra = []

    @property
    def endpoint(self):
        return "{command}.json".format(command=self.command)

    def __init__(self, command, **kwargs):
        self.command = command
        self.requires = kwargs.get('requires')
        # iWebCab uses posts by default
        self.method = kwargs.get('method', 'POST')

        if not isinstance(self.requires, list):
            raise ValueError("API Transaction requires kwarg must be a list of required parameter "
                             "keys")

    def __call__(self, *args, **kwargs):
        """
        Entry point for making an API Call.
        Tests that the call was constructed correctly with all required parameters.
        """

        param_keys = kwargs.keys()
        missing_params = []
        for k in self._get_required_parameters():
            if k not in param_keys:
                missing_params.append(k)

        if missing_params:
            raise ValueError("API endpoint {name} requires missing parameters: {keys}".format(
                name=self.endpoint, keys=", ".join(missing_params)
            ))

        return self._make_api_call(kwargs)

    def _make_api_call(self, parameters):
        """
        Do the actual HTTP request for the API call.
        """

        # Attach the API Key to the parameters which was boind to this class from the iWebCab
        # client class.
        parameters.update({
            'api_key': self.api_key
        })

        # Make the call
        if self.method == 'GET':
            response = requests.get(self.endpoint, params=parameters)
        elif self.method == 'POST':
            response = requests.post(self.endpoint, parms=parameters)
        else:
            raise ValueError("API endpoint {name} was called with an unsupported HTTP method "
                             "{method}".format(name=self.endpoint, method=self.method))

        # Convert the response to a Python object and check for errors
        response_object = json.loads(response.text())
        if 'error' in response_object.keys():
            raise iWebCabError(response_object['error'])

        return response_object

    def _get_required_parameters(self):
        """
        Get the parameters that were supplied when this transaction was intantiated, and
        additionally add any extra parameters that are required by the child Transaction class.
        """

        params = self.requires
        if self.requires_extra:
            params.extend(self.requires_extra)

        return params


class BasicAPITransaction(BaseAPITransaction):
    """
    Represents a Basic API Transaction for the iWebCab API
    See: https://iwebcab.readme.io/docs/basic-api-transaction  
    """

    # All basic API transactions require an API key
    requires_extra = ['api_key']

    def __init__(self, command, **kwargs):
        super(BasicAPITransaction, self).__init__(command, **kwargs)



class CustomerAPITransaction(BaseAPITransaction):
    """
    Represents a Basic API Transaction for the iWebCab API
    See: https://iwebcab.readme.io/docs/customer-api-transaction
    """

    # All customer API transactions require...
    requires_extra = ['api_key', 'phone_number', 'customer_id', 'customer_hash']

    def __init__(self, command, **kwargs):
        super(CustomerAPITransaction, self).__init__(command, **kwargs)
