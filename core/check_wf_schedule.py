from datetime import datetime
from calendar import monthrange


def isScheduledDate(specificDate=None):
    """Returns whether the date passed in meets the criteria"""

    if specificDate:

        if "-" in specificDate and ":" not in specificDate:
            # Just date passed in
            specificDate += "-09:00"
        elif "-" not in specificDate:
            raise Exception("SyntaxError: Date must be formatted yyyy-mm-dd-hh:mm")

        date = datetime(int(specificDate[:4]), int(specificDate[5:7]), int(specificDate[8:10]),
                        hour=int(specificDate[11:13]), minute=int(specificDate[14:]))
    else:
        date = datetime.now()

    workingCounter = 0

    if date.hour >= 9:
        # After cutoff time
        if date.month in [1, 4, 7, 10]:
            # Jan, Apr, Jul, Oct
            workingDay = 14
        else:
            # Other months
            workingDay = 9

        # Returns how many days are in the specified month
        start, end = monthrange(date.year, date.month)

        for i in range(1, end + 1):

            if datetime(date.year, date.month, i).weekday() in list(range(5)):
                # If it is a working day
                workingCounter += 1

                if workingCounter == workingDay:
                    # If it has reached specified number of working day
                    workingDay = i
                    break

        if date.day == workingDay:
            return True

    return False
