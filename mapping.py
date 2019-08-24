import operator
import math
import time
import statistics

## Part 3
class ShakespeareToken(str):
	def __init__(self, string):
		self._string = string

	def __hash__(self):
		return len(self._string)

## Part 4
class ShakespeareToken2(str):
	def __init__(self, string):
		self._string = string

	def __hash__(self):
		sum = 0
		for char in self._string:
			sum += ord(char)
		return sum

class ShakespeareToken3(str):
	def __init__(self, string):
		self._string = string

	def __hash__(self):
		p = 53
		sum = 0
		for x in range(len(self._string)-1, -1, -1):
			sum *= p
			sum += ord(self._string[x])
		return sum

class Entry:
	def __init__(self, key, value):
		self.key = key
		self.value = value

	def __str__(self):
		return "%d: %s" % (self.key, self.value)

class ListMapping:
	def __init__(self):
		self._entries = []

	def put(self, key, value):
		#print("ListMapping put", key)
		e = self._entry(key)
		if e is not None:
			e.value = value
		else:
			self._entries.append(Entry(key, value))

	def get(self, key):
		#print("ListMapping get", self, key)
		e = self._entry(key)
		if e is not None:
			return e.value
		else:
			raise KeyError

	def _entry(self, key):
		#print("ListMapping _entry", self, key)
		for e in self._entries:
			if e.key == key:
				return e
		return None

	def _entryIter(self):
		return (e for e in self._entries)

	def __str__(self):
		return str([str(e) for e in self._entries])

	def __getitem__(self, key):
		return self.get(key)

	def __setitem__(self, key, value):
		self.put(key, value)

	def __len__(self):
		return len(self._entries)

	def __contains__(self, key):
		if self._entry(key) is None:
			return False
		else:
			return True

	def __iter__(self):
		return (e.key for e in self._entries)

	def values(self):
		return (e.value for e in self._entries)

	def items(self):
		return ((e.key, e.value) for e in self._entries)

	# def __bool__(self):
	# 	if self._entries:
	# 		return True
	# 	else:
	# 		return False

## Part 2
class HashMapping():
	def __init__(self, size = 1000):
		self._size = size
		self._buckets = [ListMapping() for i in range(self._size)]
		self._length = 0

	def __iter__(self):
		return (x for x in self._entryiter())

	def _entryiter(self):
		return (x for bucket in self._buckets for x in bucket)

	def get(self, key): #hmm
		x = self._bucket(key)
		if x:
			# print(type(x))
			return x
		else:
			raise KeyError

	def put(self, key, value):
		x = self._bucket(key)
		if key not in x:
			self._length += 1
		x[key] = value

	def __getitem__(self, key):
		x = self._bucket(key)
		return x[key]

	def __setitem__(self, key, value):
		x = self._bucket(key)
		if key not in x:
			self._length += 1
		x[key] = value

	def items(self): #return the entire data structure --> all of the buckets
		return ((x.key, x.value) for x in self._buckets)

	def __contains__(self, key): # 12:49, 4/12: returns true for everything
		try:
			x = self.get(key)
			if key in x:
				return True
			else:
				return False
		except KeyError:
			return False
		return True

	def __len__(self):
		# length = 0
		# for x in self._buckets:
		# 	if x:
		# 		length += 1
		# return length
		return self._length

	def _bucket(self, key):
		return self._buckets[hash(key) % self._size]

	def statistics(self):
		sizes = []
		total_buckets = self._size
		empty_buckets = 0
		largest_bucket = len(self._buckets[0])
		for bucket in self._buckets:
			x = len(bucket._entries)
			if not x:
				empty_buckets += 1
			elif x > largest_bucket:
				largest_bucket = x
			sizes.append(x)
		average_size = statistics.mean(sizes)
		# average_size = self._length / total_buckets
		std_dev = statistics.stdev(sizes)
		print(largest_bucket)
		return (total_buckets, empty_buckets, largest_bucket, average_size, std_dev)

	def largest(self):
		largestB = 0
		yes = None
		for bucket in self._buckets:
			x = len(bucket._entries)
			if x:
				if x > largestB:
					largestB = x
					yes = bucket
		return largestB

	# def _getBucketItems(self, key):
	# 	x = self._bucket(key)
	# 	print(len(x))
	# 	for item in x.items():
	# 		print(item)

## Part 5
## Don't forget to inherit HashMapping!
class ExtendableHashMapping(HashMapping):
	def get(self, key):
		x = self._bucket(key)
		if x:
			return x
		else:
			raise KeyError

	def put(self, key, value):
		x = self._bucket(key)
		if key not in x:
			self._length += 1
		x[key] = value
		if self._length == self._size:
			self._double()

	def __getitem__(self, key):
		x = self._bucket(key)
		if x:
			return x
		else:
			raise KeyError

	def __setitem__(self, key, value):
		x = self._bucket(key)
		if key not in x:
			self._length += 1
		x[key] = value
		if self._length == self._size:
			self._double()

	def _double(self):
		# Save a reference to the old buckets.
		oldbuckets = self._buckets
		# Double the size.
		self._size *= 2
		# Create new buckets
		self._buckets = [ListMapping() for i in range(self._size)]
		# Add in all the old entries.
		for bucket in oldbuckets:
			for key, value in bucket.items():
				# Identify the new bucket.
				m = self._bucket(key)
				m[key] = value


## Part 1
def getTokensFreq(file):
	f = open(file, "r")
	lines = f.read()
	words = lines.split()
	d = {}
	for word in words:
		text = word.lower()
		if text not in d:
			d[text] = 1
		else:
			d[text] += 1
	return d
	# d = {}
	# symbols = [',', '.', '', ';', ':', '!', '?']
	# f = open(file, "r")
	# f_file = f.read().replace('/n', ' ')
	# for word in f_file.split():
	# 	x = word.lower()
	# 	if x in symbols:
	# 		continue
	# 	if x in d:
	# 		d[x] += 1
	# 	else:
	# 		d[x] = 0 #fixes the off-by-one error
	# return d

def getMostFrequent(d, k):
	sorted_d = sorted(d.items(), key=operator.itemgetter(1)) #0 for keys, 1 for values
	i = len(sorted_d)-1
	k_list = []
	for x in range(i, 0, -1):
		k_list.append(sorted_d[x])
		k -= 1
		if k == 0:
			break
	return k_list

f = open('shakespeare.txt', 'r')
data = f.read()
f.close()
data = data.split()

map1 = HashMapping()
for i in range(len(data)):
   key = data[i]
   s = ShakespeareToken(key)	## try the other two ShakespeareToken classes
   if key not in map1:
	   map1[key] = hash(s)%map1._size

stats = map1.statistics()
print(map1.largest())
# self.assertEqual(stats[0], 1000)
# self.assertEqual(stats[1], 0)
# self.assertTrue(50 < stats[2] < 60)
# self.assertEqual(stats[3], 33.505)
# self.assertTrue(5.0 < stats[4], 6.5)
