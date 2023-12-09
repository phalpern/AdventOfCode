CXX = clang++
OPT := -g
CXX_FLAGS = -std=c++20 -I. $(OPT)

.FORCE:

 .PRECIOUS : puzzle%.exe

puzzle% : puzzle%.exe .FORCE
	time ./$< $(ARG)

puzzle%.exe : puzzle%.cpp aoc_util.h
	$(CXX) $(CXX_FLAGS) $< -o $@
