
import time

import ciso8601

start = int(str(1593914400000)[:-3])

end = time.mktime(ciso8601.parse_datetime("2021-02-12").timetuple())


print(start > end)