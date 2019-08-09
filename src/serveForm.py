# you must import all the Forms here
from Forms.form_0616 import get_form as get0616
from Forms.form_0618 import get_form as get0618
from Forms.form_0605 import get_form as get0605

class ServeForm:
    def __init__(self, folder):
        self.path = folder

    def give_me_form(self, form_name):
        switcher = {
            605: get0605,
            616: get0616,
            618: get0618
        }
        func = switcher.get(form_name, lambda: "Invalid")
        json_form = func()
        return json_form

