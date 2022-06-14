from typing import Callable, Union
from unittest import mock

from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory

from django_orcid import views
from django_orcid.tests.fixtures import (
    DjangoOrcidTestSettings,
    orcid_get_records_data,
    orcid_post_response_data,
    MockResponse
)


class TestLogin(TestCase):
    """ Tests the application with a running test database in the background. """

    authentication_url = '/accounts/auth'

    def test_failing_login(self):
        request = create_get_request(self.authentication_url)
        response = views.auth(request)

        self.assertIn('Login Failed', str(response.content))

    def test_successful_login(self):
        request = create_get_request(orcid_authentication_request_parameters)
        response = views.auth(request)

        self.assertIn('You successfully logged in', str(response.content))

    def setUp(self) -> None:
        self.django_orcid_test_settings = DjangoOrcidTestSettings()
        self.django_orcid_test_settings.setup()

        self.request_factory = RequestFactory()

        self.mocks = []
        for mock_parameters in orcid_patches:
            return_value = mock_parameters['return_value'] if 'return_value' in mock_parameters else None
            patcher = mock.patch(**mock_parameters)

            if return_value is not None:
                patcher.return_value = return_value

            patcher.start()
            self.mocks.append(patcher)

            # This makes sure that the patch will be stopped, even if there is an exception
            self.addCleanup(patcher.stop)


orcid_patches = [
    {'target': 'requests.get', 'auto_spec': True, 'return_value': MockResponse(json_data=orcid_get_records_data(),
                                                                               status_code=200)},
    {'target': 'requests.post', 'auto_spec': True, 'return_value': MockResponse(json_data=orcid_post_response_data(),
                                                                                status_code=200)}
]


def orcid_authentication_request_parameters() -> dict:
    return {
        'path': TestLogin.authentication_url,
        'data': {
            'code': 'dummy-token-123'
        },
        'HTTP_X_FORWARD_FOR': '123.456.7.89'
    }


def create_get_request(parameter_callback: Union[Callable, str]):
    request_factory = RequestFactory()
    if isinstance(parameter_callback, str):
        request = request_factory.get(parameter_callback)
    else:
        request = request_factory.get(**parameter_callback())

    add_session_middleware_to_request(request)
    return request


def add_session_middleware_to_request(request):
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()
