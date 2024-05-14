"""
We could use rich, and reprint the inire response of gpt, everytime we get some new text. Then the markdown formatting could be applied automatically.
"""

MARKDOWN = """
# This is an h1
## This is an h2
### This is an h3
#### This is an h4


Rich can do a pretty *decent* job of rendering markdown.

1. This is a list item
2. This is another list item

```python
import logging

# Set up logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

def get_user_input():
    try:
        value = input("Please enter a number: ")
        value = int(value)
        return value
    except ValueError:
        print("That's not a valid number. Please enter a whole number, without any letters or punctuation.")
        # Optionally log the error for future reference by a developer or for debugging.
        logging.exception("User entered a value that couldn't be converted to an integer.")
        return None
"""
b = """
# Main application loop
while True:
    user_value = get_user_input()
    if user_value is not None:
        # Process the user's input if it's valid
        print(f"The number you entered is {user_value}")
        break
"""
c = """
    else:
        # If the input wasn't valid, the user is re-prompted by the loop
        pass
```
"""
from rich.console import Console
from rich.markdown import Markdown

console = Console()
md = Markdown(MARKDOWN)
console.print(md)
console.print(b)
console.print(c)