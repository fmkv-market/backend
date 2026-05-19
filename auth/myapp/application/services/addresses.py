from __future__ import annotations
from abc import ABC, abstractmethod



# ─── Компонент (Component) ───────────────────────────────────────
class AddressComponent(ABC):
    """Базовый компонент — общий интерфейс для листьев и контейнеров."""

    @abstractmethod
    def get_full_address(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_level(self) -> str:
        raise NotImplementedError


# ─── Лист (Leaf) ─────────────────────────────────────────────────
class AddressLeaf(AddressComponent):
    """
    Лист — конечный узел иерархии (например, номер квартиры).
    Не содержит дочерних элементов.
    """

    def __init__(self, level: str, value: str):
        self.level = level
        self.value = value

    def get_full_address(self) -> str:
        return self.value

    def get_level(self) -> str:
        return self.level


# ─── Контейнер (Composite) ───────────────────────────────────────
class AddressComposite(AddressComponent):
    """
    Контейнер — узел с дочерними элементами.
    Страна → Город → Улица → Дом.
    """

    def __init__(self, level: str, value: str):
        self.level = level
        self.value = value
        self._children: list[AddressComponent] = []

    def add(self, component: AddressComponent) -> None:
        self._children.append(component)

    def remove(self, component: AddressComponent) -> None:
        self._children.remove(component)

    def get_full_address(self) -> str:
        parts = [self.value]
        for child in self._children:
            parts.append(child.get_full_address())
        return ", ".join(parts)

    def get_level(self) -> str:
        return self.level