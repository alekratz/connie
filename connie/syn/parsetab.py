
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'bodyIDENT LBRACE LBRACKET NUM_LIT RBRACE RBRACKET SET STR_LIT SYM VAR\n        body        : atom body\n        \n        body        :\n        \n        atom    : quote\n                | value\n                | assign\n                | list\n                | sym\n                | ident\n        \n        ident : IDENT\n        sym   : SYMlist  : LBRACKET body RBRACKETassign : SETquote : LBRACE body RBRACE\n        value   : STR_LIT\n        \n        value   : NUM_LIT\n        \n        value   : VAR\n        '
    
_lr_action_items = {'$end':([0,1,2,3,4,5,6,7,8,10,11,12,13,15,16,17,20,21,],[-2,0,-2,-3,-4,-5,-6,-7,-8,-14,-15,-16,-12,-10,-9,-1,-13,-11,]),'LBRACE':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,20,21,],[9,9,-3,-4,-5,-6,-7,-8,9,-14,-15,-16,-12,9,-10,-9,-13,-11,]),'STR_LIT':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,20,21,],[10,10,-3,-4,-5,-6,-7,-8,10,-14,-15,-16,-12,10,-10,-9,-13,-11,]),'NUM_LIT':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,20,21,],[11,11,-3,-4,-5,-6,-7,-8,11,-14,-15,-16,-12,11,-10,-9,-13,-11,]),'VAR':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,20,21,],[12,12,-3,-4,-5,-6,-7,-8,12,-14,-15,-16,-12,12,-10,-9,-13,-11,]),'SET':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,20,21,],[13,13,-3,-4,-5,-6,-7,-8,13,-14,-15,-16,-12,13,-10,-9,-13,-11,]),'LBRACKET':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,20,21,],[14,14,-3,-4,-5,-6,-7,-8,14,-14,-15,-16,-12,14,-10,-9,-13,-11,]),'SYM':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,20,21,],[15,15,-3,-4,-5,-6,-7,-8,15,-14,-15,-16,-12,15,-10,-9,-13,-11,]),'IDENT':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,20,21,],[16,16,-3,-4,-5,-6,-7,-8,16,-14,-15,-16,-12,16,-10,-9,-13,-11,]),'RBRACE':([2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,18,20,21,],[-2,-3,-4,-5,-6,-7,-8,-2,-14,-15,-16,-12,-10,-9,-1,20,-13,-11,]),'RBRACKET':([2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,19,20,21,],[-2,-3,-4,-5,-6,-7,-8,-14,-15,-16,-12,-2,-10,-9,-1,21,-13,-11,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'body':([0,2,9,14,],[1,17,18,19,]),'atom':([0,2,9,14,],[2,2,2,2,]),'quote':([0,2,9,14,],[3,3,3,3,]),'value':([0,2,9,14,],[4,4,4,4,]),'assign':([0,2,9,14,],[5,5,5,5,]),'list':([0,2,9,14,],[6,6,6,6,]),'sym':([0,2,9,14,],[7,7,7,7,]),'ident':([0,2,9,14,],[8,8,8,8,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> body","S'",1,None,None,None),
  ('body -> atom body','body',2,'p_body','parse.py',28),
  ('body -> <empty>','body',0,'p_empty_body','parse.py',34),
  ('atom -> quote','atom',1,'p_atom','parse.py',40),
  ('atom -> value','atom',1,'p_atom','parse.py',41),
  ('atom -> assign','atom',1,'p_atom','parse.py',42),
  ('atom -> list','atom',1,'p_atom','parse.py',43),
  ('atom -> sym','atom',1,'p_atom','parse.py',44),
  ('atom -> ident','atom',1,'p_atom','parse.py',45),
  ('ident -> IDENT','ident',1,'p_ident','parse.py',51),
  ('sym -> SYM','sym',1,'p_sym','parse.py',56),
  ('list -> LBRACKET body RBRACKET','list',3,'p_list','parse.py',60),
  ('assign -> SET','assign',1,'p_assign','parse.py',66),
  ('quote -> LBRACE body RBRACE','quote',3,'p_quote','parse.py',70),
  ('value -> STR_LIT','value',1,'p_str_value','parse.py',77),
  ('value -> NUM_LIT','value',1,'p_int_value','parse.py',83),
  ('value -> VAR','value',1,'p_var_value','parse.py',89),
]