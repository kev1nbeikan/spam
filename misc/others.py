def check_file_name(name: str):
    if '/' in name:
        return False
    return name.endswith('.json') or name.endswith('.session')


class MySet(set):
    def add(self, element) -> None:
        if isinstance(element, set | list):
            self.update(element)
        else:
            super().add(element)





