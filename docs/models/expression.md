# Expression


## Fields

| Field                                                                          | Type                                                                           | Required                                                                       | Description                                                                    |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `key`                                                                          | *Optional[str]*                                                                | :heavy_minus_sign:                                                             | N/A                                                                            |
| `operator`                                                                     | [Optional[models.ExpressionOperator]](../models/expressionoperator.md)         | :heavy_minus_sign:                                                             | * '0' - Unspecified<br/>* '1' - In<br/>* '2' - NotIn<br/>* '3' - Exists<br/>* '4' - NotExists<br/> |
| `values_list`                                                                  | List[*str*]                                                                    | :heavy_minus_sign:                                                             | N/A                                                                            |