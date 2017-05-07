##  Between Two Cities scorer
##
##    s - shop, yellow
##    f - factory, gray
##    1,2,3,4 - (music, food, drink, bed) tavern, red
##    o - office, blue
##    p - park, green
##    h - house, brown
##
##    s s s f
##    1 o 3 p
##    h h o 2
##    h h p s
##    ==>    'sssg1o3phho2hhps'



# Originally this just used modular arithmetic, but it was clunky/unreadable
neighbors = {
  0:[1,4], 1:[0,2,5], 2:[1,3,6], 3:[2,7],
  4:[0,5,8], 5:[1,4,6,9], 6:[2,5,7,10], 7:[3,6,11],
  8:[4,9,12], 9:[5,8,10,13], 10:[6,9,11,14], 11:[7,10,15],
  12:[8,13], 13:[9,12,14], 14:[10,13,15], 15:[11,14]
}

def has_neighbor(city, i, x):
    for j in neighbors[i]:
      if city[j] in x:
        return True
    return False

def score_city(city, most_factories=False, second_most_factories=False):
  if len(city) != 16:
    raise "No"

  score = 0
  score += score_houses(city)
  score += score_taverns(city)
  score += score_offices(city)
  score += score_factories(city, most_factories, second_most_factories)
  score += score_shops(city)
  score += score_parks(city)
  return score

def score_city_verbose(city, most_factories=False, second_most_factories=False):
  if len(city) != 16:
    raise "No"

  houses = score_houses(city)
  taverns = score_taverns(city)
  offices = score_offices(city)
  factories = score_factories(city, most_factories, second_most_factories)
  shops = score_shops(city)
  parks = score_parks(city)
  total = houses + taverns + offices + factories + shops + parks

  print("----")
  print(city[:4])
  print(city[4:8])
  print(city[8:12])
  print(city[12:])
  print("----")
  print("Houses: ", houses)
  print("Taverns: ", taverns)
  print("Offices: ", offices)
  print("Factories: ", factories)
  print("Shops: ", shops)
  print("Parks: ", parks)
  print("Total: ", total)
  
def score_houses(city):
  score = 0
  house_score = 0
  
  for x in 'sfop':
    if x in city:
      house_score += 1
  for x in '1234':
    if x in city:
      house_score += 1
      break
  
  for i in range(16):
    if city[i] == 'h':
      score += house_score if not has_neighbor(city, i, 'f') else 1
  
  return score


def score_taverns(city):
  score = 0
  tavern_scores = [0,1,4,9,17]
  tiles_scored = [False]*16
  
  j = 1
  while j > 0:
    s = ''
    j = 0
    for i in range(16):
      if city[i] in '1234' and city[i] not in s and not tiles_scored[i]:
        tiles_scored[i] = True
        s += city[i]
        j += 1
    score += tavern_scores[j]
  
  return score


def score_offices(city):
  score = 0
  office_scores = [0,1,3,6,10,15,21] ## Hey triangular numbers
  
  offices_count = city.count('o')
  score += 21 * (offices_count // 6) + office_scores[offices_count % 6]
  
  for i in range(16):
    if city[i] == 'o' and has_neighbor(city, i, '1234'):
      score += 1
  
  return score

# Possibly change parameter names to "pittsburgh" and "semi-pittsburgh"
def score_factories(city, most_factories=False, second_most_factories=False):
  if most_factories:
    return 4 * city.count('f')
  elif second_most_factories:
    return 3 * city.count('f')
  else:
    return 2 * city.count('f')

def score_shops(city):
  score = 0
  tiles_scored = [False]*16
  shop_scores = [0,2,5,10,16]
  
  def shop_match(lst):
    for x in lst:
      if city[x] != 's' or tiles_scored[x]:
        return 0
    for x in lst:
      tiles_scored[x] = True
    return shop_scores[len(lst)]
  
  for i in [0,4,8,12]:
    score += shop_match([i, i+1, i+2, i+3])
  for i in [0,1,2,3]:
    score += shop_match([i, i+4, i+8, i+12])
  for i in [0,1,4,5,8,9,12,13]:
    score += shop_match([i, i+1, i+2])
  for i in [0,1,2,3,4,5,6,7]:
    score += shop_match([i, i+4, i+8])
  for i in [0,1,2,4,5,6,8,9,10,12,13,14]:
    score += shop_match([i, i+1])
  for i in [0,1,2,3,4,5,6,7,8,9,10,11]:
    score += shop_match([i, i+4])
  for i in range(16):
    score += shop_match([i])

  return score

def score_parks(city):
  visited = [False]*16
  groups = [0]*16
  
  def visit(tile, group):
    groups[tile] = group
    visited[tile] = True
    
    for i in neighbors[tile]:
      if not visited[i] and city[i] == 'p':
        visit(i, group)
  
  group = 1
  for i in range(16):
    if city[i] == 'p' and not visited[i]:
      visit(i, group)
      group += 1
  
  score = 0
  for i in range(1,group):
    k = groups.count(i)
    score += 6*k-4 if k < 3 else k+9
  
  return score
  

test_cities = [
  'sssshho1opooophp', ## 56
  '1fffppfpss1phhhf', ## 42
  '13ffh2fpsh4phhho', ## 59
  '13ffo2o4oooossss', ## 62
  '13hhs2o4sohhsfpp', ## 62
  'fsffpfppf4hppphh'  ## 47
]
