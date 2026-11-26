
Feature: Checkout Payment API validation

  As a checkout system
  I want to receive valid payment methods
  So that customers can select eligible payment options

  Scenario: S1 - Successful payment methods response
    Given the payment API scenario is "happy"
    When I request the payment methods
    Then the payment response should be valid

  Scenario: S2 - BNPL payment method is blocked
    Given the payment API scenario is "bnpl_blocked"
    When I request the payment methods
    Then the payment response should be valid

  Scenario: S3 - BNPL option has insufficient credit
    Given the payment API scenario is "insufficient_credit"
    When I request the payment methods
    Then the payment response should be valid

  Scenario: S4 - BNPL option is inactive
    Given the payment API scenario is "inactive_option"
    When I request the payment methods
    Then the payment response should be valid

  Scenario: S5 - Multiple eligible default options
    Given the payment API scenario is "invalid_default"
    When I request the payment methods
    Then the payment response should fail with rule "R6"

  Scenario: S6 - Required payment method field is missing
    Given the payment API scenario is "missing_field"
    When I request the payment methods
    Then the payment response should fail with rule "R1"

  Scenario: S7 - Payment method fields have wrong types
    Given the payment API scenario is "wrong_type"
    When I request the payment methods
    Then the payment response should fail with rule "R1"

  Scenario: S8 - HTTP server returns an error
    Given the payment API scenario is "http_error"
    When I request the payment methods
    Then the payment response should fail with rule "R8"

  Scenario: S9 - API body contains a non-success status
    Given the payment API scenario is "body_error"
    When I request the payment methods
    Then the payment response should fail with rule "R8"

  Scenario: S10 - Payment methods field is missing
    Given the payment API scenario is "missing_methods"
    When I request the payment methods
    Then the payment response should fail with rule "R1"

  Scenario: S11 - Wallet source_id is missing
    Given the payment API scenario is "missing_wallet_source"
    When I request the payment methods
    Then the payment response should fail with rule "R3"

  Scenario: S12 - BNPL options field is missing
    Given the payment API scenario is "missing_bnpl_options"
    When I request the payment methods
    Then the payment response should fail with rule "R4"

  Scenario: S13 - BNPL option has an invalid price type
    Given the payment API scenario is "invalid_price_type"
    When I request the payment methods
    Then the payment response should fail with rule "R7"

  Scenario: S14 - BNPL option credit has a wrong data type
    Given the payment API scenario is "wrong_credit_type"
    When I request the payment methods
    Then the payment response should fail with rule "R4"

  Scenario: S15 - Payment methods array is empty
    Given the payment API scenario is "empty_methods"
    When I request the payment methods
    Then the payment response should be valid

  Scenario: S16 - Clickable BNPL has empty options
    Given the payment API scenario is "empty_clickable_bnpl_options"
    When I request the payment methods
    Then the payment response should fail with rule "R4"
