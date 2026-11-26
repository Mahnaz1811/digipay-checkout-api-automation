
from playwright.sync_api import APIRequestContext, APIResponse


class PaymentClient:

    def __init__(self, request: APIRequestContext):
        self.request = request

    def get_payment_methods(self, cell_number: str, scenario: str = "happy") -> APIResponse:
        response = self.request.get(
            "/payment/",
            params={
                "CellNumber": cell_number,
                "scenario": scenario,
            },
        )

        return response
