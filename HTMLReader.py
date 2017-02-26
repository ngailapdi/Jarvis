from HTMLParser import HTMLParser
import urllib2
global arr
arr = []

class MyHTMLParser(HTMLParser):
	def handle_data(self, data):
		d = ""
		if "\xe2\x80\x9c" in data:
			for i in range(3, len(data)):
				if data[i] == "\xe2" or data[i] == "\x80" or data[i] == "\x93" or data[i] == "\x9d" or data[i] == "\x99" or data[i] == "\xc2" or data[i] == "\xa0" or data[i] == "\xa6":
					continue
				d += data[i]
			if len(d) > 0 and d[-1] == ".":
				arr.append(d)