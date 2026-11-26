
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


def get_payment_response(scenario):
    response = {
        "status": 200,
        "payment_methods": [
            {
                "id": 1,
                "type": "online",
                "title": "Online Payment",
                "is_clickable": True
            },
            {
                "id": 11,
                "type": "wallet",
                "title": "Digital Wallet",
                "is_clickable": True,
                "source_id": 316
            },
            {
                "id": 8,
                "type": "bnpl",
                "title": "Credit Payment",
                "is_clickable": True,
                "source_id": 367,
                "options": [
                    {
                        "source_id": 386,
                        "title": "1 installment",
                        "credit": 50000000,
                        "is_active": True,
                        "is_default": True,
                        "price_type": "CASH_PRICE"
                    },
                    {
                        "source_id": 387,
                        "title": "3 installments",
                        "credit": 409361033,
                        "is_active": True,
                        "is_default": False,
                        "price_type": "CREDIT_PRICE"
                    }
                ]
            }
        ]
    }

    methods = response["payment_methods"]
    bnpl = methods[2]
    options = bnpl["options"]

    if scenario == "bnpl_blocked":
        bnpl["is_clickable"] = False
        bnpl["options"] = []

    elif scenario == "insufficient_credit":
        options[0]["credit"] = 0
        options[1]["is_default"] = True

    elif scenario == "inactive_option":
        options[0]["is_active"] = False
        options[1]["is_default"] = True

    elif scenario == "invalid_default":
        options[1]["is_default"] = True

    elif scenario == "missing_field":
        del methods[0]["type"]

    elif scenario == "wrong_type":
        methods[0]["id"] = "1"
        methods[0]["is_clickable"] = "true"

    elif scenario == "body_error":
        response["status"] = 500

    # S10: payment_methods is missing
    elif scenario == "missing_methods":
        del response["payment_methods"]

    # S11: Wallet source_id is missing
    elif scenario == "missing_wallet_source":
        del methods[1]["source_id"]

    # S12: BNPL options field is missing
    elif scenario == "missing_bnpl_options":
        del bnpl["options"]

    # S13: Invalid price_type
    elif scenario == "invalid_price_type":
        options[0]["price_type"] = "INVALID_PRICE"

    # S14: Credit has an incorrect data type
    elif scenario == "wrong_credit_type":
        options[0]["credit"] = "50000000"

    # S15: Empty payment_methods array
    elif scenario == "empty_methods":
        response["payment_methods"] = []

    # S16: Clickable BNPL with empty options
    elif scenario == "empty_clickable_bnpl_options":
        bnpl["options"] = []

    return response


class PaymentHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path != "/payment/":
            self.send_response(404)
            self.end_headers()
            return

        query = parse_qs(parsed_url.query)

        cell_number = query.get("CellNumber", [None])[0]
        scenario = query.get("scenario", ["happy"])[0]

        if not cell_number:
            self.send_response(400)
            self.end_headers()
            return

        if scenario == "http_error":
            self.send_response(500)
            self.end_headers()
            return

        response = get_payment_response(scenario)
        response_body = json.dumps(response).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()

        self.wfile.write(response_body)

    def log_message(self, format, *args):
        print(f"[Mock API] {format % args}")


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8080), PaymentHandler)

    print("Fake Payment API is running at http://localhost:8080")
    print("Endpoint: GET /payment/?CellNumber=09123456789")

    server.serve_forever()
