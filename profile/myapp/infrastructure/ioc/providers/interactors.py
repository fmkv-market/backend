from dishka import provide, Provider, Scope

from myapp.application.interactor.address import (
    AddAddressInteractor,
    DeleteAddressInteractor,
    GetAddressesInteractor,
    SetDefaultAddressInteractor,
)
from myapp.application.interactor.create_profile import CreateProfileInteractor
from myapp.application.interactor.delete_profile import DeleteProfileInteractor
from myapp.application.interactor.get_profile import GetProfileInteractor
from myapp.application.interactor.update_profile import UpdateProfileInteractor


class InteractorProvider(Provider):
    create_profile = provide(CreateProfileInteractor, scope=Scope.REQUEST)
    delete_profile = provide(DeleteProfileInteractor, scope=Scope.REQUEST)
    get_profile = provide(GetProfileInteractor, scope=Scope.REQUEST)
    update_profile = provide(UpdateProfileInteractor, scope=Scope.REQUEST)

    add_address = provide(AddAddressInteractor, scope=Scope.REQUEST)
    get_addresses = provide(GetAddressesInteractor, scope=Scope.REQUEST)
    delete_address = provide(DeleteAddressInteractor, scope=Scope.REQUEST)
    set_default_address = provide(SetDefaultAddressInteractor, scope=Scope.REQUEST)
