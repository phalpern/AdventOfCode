CXX = clang++
CXX_FLAGS = -std=c++20 -g -I.

.FORCE:

 .PRECIOUS : puzzle%.exe

puzzle% : puzzle%.exe .FORCE
	./$< $(ARG)

puzzle%.exe : puzzle%.cpp aoc_util.h
	$(CXX) $(CXX_FLAGS) $< -o $@
