from src.bases.api.method_handler import MethodHandler


class Get(MethodHandler):
    def handle_logic(self):
        return dict(ok=True)

