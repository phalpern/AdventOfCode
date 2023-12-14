CXX = clang++
OPT := -g
CXX_FLAGS = -std=c++20 -I. -Wall $(OPT)

.FORCE:

.PRECIOUS : bin/puzzle%.exe

puzzle% : bin/puzzle%.exe .FORCE
	time ./$< $(ARG)

bin/puzzle%.exe : puzzle%.cpp aoc_util.h
	$(CXX) $(CXX_FLAGS) $< -o $@
