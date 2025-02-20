import textwrap


class Message:
    """A message, which holds translated text (if exists) and its color."""
    def __init__(self, text, color='white'):
        """Initialize the message's text and color."""
        self.text = f"[font=text]{text}"
        self.color = color


class MessageLog:
    # Organize message log.
    def __init__(self, x, width, height):
        """Set properties."""
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        # Adda  message to the log.
        # Split the message if necessary, among multiple lines
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # If the buffer is full, remove the first line to make room for the new one
            if len(self.messages) == self.height:
                del self.messages[0]

            # Add the new line as a Message object, with the text and the color
            self.messages.append(Message(line, message.color))
