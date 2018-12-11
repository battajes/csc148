# tests where remove fails

x = CompressedPrefixTree()
    # x.insert('hi', 1, ['h', 'i'])
    # print(str(x))
    # x.insert('hello', 3, ['h', 'i'])
    # print(str(x))
    # x.insert('he', 2, ['h', 'e'])
    # print(str(x))
    # x.insert('cats', 6, ['c', 'a', 't', 's'])
    # print(str(x))
    # print(compare_prefix(['h','i'],['h']))
    x.insert('car', 1, ['c', 'a', 'r'])
    x.insert('care', 2, ['c', 'a', 'r','e'])
    x.insert('cat', 6, ['c', 'a', 't'])
    x.insert('danger', 1, ['d', 'a', 'n','g','e','r'])
    x.insert('door', 0.5, ['d', 'o', 'o','r'])
    x.insert('doors', 0.5, ['d', 'o', 'o', 'r', 's'])
    print(str(x))
    x.insert('doors', 0.5, ['d', 'o', 'o', 'r', 's'])

[] (1.8333333333333333)
  ['c', 'a'] (3.0)
    ['c', 'a', 't'] (6.0)
      cat (6.0)
    ['c', 'a', 'r'] (1.5)
      ['c', 'a', 'r', 'e'] (2.0)
        care (2.0)
      car (1.0)
  ['d'] (0.6666666666666666)
    ['d', 'a', 'n', 'g', 'e', 'r'] (1.0)
      danger (1.0)
    ['d', 'o', 'o', 'r'] (0.5)
      door (0.5)
      ['d', 'o', 'o', 'r', 's'] (0.5)
        doors (0.5)

In[3]: x.remove(['d'])
In[4]: print(str(x))
[] (3.5555555555555554)
  ['c', 'a'] (3.0)
    ['c', 'a', 't'] (6.0)
      cat (6.0)
    ['c', 'a', 'r'] (1.5)
      ['c', 'a', 'r', 'e'] (2.0)
        care (2.0)
      car (1.0)

In[5]: x.remove(['c','a','t'])
In[6]: print(str(x))
[] (3.5555555555555554)
  ['c', 'a'] (3.0)
    ['c', 'a', 't'] (6.0)
      cat (6.0)
    ['c', 'a', 'r'] (1.5)
      ['c', 'a', 'r', 'e'] (2.0)
        care (2.0)
      car (1.0)

In[9]: x.remove(['c','a'])
In[10]: print(str(x))
[] (3.5555555555555554)
  ['c', 'a'] (3.0)
    ['c', 'a', 't'] (6.0)
      cat (6.0)
    ['c', 'a', 'r'] (1.5)
      ['c', 'a', 'r', 'e'] (2.0)
        care (2.0)
      car (1.0)

In[11]: x.remove([])

if True:
  pass
elif similarity == len(prefix) + (-c + 1) and \
  len(self.subtrees[i].value) == len(prefix):
elif similarity == len(prefix):
  # alternative to next case?
  # when ab is inserted to abc
  pass
elif 0 < similarity and \
  similarity + 1 == len(self.subtrees[i].value) + (-c + 1):
