class CheckQueue:
	def __init__(self):
		self.domain = "https://es.asurso.ru"
		self.urlpost = "%s/municipality/set"%self.domain
		self.urlget = "%s/inquiry/search/no-cache"%self.domain
		self.data = {"isajax":"true",
					 "municipality":"8119a190-46a9-4b0a-9dfc-a5480156c40b"}
		self.path = './/*[@class = "table table-bordered"]/tbody/tr'
		self.addr = {"12":"ул.Красноармейская,93а","108":"ул.Коммунистическая,20",
				"121":"ул.Владимирская,24","172":"ул.Искровская,5","338":"ул.Ново-Садовая,9"}

	def set_number(self,number = None):
		self.number = number

	def get_page(self, number):
		self.payload = {"isRegisterHandler":"false","number":number}
		self.s = __import__("requests").Session()
		self.s.post(self.urlpost, self.data)
		return self.s.get(self.urlget,params=self.payload).text

	def get_queue(self,number = None):
		if number: self.number = number
		self.res = dict()
		self.page = __import__("lxml").html.fromstring(self.get_page(self.number))
		for i in self.page.xpath(self.path)[1:]:
			self.res[self.prep_key(i[0])]=int(i[1][0].text.strip()[:-8])
		return self.res

	def prep_key(self,s):
		return ''.join(i for i in s.text.strip() if i.isdigit())

	def get_addr(self):
		self.url = "http://samadm.ru/city_life/obrazovanie/detskie-sady/the-list-of-kindergartens"
		self.lst = __import__("requests").get(self.url)
		self.lst = __import__("lxml").html.fromstring(self.lst.content)
		self.result = dict()
		for i in page.xpath(path1)[1:]:
			self.result[self.prep_key(i[2])] =\
			i[3].text.strip().replace('город','г.').replace('дом','д.').replace('улица','ул.')[19:]
		return self.result

	def __str__(self):
		self.queue = self.get_queue()
		return '\n'.join('Д/с № {:<3s}: {:>2d} место ({})'.format(i[0],i[1],self.addr[i[0]])\
				for i in sorted(self.queue.items(),key=lambda x:x[1]))

if __name__ == "__main__":
	NUMBER = "36401/ЗЗ/1703091917"
	q = CheckQueue()
	q.set_number(NUMBER)
	print(q)