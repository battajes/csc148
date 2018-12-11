/usr/local/bin/python3.7 /local/packages/pycharm-community-2018.2.2/helpers/pydev/pydevconsole.py 36167 39707

import sys; print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend(['/h/u4/c8/04/wattpatr/csc148'])

Python 3.7.0 (default, Aug 10 2018, 16:34:38) 
Type 'copyright', 'credits' or 'license' for more information
IPython 6.5.0 -- An enhanced Interactive Python. Type '?' for help.
PyDev console: using IPython 6.5.0

Python 3.7.0 (default, Aug 10 2018, 16:34:38) 
[GCC 5.4.0 20160609] on linux
In[2]: runfile('/h/u4/c8/04/wattpatr/csc148/assignments/a2/prefix_tree.py', wdir='/h/u4/c8/04/wattpatr/csc148/assignments/a2')
[] (0.5)
  ['a'] (0.5)
    ['a', 'b'] (0.5)
      ['a', 'b', 'c'] (0.5)
        abc (0.5)

[] (0.7)
  ['a'] (0.7)
    ['a', 'b'] (0.7)
      ab (0.2)
      ['a', 'b', 'c'] (0.5)
        abc (0.5)

In[3]: x.add_on('abdfg',0.1,['a','b','d','f','g'])
In[4]: print(str(x))
[] (0.7999999999999999)
  ['a'] (0.7999999999999999)
    ['a', 'b'] (0.7999999999999999)
      ab (0.2)
      ['a', 'b', 'c'] (0.5)
        abc (0.5)
      ['a', 'b', 'd'] (0.1)
        ['a', 'b', 'd', 'f'] (0.1)
          ['a', 'b', 'd', 'f', 'g'] (0.1)
            abdfg (0.1)

In[5]: x.add_on('abb', 0.2, ['a','b','c'])
In[6]: print(str(x))
[] (1.0)
  ['a'] (1.0)
    ['a', 'b'] (1.0)
      ab (0.2)
      ['a', 'b', 'c'] (0.7)
        abb (0.2)
        abc (0.5)
      ['a', 'b', 'd'] (0.1)
        ['a', 'b', 'd', 'f'] (0.1)
          ['a', 'b', 'd', 'f', 'g'] (0.1)
            abdfg (0.1)

In[7]: y = SimplePrefixTree()
In[8]: y = add_nw('abc', 0.1, ['a','b','c'])
Traceback (most recent call last):
  File "/usr/local/packages/python-3.7/lib/python3.7/site-packages/IPython/core/interactiveshell.py", line 2961, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-8-416f713a6cb8>", line 1, in <module>
    y = add_nw('abc', 0.1, ['a','b','c'])
NameError: name 'add_nw' is not defined
In[9]: y.add_nw('abc', 0.1, ['a','b','c'])
In[10]: print(str(y))
[] (0.1)
  ['a'] (0.1)
    ['a', 'b'] (0.1)
      ['a', 'b', 'c'] (0.1)
        abc (0.1)

In[11]: y.add_nw('abb',0.2,['a','b','b'])
In[12]: print(str(y))
[] (0.30000000000000004)
  ['a'] (0.1)
    ['a', 'b'] (0.1)
      ['a', 'b', 'c'] (0.1)
        abc (0.1)
  ['a'] (0.2)
    ['a', 'b'] (0.2)
      ['a', 'b', 'b'] (0.2)
        abb (0.2)

