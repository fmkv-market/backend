from dishka import provide, Provider, Scope

from myapp.application.interactor.cart import (
    CreateCartInteractor,
    AddItemToCartInteractor,
    RemoveItemFromCartInteractor,
)


class InteractorProvider(Provider):
    create_cart = provide(CreateCartInteractor, scope=Scope.REQUEST)
    add_item_to_cart = provide(AddItemToCartInteractor, scope=Scope.REQUEST)
    remove_item_from_cart = provide(RemoveItemFromCartInteractor, scope=Scope.REQUEST)