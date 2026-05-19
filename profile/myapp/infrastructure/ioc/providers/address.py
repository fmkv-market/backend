from dishka import provide, Provider, Scope, AnyOf

from myapp.application.interface.address import IAddressGateway
from myapp.infrastructure.gateways.address import AddressGateway


class AddressProvider(Provider):
    address_gateway = provide(
        AddressGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            AddressGateway,
            IAddressGateway,
        ],
    )
