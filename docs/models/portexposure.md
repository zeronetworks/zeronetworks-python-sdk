# PortExposure


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `allowed_subnets_total_size`                                         | *Optional[int]*                                                      | :heavy_minus_sign:                                                   | N/A                                                                  |
| `num_of_distinct_allowed_sources`                                    | *Optional[int]*                                                      | :heavy_minus_sign:                                                   | N/A                                                                  |
| `protocol_port_range`                                                | [Optional[models.ProtocolPortRange]](../models/protocolportrange.md) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `scope`                                                              | [Optional[models.Scope]](../models/scope.md)                         | :heavy_minus_sign:                                                   | * '1' - Distinct<br/>* '2' - Any<br/>* '3' - Internal Subnet<br/>    |