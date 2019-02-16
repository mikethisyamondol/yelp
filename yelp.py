from bs4 import BeautifulSoup
import requests
import nltk
import regex as re
import heapq  

# Extract reviews into list
def extract_review(yelp_url):
	reviews = []
	url = yelp_url
	for i in range(1,10):
	    result = requests.get(url)
	    html = result.text
	    soup = BeautifulSoup(html, "lxml")
	    review_div = soup.find_all('div', {'class':'review-content'})
	    for element in review_div:
	        p = element.find('p')
	        if p:
	            reviews.append(p.text)
	    url = yelp_url + str(len(reviews))
	return reviews


# Tokenize +  n-grams
def tokenize(reviews):

	# Lowercase text + remove non alpha numeric characters
	input = [i.lower() for i in reviews]
	input = [re.sub("[^\w\s]", '', i) for i in input]
	input = [i.replace("\xa0", '') for i in input]

	# Break sentence in the token, remove empty tokens
	tokens = [nltk.tokenize.SpaceTokenizer().tokenize(i) for i in input]
	return tokens


# Word Scores
def word_score(tokenized_reviews):
	stopwords = nltk.corpus.stopwords.words("english")

	# Find word frequencies
	word_frequencies = {}

	for review in tokenized_reviews:  
	    for word in review:
	        if word not in stopwords:
	            if word not in word_frequencies.keys():
	                word_frequencies[word] = 1
	            else:
	                word_frequencies[word] += 1

	# Divide word frequencies by maximum frequency to get word scores
	max_freq = max(word_frequencies.values())

	for word in word_frequencies.keys():
	    word_frequencies[word] = word_frequencies[word] / max_freq
	
	return word_frequencies


# Review Scores
def review_score(reviews, word_frequencies, max_word_count):
	review_scores = {}  
	for review in reviews:  
	    for word in nltk.word_tokenize(review.lower()):
	        if word in word_frequencies.keys():
	            if len(review.split(' ')) < max_word_count:
	                if review not in review_scores.keys():
	                    review_scores[review] = word_frequencies[word]
	                else:
	                    review_scores[review] += word_frequencies[word]
	return review_scores


# Summary
def summary_reviews(review_scores, num_reviews):
	summary_reviews = heapq.nlargest(num_reviews, review_scores, key=review_scores.get)
	summary = '| '.join(summary_reviews)
	output = print(summary)
	return output


#Input formatting
restaurant = input("Input name of restaurant.  ")
city = input("Input name of NYC borough.  ")

restaurant = restaurant.replace(' ', '-').lower()

if city.lower() == 'manhattan':
	city = 'new-york'

city = city.replace(' ', '-').lower()


#Call functions
reviews = extract_review("https://www.yelp.com/biz/" + restaurant + "-" + city)
tokenize = tokenize(reviews)
word_score = word_score(tokenize)
review_scores = review_score(reviews, word_score, 60)
summary_reviews(review_scores, 5)


# if __name__ == "__main__":
#     main()







