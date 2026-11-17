# OutboundRestrictionState


## Fields

| Field                                                                                | Type                                                                                 | Required                                                                             | Description                                                                          |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| `internal`                                                                           | [Optional[models.OutboundDirectionState]](../models/outbounddirectionstate.md)       | :heavy_minus_sign:                                                                   | N/A                                                                                  |
| `external`                                                                           | [Optional[models.OutboundDirectionState]](../models/outbounddirectionstate.md)       | :heavy_minus_sign:                                                                   | N/A                                                                                  |
| `internal_shared_machine`                                                            | *Optional[bool]*                                                                     | :heavy_minus_sign:                                                                   | Whether the internal traffic of this asset is learned per user rather than per asset |