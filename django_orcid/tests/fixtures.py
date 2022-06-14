import json
import pathlib
from dataclasses import dataclass, field
from django.conf import settings


class DjangoOrcidTestSettings:
    """ Allow the configuration of the django_orcid tests, even if the app is not configured. """

    DJANGO_ORCID_BACKEND = 'django_orcid.backends.OrcidBackend'

    def __init__(self):
        self.is_django_orcid_backend_present_in_settings_per_default = False
        self.settings = settings

    def setup(self):
        if self.DJANGO_ORCID_BACKEND not in self.settings.AUTHENTICATION_BACKENDS:
            self.settings.AUTHENTICATION_BACKENDS.append(self.DJANGO_ORCID_BACKEND)
        else:
            self.is_django_orcid_backend_present_in_settings_per_default = True

    def restore(self):
        """ Set possibly changed settings back to default. """
        if not self.is_django_orcid_backend_present_in_settings_per_default:
            self.settings.AUTHENTICATION_BACKENDS.pop(self.DJANGO_ORCID_BACKEND)


def orcid_post_response_data() -> dict:
    """ Example data from: Example from:
        https://info.orcid.org/documentation/api-tutorials/api-tutorial-get-and-authenticated-orcid-id/#easy-faq-2537
    """
    orcid_json = {"access_token": "f5af9f51-07e6-4332-8f1a-c0c11c1e3728",
                  "token_type": "bearer",
                  "refresh_token": "f725f747-3a65-49f6-a231-3e8944ce464d",
                  "expires_in": 631138518,
                  "scope": "/read-limited",
                  "name": "Sofia Garcia",
                  "orcid": "0000-0001-2345-6789"}
    return orcid_json


def orcid_get_records_data() -> dict:
    """ Returns a JSON representation of a single ORCID record.
        The data source should be given as '_source' key in the JSON data itself.
    """
    orcid_record_file_path = test_resource_directory() / 'orcid-record-response.json'
    with open(orcid_record_file_path, 'r') as f:
        return json.loads(f.read())


def test_resource_directory() -> pathlib.Path:
    """ The root folder for any test resource. """
    test_directory = pathlib.Path(__file__).parent
    return test_directory / 'resources'


@dataclass
class MockResponse:
    """ Emulate the very basics of a JSON response. """
    json_data: dict
    status_code: int
    headers: dict = field(default_factory=dict)

    def json(self):
        return self.json_data
