#!/usr/bin/env python3

import re

OUTPUT_PATH = '/path/to/imdb/output'

class Row():
  def __init__(self, title = '', genre = '', gender_ratio = 0.0, rating=0.0, votes=0, actors = 0, actresses = 0, director = 'NO_DIRECTOR', year='????'):
    self.title = title
    self.genre = genre
    self.gender_ratio = gender_ratio # Male:Female
    self.rating = rating
    self.votes = votes
    self.actors = actors
    self.actresses = actresses
    self.director = director
    self.year = year

  def __str__(self):
    return '%s\t%s\t%.04f\t%.02f\t%d\t%s\t%s' % (self.title, self.genre, self.gender_ratio, self.rating, self.votes, self.director, self.year)

def filter_unique(lst, on_idx):
  d = {}
  lst2 = []
  for item in lst:
    k = item[on_idx]
    if not k in d.keys():
      d[k] = True
      lst2.append(item)
  return lst2

def read_tsv(name):
  lst = []
  with open(OUTPUT_PATH + '/' + name, 'r', encoding='UTF-8') as f:
    lst = [x.strip().split('\t') for x in f.readlines()]
  return lst

def find_item(lst, query, match_idx, return_idx):
  for i in lst:
    if i[match_idx] == query:
      return i[return_idx]
  return None

def tuple_to_dict(lst, idx_key, idx_value):
  d = {}
  for item in lst:
    d[item[idx_key]] = item[idx_value]
  return d

def create_count_dict(lst, key_idx):
  d = {}
  for row in lst:
    k = row[key_idx]
    if k in d.keys():
      d[k] += 1
    else:
      d[k] = 1
  return d

def extract_years(lst):
  pat1 = r'\(.*[0-9]*.*\)'
  pat2 = r'[0-9][0-9][0-9][0-9]'
  out = []
  for i in lst:
    o1 = re.search(pat1, i[1])
    if o1:
      o2 = re.search(pat2, o1.group())
      if o2:
        out.append(o2.group())
      else:
        out.append('????')
    else:
      out.append('????')
  return out

def main():
  print('[1] Reading actors.list.tsv')
  actors = {}
  ac = 0
  with open(OUTPUT_PATH + '/actors.list.tsv', 'r', encoding='UTF-8') as f:
    for line in f:
      key = line.strip().split('\t')[2]
      if key in actors.keys():
        actors[key] += 1
      else:
        actors[key] = 1

  print(len(actors.keys()))
  print('[2] Reading actresses.list.tsv')
  actresses = {}
  with open(OUTPUT_PATH + '/actresses.list.tsv', 'r', encoding='UTF-8') as f:
    for line in f:
      key = line.strip().split('\t')[2]
      if key in actresses.keys():
        actresses[key] += 1
      else:
        actresses[key] = 1

  table = []
  print('[3] Reading movies.list.tsv')
  movies = read_tsv('movies.list.tsv')
  print('[3] Filtering on unique titles')
  movies = filter_unique(movies, 1)
  years = extract_years(movies)
  print('[3] Extracting movie titles from table')
  movies = [x[1] for x in movies]

  print('[3] Constructing first column: Titles')
  for i, title in enumerate(movies):
    table.append(Row(title=title, year=years[i]))

  # Might be several GBs, so explicitely del
  del movies

  print('[4] Reading genres.list.tsv')
  genres = read_tsv('genres.list.tsv')

  print('[4] Filtering on unique titles (keep first genre)')
  genres = filter_unique(genres, 0)

  print('[4] Translating title / genre list to dictionary for fast lookups')
  genres = tuple_to_dict(genres, 0, 1)

  for row in table:
    if row.title in genres.keys():
      row.genre = genres[row.title]
    else:
      pass
      #print('[!] Error: %s does not have a matching genre' % row.title)

  del genres

  print('[5] Reading ratings.list.tsv')
  ratings = read_tsv('ratings.list.tsv')

  print('[5] Filtering on unique titles (keep first rating)')
  ratings = filter_unique(ratings, 3)

  print('[5] Translating title / n_votes and rating list to dictionary for fast lookups')
  n_ratings = tuple_to_dict(ratings, 3, 1)
  ratings = tuple_to_dict(ratings, 3, 2)

  for row in table:
    if row.title in ratings.keys():
      row.rating = float(ratings[row.title])
      row.votes = int(n_ratings[row.title])

  del ratings
  del n_ratings

  print('[6] Reading directors.list.tsv')
  directors = read_tsv('directors.list.tsv')
  d = {}
  directors2 = {}
  for item in directors:
    k = item[0] + ' ' + item[1]
    k2 = item[2]
    if not k in d.keys():
      d[k] = [item[2]]
      directors2[k2] = k
    elif item[2] not in d[k]:
      d[k].append(item[2])
      directors2[k2] = k

  del directors
  del d

  directors = directors2

  for row in table:
    if row.title in directors.keys():
      row.director = directors[row.title]

  for row in table:
    if row.title in actors.keys():
      row.actors = actors[row.title]
    if row.title in actresses.keys():
      row.actresses = actresses[row.title]
    if row.actors > 0 and row.actresses > 0:
      row.gender_ratio = float(row.actors) / float(row.actresses)

  # Obtain viable candidates (must have rating > 100 & genre & at least one male & female actor)
  #table2 = []
  #for row in table:
  #  if row.genre != '' and row.votes > 100 and row.gender_ratio != 0.0:
  #    table2.append(row)
  #table = table2

  with open('output.tsv', 'w', encoding='UTF-8') as f:
    f.write('title\tgenre\tgender_ratio\trating\tvotes\tdirector\tyear\n')
    for row in table:
      f.write(str(row) + '\n')

if __name__ == '__main__':
  main()
