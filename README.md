# schemata
[![codecov](https://codecov.io/gh/dion-ricky/schemata/branch/master/graph/badge.svg?token=D81L4WPQRU)](https://codecov.io/gh/dion-ricky/schemata)

A thin layer of abstraction between schema definition and schema generation. Define once, transform all you want (not a good catchphrase, I know..)

Specify schema definition using Python classes and type hints,
```python
# file: your_own/schemata.py
from schemata.commons.special_type import Required

class User:
    id: Required[int]
    username: Required[str]

class Customer(User):
    pass

class Product:
    id: Required[int]
    name: Required[str]
    price: float
```

And create your own schemata translator to convert it to any schema specification that you want. Be it Avro schema, BigQuery JSON schema, or even a proprietary or legacy schema specification. Remember, define once, transform all you want (haha.. okay I'll stop now).
```python
from your_own.translator import AvroTranslator
from your_own.schemata import Customer, Product
from schemata.commons.utils import resolve_dependency

customer_schemata = resolve_dependency(Customer)
product_schemata = resolve_dependency(Product)

translator = AvroTranslator()

customer_schema = translator.translate(customer_schemata)
product_schema = translator.translate(product_schemata)
```

## What this package provides?
**Resolving schema nesting**

If you reuse a lot of schemata in another schemata, this package automatically and recursively expanded the nested schemata into the outer schemata. Consider the following example:
```python
from typing import List

class Product:
    id: int

class Catalog:
    items: List[Product]

class Merchant:
    catalogs: List[Catalog]
```

Now if you translate the `Merchant` schemata, you'll see that all of the nested schemata are translated as well. The moment you change `Product` or `Catalog` schemata, it'll reflect on the outer schemata when translated. All of this magic, however, comes with a price. To resolve schema nesting you have to use the `resolve_dependency` function defined in `commons.utils` module. For example:
```python
from schemata.commons.utils import resolve_dependency
from schemata.translator.dummy import Dummy
from your_own.schemata import Merchant

merchant_schemata = resolve_dependency(Merchant)

translator = Dummy()

translator.translate(merchant_schemata)
# observe the output from your console
```

## Tips and Tricks
**1. How to provide additional metadata?**

It depends on what kind of metadata that you need to include. For example, in Avro you may want to specify a namespace for each schema. So how to do that?

Well, there are a bunch of ways to assign a namespace but the easier and probably the most elegant solution that I can think of is to use directory structure. Check the example below:
```python
# file: com/your_company/marketplace/Product.py
class Product:
    # You define your schema here
    pass

# file: com/your_company/marketplace/Customer.py
class Customer:
    pass
```

Since this library doesn't provide any translator out of the box, you can go wild when creating your own translator. Using the directory structure above you can infer the namespace using the path of the file that defines the schemata. This is achievable because Python is keeping track of the module where the imported class is defined. The below snippets is a simple proof using our included examples schemata:
```python
from schemata.examples.example1 import ProductEntity

print(ProductEntity.__module__)
# output: 'schemata.examples.example1'

# Now here's what it looks like for your schemata
from com.your_company.marketplace.Product import Product
from com.your_company.marketplace.Customer import Customer

print(Product.__module__)
# output: 'com.your_company.marketplace.Product'
print(Customer.__module__)
# output: 'com.your_company.marketplace.Customer'
```

And that's how you trick the system, .. or maybe not. Anyway hope this example can help.
