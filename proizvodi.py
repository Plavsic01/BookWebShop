import stripe
from models import Proizvod

stripe.api_key = "sk_test_51KpDc2HWcPcdTkMNg3fTxBusO5FLBOomptkRp7xzYMp6UY919vJ2oIEVWMC3VLxb3ta0kp0FXYebbn77681y8DOj007ZQrLRc9"


def dobavi_proizvode():
    proizvodi = Proizvod.query.all()
    return proizvodi

