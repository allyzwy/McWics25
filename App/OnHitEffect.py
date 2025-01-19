from abc import abstractmethod


class OnHitEffect:
    @abstractmethod
    def start(self, player): ...
