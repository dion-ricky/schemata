from datetime import date, datetime

from schemata.commons.type import Long
from schemata.commons.special_type import Required, PII_HIGH


class CustomerEntity:
    id: int
    first_name: PII_HIGH[str]
    last_name: PII_HIGH[str]
    dob: PII_HIGH[date]


class ProductEntity:
    id: Required[int]
    name: str
    sku: str
    description: str
    price: Long


class ProductEntityTimestamped(ProductEntity):
    created_date: datetime
    updated_date: datetime