# RuleReviewReason

Mandatory object for rule review approve_with_changes / reject.

reason: {
    HUMAN_TRAFFIC_COVERED_BY_MFA = 1,
    TIGHTEN_RULE_SCOPE = 2,
    MISSING_PORT_OR_PROCESS = 3,
    AFFECTED_ENTITIES_CONTAINED_IN_AN_EXISTING_GROUP = 4,
    REDUNDANT_RULE = 5,
    TRAFFIC_SHOULD_BE_BLOCKED = 6,
    OTHER = 7
}


## Fields

| Field                                                           | Type                                                            | Required                                                        | Description                                                     |
| --------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- |
| `reason`                                                        | *int*                                                           | :heavy_check_mark:                                              | N/A                                                             |
| `details`                                                       | *Optional[str]*                                                 | :heavy_minus_sign:                                              | Optional if reason != OTHER(7), mandatory if reason == OTHER(7) |