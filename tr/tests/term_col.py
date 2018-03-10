
import colored
import functools


blue = functools.partial(colored.stylize, styles=colored.fore.BLUE)
green = functools.partial(colored.stylize, styles=colored.fore.GREEN)
red = functools.partial(colored.stylize, styles=colored.fore.RED)

print(blue("This is blue"))
print(green("This is green"))
print(red("This is red"))