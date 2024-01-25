
def get_ask_id(message):
    return str(message.payload.decode("utf-8").split('/')[1])


def decode_temperature(message):
    return read_topic(message), int(read_id(message)), float(read_value(message))


def read_topic(message):
    return message.topic


def read_id(message):
    return str(message.payload.decode("utf-8").split('/')[0])


def read_value(message):
    return str(message.payload.decode("utf-8").split('/')[1])