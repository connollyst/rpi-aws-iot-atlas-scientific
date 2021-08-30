class IO:

    def send_and_receive(self, address, message, wait=0) -> str:
        pass

    def send(self, address, message) -> None:
        pass

    def receive(self, address) -> str:
        pass

    def close(self):
        pass
