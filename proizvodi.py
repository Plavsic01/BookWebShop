import stripe

stripe.api_key = "sk_test_51KpDc2HWcPcdTkMNg3fTxBusO5FLBOomptkRp7xzYMp6UY919vJ2oIEVWMC3VLxb3ta0kp0FXYebbn77681y8DOj007ZQrLRc9"

def kreiraj_proizvod(name:str,description:str,images:list):
    return stripe.Product.create(name=name,description=description,images=images)


def dobavi_proizvod(product_id:str):
    return stripe.Product.retrieve(product_id)


def dobavi_proizvode(limit=None):
    if limit is not None:
        return stripe.Product.list(limit=limit)

    return stripe.Product.list()

