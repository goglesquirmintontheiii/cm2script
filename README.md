# cmscript
circuitmakerscript (or cmscript for short) is a simple way to write circuits. It is designed for a Roblox game named cm2, but with some work, it can be adapted for many other uses.
It should be noted that this script has been tested and works, but it has zero dummy-proofing. Using it in any way that is unintended may result in various errors.


## Docs

### Variable initialization
Initializing variables is done via an equals ``=`` sign. An example of this: ``my_var_name = NOR``
When you initialize a variable, parameters are seperated by equals signs. 
If you supply 2 parameters, the first will be the variable name, and the second will be the block type that will be the value of the variable.
If you supply 3 parameters, the third parameter will be the properties the block is given.
It is highly recommended you avoid using symbols (specifically ':', '#', and '=') in variable names, though underscores and numbers wont cause issues. 

### Making connections
To make connections, you use '->'. An example of this would be ``var_1 -> var_2``, where ``var_1`` gets linked to ``var_2``. 
You cannot break or edit connections once they have been made.

### Buildings
Buildings are like classes in Python. To create one, you write the name, with a colon ':' after the name, with the code to go in that building after that line.
Code for buildings must be indented with any number of spaces.
Example of creating a building with an xor gate, a red tile, and an or gate:
```
example_building:
  xor1 = XOR
  tile1 = TILE = 255,0,0
  or1 = OR
```
Note that all variables intialized inside buildings are completely localized to that building.
Accessing variables that are outside buildings can be done via 'globals', for example: ``globals.xor1``
Accessing localized variables from outside buildings can be done via a simple dot '.', for example: ``example_building.xor1``
You cannot (currently) nest a building inside another building.

### Utility functions
Currently, you can clone any building or variable using ``:clone(count)``, where count is the number of clones to make (1 unless specified otherwise)
An example of cloning an xor gate stored in variable ``xor1``: ``xor1:clone()``
An example of cloning a building named ``adder`` 12 times: ``adder:clone(12)``
Cloned buildings will retain internal connections, but connections from inside the building to globals will not be copied.
Cloned text blocks will have their character incremented by 1 for each clone (for example, if the original text block had character 'A', the clones would have characters 'B', 'C', 'D', 'E', 'F', and so on..)
The name of clones will be the original name, with the index of the clone appended to it. For example, ``xor:clone(5)`` produces ``xor0``, ``xor1``, ``xor2``, ``xor3``, and ``xor4``. 

### Paralellization indexing (or just indexing)
Indexing allows you to make multiple links in one line of code.
Indexes utilize square brackets '[]' and must contain two parameters seperated by a colon ':'.
The first parameter is the number of variables to link, and the second is the offset.
Indexing goes by names (mainly as it is designed for working with clones). For example, an index of ``xor[3:2]`` would reference ``xor2``, ``xor3``, and ``xor4``. 
If you put an index by building name rather than at the end, it will access the number of buildings specified (the number parameter of the index), accessing the specified localized variable in each one  
For an example of indexing building names, ``adder[3:0].or`` would access the ``or`` in ``adder0``, ``adder1``, and ``adder2``, whereas ``adder.or[3:0]`` would access ``adder``'s ``or0``, ``or1``, and ``or2``

An excellent example of using indexing to make 16 total connections in only 2 lines:
```
texti = TEXT = 64
texto = TEXT = 64
or = OR
texti:clone(8)
texto:clone(8)
or:clone(8)
texti[8:0] -> or[8:0]
or[8:0] -> texto[8:0]
```

### Comments
Comments use hashtags '#'. Comments must be in their own lines, and must not share a line with other code.

# TLDR;/CHEATSHEET
```
var_name = block_type
var_name = block_type = block_properties
variable_or_building:clone()
variable_or_building:clone(number_of_clones)
var_name -> var_name_2
var_name[number_of_vars:start_offset] -> var_name_2[same_number_of_vars:start_offset]
building_name:
  indented_building_code
```

