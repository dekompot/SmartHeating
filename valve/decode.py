def decode_temperature(message):
    return read_topic(message), read_id(message), read_value(message)


def read_topic(message):
    return message.topic


def read_id(message):
    return str(message.payload.decode("utf-8").split(':')[0])


def read_value(message):
    return str(message.payload.decode("utf-8").split(':')[1])