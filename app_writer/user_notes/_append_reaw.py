import sys
with open('user_notes/reaw_reference.md', 'a') as f:
    f.write(sys.stdin.read())
