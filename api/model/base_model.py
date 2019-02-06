class BaseModel:
    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(frozenset(self.__dict__.items()))

    def to_json(self):
        return self.__dict__

    @classmethod
    def from_row(cls, row):
        params = { }
        for key in row.keys():
            params[key] = row[key]

        return cls(**params)
