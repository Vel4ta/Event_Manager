class DateBuilder:
    
    def __init__(self, raw_date: str):
        self.raw_date = raw_date
    
    def get_month(self):
        months = {}
        for i, m in enumerate(["january", "febuary", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]):
            months[m] = i + 1
        return months[self.raw_date.split(" ")[0].strip().lower()]
    def get_day(self):
        return int(self.raw_date.split(",", 1)[0].split(" ", 1)[1].split(" - ")[0].strip())
    def get_year(self):
        try:
            return int(self.raw_date.split(",")[1].strip())
        except:
            return 2023
    def get_time(self):
        # 0 - 23
        def convert(time):
            if "pm" in time:
                hr, min = time.split("pm")[0].split(":")
                min = float(min)/100.0
                time = float(hr)
                if time < 12.0:
                    time += 12.0
                time += min
            else:
                hr, min = time.split("am")[0].split(":")
                min = float(min)/100.0
                time = float(hr)
                if time == 12.0:
                    time -= time
                time += min
            return time
        temp = self.raw_date.split(",")[-1].split(" to ")
        if len(temp) == 1:
            return convert(temp[0].strip()), convert(temp[0].strip())
        start, end = temp
        return convert(start.strip()), convert(end.strip())
    
    def less_than_equal(self, date):
        return self.get_year() <= date.get_year() and (self.get_month() < date.get_month() or (self.get_month() == date.get_month() and (self.get_day() < date.get_day() or (self.get_day() == date.get_day() and self.get_time()[-1] <= date.get_time()[-1]))))
    
    def makeDate(self):
        start, end = self.get_time()
        return (self.get_year(), self.get_month(), self.get_day(), start, end)

    def displayDate(self):
        o = ""
        for value in self.makeDate():
            o += str(value) + " "
        return o.strip()