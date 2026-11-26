
class PaymentValidationError(AssertionError):
    """Raised when the payment API response violates the expected contract."""


def require(condition, rule, location, actual):
    if not condition:
        raise PaymentValidationError(
            f"[{rule}] {location}: actual value = {actual!r}"
        )


def is_integer(value):
    # In Python, bool is a subclass of int, so exclude bool explicitly.
    return isinstance(value, int) and not isinstance(value, bool)


def validate_payment_response(response, http_status):
    # R8: HTTP response must be successful.
    require(
        http_status == 200,
        "R8",
        "HTTP response status",
        http_status
    )

    # R1: Response body must be a JSON object.
    require(
        isinstance(response, dict),
        "R1",
        "response body",
        type(response).__name__
    )

    # R1: Body status must exist and be an integer.
    require("status" in response, "R1", "body.status", "missing")
    require(
        is_integer(response["status"]),
        "R1",
        "body.status",
        response["status"]
    )

    # R8: Body status must indicate success.
    require(
        response["status"] == 200,
        "R8",
        "body.status",
        response["status"]
    )

    # R1: payment_methods must exist and be an array.
    require(
        "payment_methods" in response,
        "R1",
        "payment_methods",
        "missing"
    )

    methods = response["payment_methods"]

    require(
        isinstance(methods, list),
        "R1",
        "payment_methods",
        methods
    )

    for index, method in enumerate(methods):
        location = f"payment_methods[{index}]"

        require(
            isinstance(method, dict),
            "R1",
            location,
            type(method).__name__
        )

        # R1: Required payment method fields.
        required_fields = ("id", "type", "title", "is_clickable")

        for field in required_fields:
            require(
                field in method,
                "R1",
                f"{location}.{field}",
                "missing"
            )

        # R1: Validate payment method field types.
        require(
            is_integer(method["id"]),
            "R1",
            f"{location}.id",
            method["id"]
        )

        require(
            isinstance(method["type"], str)
            and method["type"] in ("online", "wallet", "bnpl"),
            "R1",
            f"{location}.type",
            method["type"]
        )

        require(
            isinstance(method["title"], str),
            "R1",
            f"{location}.title",
            method["title"]
        )

        require(
            isinstance(method["is_clickable"], bool),
            "R1",
            f"{location}.is_clickable",
            method["is_clickable"]
        )

        # Description is optional, but must be a string if provided.
        if "description" in method:
            require(
                isinstance(method["description"], str),
                "R1",
                f"{location}.description",
                method["description"]
            )

        # R3: Wallet and BNPL methods require an integer source_id.
        if method["type"] in ("wallet", "bnpl"):
            require(
                "source_id" in method,
                "R3",
                f"{location}.source_id",
                "missing"
            )

            require(
                is_integer(method["source_id"]),
                "R3",
                f"{location}.source_id",
                method["source_id"]
            )

        # BNPL-specific validation.
        if method["type"] == "bnpl":

            # R4: BNPL options must exist and be an array.
            require(
                "options" in method,
                "R4",
                f"{location}.options",
                "missing"
            )

            options = method["options"]

            require(
                isinstance(options, list),
                "R4",
                f"{location}.options",
                options
            )

            # R4: Clickable BNPL must have at least one option.
            # Non-clickable BNPL may have an empty options array.
            require(
                not method["is_clickable"] or len(options) > 0,
                "R4",
                f"{location}.options",
                options
            )

            eligible_options = []

            for option_index, option in enumerate(options):
                option_location = (
                    f"{location}.options[{option_index}]"
                )

                require(
                    isinstance(option, dict),
                    "R4",
                    option_location,
                    type(option).__name__
                )

                # R4: All BNPL option fields are required.
                option_fields = (
                    "source_id",
                    "title",
                    "credit",
                    "is_active",
                    "is_default",
                    "price_type"
                )

                for field in option_fields:
                    require(
                        field in option,
                        "R4",
                        f"{option_location}.{field}",
                        "missing"
                    )

                require(
                    is_integer(option["source_id"]),
                    "R4",
                    f"{option_location}.source_id",
                    option["source_id"]
                )

                require(
                    isinstance(option["title"], str),
                    "R4",
                    f"{option_location}.title",
                    option["title"]
                )

                require(
                    is_integer(option["credit"]),
                    "R4",
                    f"{option_location}.credit",
                    option["credit"]
                )

                require(
                    isinstance(option["is_active"], bool),
                    "R4",
                    f"{option_location}.is_active",
                    option["is_active"]
                )

                require(
                    isinstance(option["is_default"], bool),
                    "R4",
                    f"{option_location}.is_default",
                    option["is_default"]
                )

                # R7: price_type must match one of the allowed values.
                require(
                    isinstance(option["price_type"], str)
                    and option["price_type"] in (
                        "CASH_PRICE",
                        "CREDIT_PRICE"
                    ),
                    "R7",
                    f"{option_location}.price_type",
                    option["price_type"]
                )

                # R5: An option is eligible only when active and credit > 0.
                if option["is_active"] and option["credit"] > 0:
                    eligible_options.append(option)

            # R6: Exactly one eligible option must be the default,
            # whenever at least one eligible option exists.
            if eligible_options:
                default_count = sum(
                    1
                    for option in eligible_options
                    if option["is_default"]
                )

                require(
                    default_count == 1,
                    "R6",
                    f"{location}.eligible_options.default_count",
                    default_count
                )

    return True
