TONE_ORDER = ["C", "C#", "D", "D#", "E",
              "F", "F#", "G", "G#", "A", "A#", "B"]
TONE_ORDER_MAP = {tone: index for index, tone in enumerate(TONE_ORDER)}


class Tone:

    def __init__(self, tone):
        self.name = tone

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Tone) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __add__(self, other):
        if isinstance(other, Tone):
            return Chord(self, other)
        elif isinstance(other, Interval):
            index = (TONE_ORDER_MAP[self.name] + other.number_of_semitones) % 12
            return Tone(TONE_ORDER[index])

    def __sub__(self, other):
        if isinstance(other, Tone):
            return Interval((12 + TONE_ORDER_MAP[self.name] - TONE_ORDER_MAP[other.name]) % 12)
        elif isinstance(other, Interval):
            index = (12 + TONE_ORDER_MAP[self.name] - other.number_of_semitones) % 12
            return Tone(TONE_ORDER[index])


class Interval:
    intervals = {0: 'unison',
                 1: 'minor 2nd',
                 2: 'major 2nd',
                 3: 'minor 3rd',
                 4: 'major 3rd',
                 5: 'perfect 4th',
                 6: 'diminished 5th',
                 7: 'perfect 5th',
                 8: 'minor 6th',
                 9: 'major 6th',
                 10: 'minor 7th',
                 11: 'major 7th'}

    def __init__(self, number):
        self.number_of_semitones = number % 12

    def __str__(self):
        return self.intervals[self.number_of_semitones]

    def __add__(self, other):
        if isinstance(other, Interval):
            return Interval(self.number_of_semitones + other.number_of_semitones)
        elif isinstance(other, Tone):
            raise TypeError("Invalid operation")

    def __sub__(self, other):
        if isinstance(other, Tone):
            raise TypeError("Invalid operation")

    def __neg__(self):
        return Interval(12 - self.number_of_semitones)


class Chord:

    def __init__(self, root, *args):
        unique_tones = {root, *args}

        if len(unique_tones) < 2:
            raise TypeError('Cannot have a chord made of only 1 unique tone')

        self.main_tone = root
        self.root_index = TONE_ORDER_MAP[root.name]

        self.tones = sorted(
            unique_tones,
            key=lambda tone: (TONE_ORDER_MAP[tone.name] - self.root_index) % len(TONE_ORDER))

    def __str__(self):
        return "-".join(tone.name for tone in self.tones)

    def is_minor(self):
        for tone in self.tones:
            if (TONE_ORDER_MAP[tone.name] - self.root_index + 12) % 12 == 3:
                return True
        return False

    def is_major(self):
        for tone in self.tones:
            if (TONE_ORDER_MAP[tone.name] - self.root_index + 12) % 12 == 4:
                return True
        return False

    def is_power_chord(self):
        return not self.is_major() and not self.is_minor()

    def __add__(self, other):
        if isinstance(other, Tone):
            return Chord(self.main_tone, *self.tones, other)
        elif isinstance(other, Chord):
            return Chord(self.main_tone, *self.tones, *other.tones)

    def __sub__(self, other):
        if isinstance(other, Tone):
            if other in self.tones:
                new_tones = [tone for tone in self.tones if tone != other]
                new_main_tone = self.main_tone if self.main_tone != other else new_tones[0]
                return Chord(new_main_tone, *new_tones)
            else:
                raise TypeError(
                    f'Cannot remove tone {other} from chord {self}')

    def transposed(self, interval):
        new_root = self.main_tone + interval
        new_tones = tuple(tone + interval for tone in self.tones)
        return Chord(new_root, *new_tones)

