#!/bin/bash
# argv[1] = p1type
# argv[2] = p2type
# argv[3] = p1_eval_type
# argv[4] = p1_prune
# argv[5] = p2_eval_type
# argv[6] = p2_prune
# argv[7] = p1_depth
# argv[8] = p2_depth

p1type="alphabeta"
p2type="human"
p1_eval_type=0
p1_prune=0
p2_eval_type=2
p2_prune=0
p1_depth=0
p2_depth=9

python GameDriver.py $p1type $p2type $p1_eval_type $p1_prune $p2_eval_type $p2_prune $p1_depth $p2_depth