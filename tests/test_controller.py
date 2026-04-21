from app.controllers.main_controller import MainController


class FakeView:
    def __init__(self):
        self.status = None

    def update_status(self, msg):
        self.status = msg


def test_button_click_updates_view():
    controller = MainController(root=None)

    fake_view = FakeView()
    controller.set_view(fake_view)

    controller.on_button_click()

    assert fake_view.status == "Button clicked!"
