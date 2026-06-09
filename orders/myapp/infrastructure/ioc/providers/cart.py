from dishka import provide, Provider, Scope, AnyOf

from myapp.application.interface.cart import CartSaver, CartReader
from myapp.infrastructure.gateways.cart import CartGateway


class CartProvider(Provider):
    cart_gateway = provide(
        CartGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            CartGateway,
            CartSaver,
            CartReader,
        ],
    )