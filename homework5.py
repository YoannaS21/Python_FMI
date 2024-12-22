import re
from collections import defaultdict
import random


class Santa:
    _santa_the_one_and_only = None
    _kids_and_wishes = {}
    _kid_christmas_count = defaultdict(int)

    def __new__(cls, *args, **kwargs):
        if cls._santa_the_one_and_only is None:
            cls._santa_the_one_and_only = super(Santa, cls).__new__(cls)
        return cls._santa_the_one_and_only

    def __call__(self, kid, wish):
        gift = self._get_wanted_gift(wish)
        self._kids_and_wishes[kid] = gift

    def __matmul__(self, letter):
        gift = self._get_wanted_gift(letter)
        kid_id = self._get_signature(letter)
        kid_id.strip()

        for kid in Kid._kids:
            if id(kid) == int(kid_id):
                self._kids_and_wishes[kid] = gift

    def __iter__(self):
        return iter(self._kids_and_wishes.values())

    @staticmethod
    def _get_signature(letter):
        signature = re.search(r'^\s*(\d+)\s*$', letter, re.MULTILINE)
        if (signature):
            return str(signature.group(1))

    @staticmethod
    def _get_wanted_gift(letter):
        wanted_gift = re.search(r'[\'\"]([a-zA-Z0-9\s]+)[\' \"]', letter)
        if (wanted_gift):
            return str(wanted_gift.group(1))

    def _get_most_wanted_gift(self):
        count_of_gift = defaultdict(int)

        for gift in self._kids_and_wishes.values():
            count_of_gift[gift] += 1

        max_count = max(count_of_gift.values())

        most_wanted_gifts = []
        for gift, count in count_of_gift.items():
            if (count == max_count):
                most_wanted_gifts.append(gift)

        return random.choice(most_wanted_gifts)

    def xmas(self):
        if not self._kids_and_wishes:
            for kid in Kid._kids:
                self._kid_christmas_count[kid] += 1
            return

        for kid in Kid._kids:
            self._kid_christmas_count[kid] += 1
            if (self._kid_christmas_count[kid]) > 5:
                continue

            if kid._is_naughty:
                kid('coal')
                kid._is_naughty = False
                continue

            elif kid in self._kids_and_wishes:
                kid(self._kids_and_wishes[kid])

            else:
                kid(self._get_most_wanted_gift())

        self._kids_and_wishes.clear()


class Kid(type):
    _kids = []

    def __new__(cls, name, bases, attr_dict):
        if '__call__' not in attr_dict:
            raise NotImplementedError('Готиняги')
        for name, method in attr_dict.items():
            if not name.startswith('__') and callable(method):
                attr_dict[name] = cls.check_if_naughty(method)
        return super().__new__(cls, name, bases, attr_dict)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        Kid._kids.append(instance)
        instance._is_naughty = False
        return instance
    
    def check_if_naughty(method):
        def decorator(self, *args, **kwargs):
            try:
                return method(self, *args, **kwargs)
            except Exception:
                self._is_naughty = True
                raise
        return decorator

