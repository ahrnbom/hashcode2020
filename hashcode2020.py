import numpy as np
from random import sample, choice
from pathlib import Path 

class Library:
    def __init__(self, library_id, signup_time, shipment_rate, books, S):
        self.library_id = library_id
        self.signup_time = signup_time
        self.shipment_rate = shipment_rate
        books.sort(key = lambda x : S[x], reverse=True)
        self.sorted_books = np.array(books)
        self.S = S

    #Preemptively evaluates score for this library given the time left
    def evaluate(self, time_left, all_shipped_books):
        time = time_left - self.signup_time
        if time <= 0:
            return 0, np.array([], dtype=int)
        no_shipped_books = time * self.shipment_rate

        # Compute which books that can be shipped (no duplicates, no time travels)
        shipped_books = self.sorted_books.copy()
        already_shipped = all_shipped_books[shipped_books]
        shipped_books = shipped_books[already_shipped==False]
        shipped_books = shipped_books[:no_shipped_books]

        scores = self.S[shipped_books]
        score = np.sum(scores)
        return score, shipped_books

    def __repr__(self):
        if len(self.sorted_books) > 5:
            b = str(self.sorted_books[:2]) + '(...)' + str(self.sorted_books[:2])    
        else:
            b = self.sorted_books
        return f"Library(id={self.library_id}, signup_time={self.signup_time}, shipment_rate={self.shipment_rate}, sorted_books={b})"

def process_library(data):
    score, books = data['library'].evaluate(data['time_left'], data['all_shipped_books'])
    return (data['library'], score, books)

def calculate_solution(all_libraries, sample_amount=0):
    libraries = [x for x in all_libraries]
    libraries_in_order = list()
    all_shipped_books = np.zeros((B,), dtype=bool)
    time_left = D
    total_score = 0
    while(True):
        if not libraries:
            break
        
        best_score = 0
        best_library = None
        best_books = None 
        
        datas = [{'library':library, 'time_left': time_left, 'all_shipped_books':all_shipped_books} for library in libraries]
        if sample_amount > 0:
            datas = sample(datas, sample_amount)
        out = [process_library(data) for data in datas]

        for library, score, shipped_books in out:
            if score > best_score:
                best_score = score
                best_library = library
                best_books = shipped_books
        
        if not best_library:
            break
        
        time_left -= best_library.signup_time
        if time_left < 0:
            break

        if choice([True, False, False, False]):
            print("Time left:", time_left)

        #library is chosen
        libraries.remove(best_library)
        all_shipped_books[best_books] = True
        total_score += best_score
        libraries_in_order.append((best_library, best_books))

    return libraries_in_order, total_score

names = ["a_example", "b_read_on", "c_incunabula", "d_tough_choices", "e_so_many_books", "f_libraries_of_the_world"]
name = names[3]
sample_amount = 0 # For d_tough_choices, set sample_amount to something like 2-4. Higher numbers run slower but finds better solutions on average.
infile = Path('input') / f"{name}.txt"
intext = infile.read_text()
lines = intext.split("\n")
first = lines[0]
B,L,D = [int(x) for x in first.split()]

S = np.array([int(x) for x in lines[1].split()])

libraries = list()

for l in range(L):
    N, T, M = [int(x) for x in lines[2*l + 2].split()]
    books = [int(x) for x in lines[2*l + 3].split()]
    library = Library(l, T, M, books, S)
    libraries.append(library)

solution, score = calculate_solution(libraries, sample_amount)
print(score)

outfile = Path('output') / f"{name}.txt"

text = [str(len(solution))]
for library, books in solution:
    text.append(f"{library.library_id} {len(books)}")
    text.append(' '.join([str(x) for x in books]))

outfile.write_text('\n'.join(text))

