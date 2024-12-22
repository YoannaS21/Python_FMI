class HauntedMansion:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattr__(self, name):
        return "Booooo, only ghosts here!"

    def __setattr__(self, name, value):
        object.__setattr__(self, f"spooky_{name}", value)


haunted_mansion = HauntedMansion(butler="Alfred", rooms=10, basement=True)

print(haunted_mansion.butler)
# Booooo, only ghosts here!

print(haunted_mansion.spooky_butler)
# Alfred

haunted_mansion.friendly_ghost = "Your favourite HP ghost - Nearly Headless Nick"
print(haunted_mansion.friendly_ghost)
# Booooo, only ghosts here!

print(haunted_mansion.spooky_friendly_ghost)
# Your favourite HP ghost - Nearly Headless Nick

print(haunted_mansion.__class__)
# <class '__main__.HauntedMansion'>

print(haunted_mansion.spooky_rooms)
# 10

print(HauntedMansion(_nikola_georgiev='Може ли да дадете пример за очаквано поведение при работа с protected атрибути').spooky__nikola_georgiev)
# Може ли да дадете пример за очаквано поведение при работа с protected атрибути
