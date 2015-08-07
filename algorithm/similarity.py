def levenshtein(first, second):
    if len(first) > len(second):
        first,second = second,first
    if len(first) == 0:
        return len(second)
    if len(second) == 0:
        return len(first)
    if first == second:
        return 0
    first_length = len(first) + 1
    second_length = len(second) + 1
    distance_matrix = [range(second_length) for x in range(first_length)]
    for i in range(1,first_length):
        for j in range(1,second_length):
            deletion = distance_matrix[i-1][j] + 1
            insertion = distance_matrix[i][j-1] + 1
            substitution = distance_matrix[i-1][j-1]
            if first[i-1] != second[j-1]:
                substitution += 1
            distance_matrix[i][j] = min(insertion,deletion,substitution)
    return distance_matrix[first_length-1][second_length-1]

def lss_len(s1, s2):
    if not s1 or not s2:
        return 0
    max_len = 0
    matrix = [[0 for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i-1] == s2[j-1]:
                matrix[i][j] = matrix[i-1][j-1] + 1
                if matrix[i][j] > max_len:
                    max_len = matrix[i][j]
    return max_len

def lcs_len(s1, s2):
  m = [ [ 0 for x in s2 ] for y in s1 ]
  for p1 in range(len(s1)):
    for p2 in range(len(s2)):
      if s1[p1] == s2[p2]:
        if p1 == 0 or p2 == 0:
          m[p1][p2] = 1
        else:
          m[p1][p2] = m[p1-1][p2-1]+1
      elif m[p1-1][p2] < m[p1][p2-1]:
        m[p1][p2] = m[p1][p2-1]
      else:                             # m[p1][p2-1] < m[p1-1][p2]
        m[p1][p2] = m[p1-1][p2]
  return m[-1][-1]

def lcs(s1, s2):
  # length table: every element is set to zero.
  m = [ [ 0 for x in s2 ] for y in s1 ]
  # direction table: 1st bit for p1, 2nd bit for p2.
  d = [ [ None for x in s2 ] for y in s1 ]
  # we don't have to care about the boundery check.
  # a negative index always gives an intact zero.
  for p1 in range(len(s1)):
    for p2 in range(len(s2)):
      if s1[p1] == s2[p2]:
        if p1 == 0 or p2 == 0:
          m[p1][p2] = 1
        else:
          m[p1][p2] = m[p1-1][p2-1] + 1
        d[p1][p2] = 3                   # 11: decr. p1 and p2
      elif m[p1-1][p2] < m[p1][p2-1]:
        m[p1][p2] = m[p1][p2-1]
        d[p1][p2] = 2                   # 10: decr. p2 only
      else:                             # m[p1][p2-1] < m[p1-1][p2]
        m[p1][p2] = m[p1-1][p2]
        d[p1][p2] = 1                   # 01: decr. p1 only
  (p1, p2) = (len(s1)-1, len(s2)-1)
  # now we traverse the table in reverse order.
  s = []
  while 1:
    print p1,p2
    c = d[p1][p2]
    if c == 3: s.append(s1[p1])
    if not ((p1 or p2) and m[p1][p2]): break
    if c & 2: p2 -= 1
    if c & 1: p1 -= 1
  s.reverse()
  return ''.join(s)
