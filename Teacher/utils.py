from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Schedule

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None,classcode = None):
		self.year = year
		self.month = month
		self.classcode = classcode
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(event_date__day=day)
		d = ''
		for event in events_per_day:
			d += f'<li> {event.event_data} </li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = Schedule.objects.filter(event_date__year=self.year, event_date__month=self.month, class_code = self.classcode)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal