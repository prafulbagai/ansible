def process_string(text, number):
    text_arr = text.split(" ")
    final_string = ""
    for text_val in text_arr:
        if (len(text_val) + len(final_string)) > number:
            return final_string
        final_string = (final_string + " " + text_val).strip()
    return final_string

text = "Featuring stylish rooms and moorings for recreation boats, Room Mate Aitana is a designer hotel built in 2013 on an island in the IJ River in Amsterdam."
print process_string(text, 30)