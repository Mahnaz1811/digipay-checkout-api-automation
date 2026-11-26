
import pytest

from pytest_bdd import scenarios, given, when, then, parsers

from apis.payment_client import PaymentClient
from validators.payment_validator import (
    PaymentValidationError,
    validate_payment_response,
)


scenarios("../features/checkout_payment.feature")


@pytest.fixture
def payment_state():
    return {}


@given(
    parsers.parse('the payment API scenario is "{scenario}"'),
    target_fixture="payment_state",
)
def set_payment_scenario(scenario):
    return {"scenario": scenario}


@when("I request the payment methods")
def request_payment_methods(
    payment_state,
    api_request_context,
    cell_number,
):
    client = PaymentClient(api_request_context)

    response = client.get_payment_methods(
        cell_number=cell_number,
        scenario=payment_state["scenario"],
    )

    payment_state["request_url"] = response.url
    payment_state["http_status"] = response.status
    payment_state["response_text"] = response.text()

    try:
        payment_state["response_body"] = response.json()
    except ValueError:
        payment_state["response_body"] = None


def build_diagnostic_message(payment_state):
    return (
        "\n========== API TEST DIAGNOSTICS ==========\n"
        f"Scenario: {payment_state.get('scenario')}\n"
        f"Request URL: {payment_state.get('request_url')}\n"
        f"HTTP Status: {payment_state.get('http_status')}\n"
        f"Response Body:\n{payment_state.get('response_text')}\n"
        "==========================================\n"
    )


@then("the payment response should be valid")
def validate_successful_response(payment_state):
    try:
        validate_payment_response(
            response=payment_state["response_body"],
            http_status=payment_state["http_status"],
        )

    except PaymentValidationError as error:
        raise AssertionError(
            f"Payment response validation failed:\n"
            f"{error}"
            f"{build_diagnostic_message(payment_state)}"
        ) from error


@then(parsers.parse('the payment response should fail with rule "{rule}"'))
def validate_expected_failure(payment_state, rule):
    try:
        validate_payment_response(
            response=payment_state["response_body"],
            http_status=payment_state["http_status"],
        )

    except PaymentValidationError as error:
        assert f"[{rule}]" in str(error), (
            f"Expected rule [{rule}], but received:\n"
            f"{error}"
            f"{build_diagnostic_message(payment_state)}"
        )

    else:
        pytest.fail(
            f"Expected validation to fail with rule [{rule}], "
            f"but the response was accepted."
            f"{build_diagnostic_message(payment_state)}"
        )
