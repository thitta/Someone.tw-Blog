class WidgetConfig:

    def from_dict(self, dct: dict):
        raise NotImplementedError

    def update_prop_by_dict(self, dct: dict) -> None:
        for key, val in dct.items():
            setattr(self, key, val)


class SomeoneUtility:
    @staticmethod
    def to_bool(value) -> bool:
        return True if str(value).lower() in ("true", "1") else False
