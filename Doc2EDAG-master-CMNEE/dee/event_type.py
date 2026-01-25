# -*- coding: utf-8 -*-
# AUTHOR: Shun Zheng
# DATE: 19-9-19


class BaseEvent(object):
    def __init__(self, fields, event_name='Event', key_fields=(), recguid=None):
        self.recguid = recguid
        self.name = event_name
        self.fields = list(fields)
        self.field2content = {f: None for f in fields}
        self.nonempty_count = 0
        self.nonempty_ratio = self.nonempty_count / len(self.fields)

        self.key_fields = set(key_fields)
        for key_field in self.key_fields:
            assert key_field in self.field2content

    def __repr__(self):
        event_str = "\n{}[\n".format(self.name)
        event_str += "  {}={}\n".format("recguid", self.recguid)
        event_str += "  {}={}\n".format("nonempty_count", self.nonempty_count)
        event_str += "  {}={:.3f}\n".format("nonempty_ratio", self.nonempty_ratio)
        event_str += "] (\n"
        for field in self.fields:
            if field in self.key_fields:
                key_str = " (key)"
            else:
                key_str = ""
            event_str += "  " + field + "=" + str(self.field2content[field]) + ", {}\n".format(key_str)
        event_str += ")\n"
        return event_str

    def update_by_dict(self, field2text, recguid=None):
        self.nonempty_count = 0
        self.recguid = recguid

        for field in self.fields:
            if field in field2text and field2text[field] is not None:
                self.nonempty_count += 1
                self.field2content[field] = field2text[field]
            else:
                self.field2content[field] = None

        self.nonempty_ratio = self.nonempty_count / len(self.fields)

    def field_to_dict(self):
        return dict(self.field2content)

    def set_key_fields(self, key_fields):
        self.key_fields = set(key_fields)

    def is_key_complete(self):
        for key_field in self.key_fields:
            if self.field2content[key_field] is None:
                return False

        return True

    def is_good_candidate(self):
        raise NotImplementedError()

    def get_argument_tuple(self):
        args_tuple = tuple(self.field2content[field] for field in self.fields)
        return args_tuple


class Experiment(BaseEvent):
    NAME = 'Experiment'
    FIELDS = [
        "Subject",
        "Equipment",
        "Date",
        "Location"
    ]

    def __init__(self, recguid=None):
        super().__init__(
            Experiment.FIELDS, event_name=Experiment.NAME, recguid=recguid
        )
        self.set_key_fields([
            'Subject',
            'Equipment',
        ])

    def is_good_candidate(self, min_match_count=5):
        key_flag = self.is_key_complete()
        if key_flag:
            if self.nonempty_count >= min_match_count:
                return True
        return False


class Manoeuvre(BaseEvent):
    NAME = 'Manoeuvre'
    FIELDS = [
        "Subject",
        "Date",
        "Area",
        "Content"
    ]

    def __init__(self, recguid=None):
        super().__init__(
            Manoeuvre.FIELDS, event_name=Manoeuvre.NAME, recguid=recguid
        )
        self.set_key_fields([
            'Content',
        ])

    def is_good_candidate(self, min_match_count=4):
        key_flag = self.is_key_complete()
        if key_flag:
            if self.nonempty_count >= min_match_count:
                return True
        return False


class Deploy(BaseEvent):
    NAME = 'Deploy'
    FIELDS = [
        "Subject",
        "Militaryforce",
        "Date",
        "Location"
    ]

    def __init__(self, recguid=None):
        super().__init__(
            Deploy.FIELDS, event_name=Deploy.NAME, recguid=recguid
        )
        self.set_key_fields([
            "Militaryforce",
        ])

    def is_good_candidate(self, min_match_count=4):
        key_flag = self.is_key_complete()
        if key_flag:
            if self.nonempty_count >= min_match_count:
                return True
        return False


class Support(BaseEvent):
    NAME = 'Support'
    FIELDS = [
        "Subject",
        "Object",
        "Materials",
        "Date"
    ]

    def __init__(self, recguid=None):
        super().__init__(
            Support.FIELDS, event_name=Support.NAME, recguid=recguid
        )
        self.set_key_fields([
            "Materials",
        ])

    def is_good_candidate(self, min_match_count=4):
        key_flag = self.is_key_complete()
        if key_flag:
            if self.nonempty_count >= min_match_count:
                return True
        return False


class Accident(BaseEvent):
    NAME = 'Accident'
    FIELDS = [
        "Subject",
        "Date",
        "Location",
        "Result"
    ]

    def __init__(self, recguid=None):
        # super(EquityPledgeEvent, self).__init__(
        super().__init__(
            Accident.FIELDS, event_name=Accident.NAME, recguid=recguid
        )
        self.set_key_fields([
            "Result"
        ])

    def is_good_candidate(self, min_match_count=5):
        key_flag = self.is_key_complete()
        if key_flag:
            if self.nonempty_count >= min_match_count:
                return True
        return False

class Exhibit(BaseEvent):
    NAME = 'Exhibit'
    FIELDS = [
        "Subject",
        "Equipment",
        "Date",
        "Location"
    ]

    def __init__(self, recguid=None):
        # super(EquityPledgeEvent, self).__init__(
        super().__init__(
            Exhibit.FIELDS, event_name=Exhibit.NAME, recguid=recguid
        )
        self.set_key_fields([
            "Equipment",
        ])

    def is_good_candidate(self, min_match_count=5):
        key_flag = self.is_key_complete()
        if key_flag:
            if self.nonempty_count >= min_match_count:
                return True
        return False

class Conflict(BaseEvent):
    NAME = 'Conflict'
    FIELDS = [
        "Subject",
        "Object",
        "Date",
        "Location"
    ]

    def __init__(self, recguid=None):
        # super(EquityPledgeEvent, self).__init__(
        super().__init__(
            Conflict.FIELDS, event_name=Conflict.NAME, recguid=recguid
        )
        self.set_key_fields([
            "Subject",
            "Object",
        ])

    def is_good_candidate(self, min_match_count=5):
        key_flag = self.is_key_complete()
        if key_flag:
            if self.nonempty_count >= min_match_count:
                return True
        return False

class Injure(BaseEvent):
    NAME = 'Injure'
    FIELDS = [
        "Subject",
        "Quantity",
        "Date",
        "Location"
    ]

    def __init__(self, recguid=None):
        # super(EquityPledgeEvent, self).__init__(
        super().__init__(
            Injure.FIELDS, event_name=Injure.NAME, recguid=recguid
        )
        self.set_key_fields([
            "Subject",
            "Quantity",
        ])

    def is_good_candidate(self, min_match_count=5):
        key_flag = self.is_key_complete()
        if key_flag:
            if self.nonempty_count >= min_match_count:
                return True
        return False

common_fields = ["Date"]


event_type2event_class = {
    Experiment.NAME: Experiment,
    Manoeuvre.NAME: Manoeuvre,
    Deploy.NAME: Deploy,
    Support.NAME: Support,
    Accident.NAME: Accident,
    Exhibit.NAME: Exhibit,
    Conflict.NAME: Conflict,
    Injure.NAME: Injure,
}


event_type_fields_list = [
    (Experiment.NAME, Experiment.FIELDS),
    (Manoeuvre.NAME, Manoeuvre.FIELDS),
    (Deploy.NAME, Deploy.FIELDS),
    (Support.NAME, Support.FIELDS),
    (Accident.NAME, Accident.FIELDS),
    (Exhibit.NAME, Exhibit.FIELDS),
    (Conflict.NAME, Conflict.FIELDS),
    (Injure.NAME, Injure.FIELDS),
]


