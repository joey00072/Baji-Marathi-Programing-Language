class Translate(object):
    def __init__(self):
        self.DIGITS_M_TO_E={'०': '0',
                             '१': '1',
                             '२': '2',
                             '३': '3',
                             '४': '4',
                             '५': '5',
                             '६': '6',
                             '७': '7',
                             '८': '8',
                             '९': '9'}
        self.DIGITS_E_TO_M={'0': '०',
                             '1': '१',
                             '2': '२',
                             '3': '३',
                             '4': '४',
                             '5': '५',
                             '6': '६',
                             '7': '७',
                             '8': '८',
                             '9': '९'}

    def digit_to_eng(self,num_char):
        if num_char in self.DIGITS_M_TO_E:
            return self.DIGITS_M_TO_E[num_char]

        return num_char