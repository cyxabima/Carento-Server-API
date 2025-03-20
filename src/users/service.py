from abc import ABC, abstractmethod


class UserService(ABC):
    @abstractmethod
    def sign_up(self):
        pass

    @abstractmethod
    def login_in(self):
        pass

    @abstractmethod
    def log_out(self):
        pass


class OwnerService(UserService):
    pass


class RenterService(UserService):
    pass
