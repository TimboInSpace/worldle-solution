#!/usr/bin/python3

# The plan:
# (1) make a request to the url
# (2) Find the img tag, and check its src property
# (3) src will end in "...[countrycode]/vector.png". Extract the country code
# (4) translate country code from https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#CZ

from requests_html import HTMLSession

url = "https://worldle.teuteuf.fr/"
tgt = "vector.svg"

# Locate the request for vector.svg and return the country code used to load the image
def getCountryCode(addr):
	with HTMLSession() as sesh:
		resp = sesh.get(addr, allow_redirects=True)
		resp.html.render() # render page and put it in resp.html
		imgs = resp.html.find('img')
		countryCode = ""
		for img in imgs:
			if img.attrs['src'].find(tgt) > 0:
				#print(img.attrs['src'])
				countryCode = img.attrs['src'].split('/')[-2]
				return countryCode.upper()

# Translate country code -> country name
def getCountryFromCode(cc):
	with HTMLSession() as sesh:
		resp = sesh.get("https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2")
		td = resp.html.find(f'td#{cc} + td', first=True)
		return td.find('a', first=True).attrs['title']
	
	
cc = getCountryCode(url)
country = getCountryFromCode(cc)
print(country)
