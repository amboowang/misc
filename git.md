# Git Related

## What's the difference between HEAD^ and HEAD~ in Git?


Both ~ and ^ on their own refer to the parent of the commit (~~ and ^^ both refer to the grandparent commit, etc.) But they differ in meaning when they are used with numbers:

"\~2" means up two levels in the hierarchy, via the first parent if a commit has more than one parent
"\^2" means the second parent where a commit has more than one parent (i.e. because it's a merge)
These can be combined, so HEAD~2^3 means HEAD's grandparent commit's third parent commit

example:

G   H   I   J
 \ /     \ /
  D   E   F
   \  |  / \
    \ | /   |
     \|/    |
      B     C
       \   /
        \ /
         A

A =      = A^0
B = A^   = A^1     = A~1
C = A^2  = A^2
D = A^^  = A^1^1   = A~2
E = B^2  = A^^2
F = B^3  = A^^3
G = A^^^ = A^1^1^1 = A~3
H = D^2  = B^^2    = A^^^2  = A~2^2
I = F^   = B^3^    = A^^3^
J = F^2  = B^3^2   = A^^3^2
