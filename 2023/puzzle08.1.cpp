// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT
#include <aoc_util.h>
#include <array>
#include <map>
#include <utility>
#include <string_view>

using namespace aoc;

struct Node : std::array<char, 3>
{
  Node() = default;
  Node(std::string_view s, std::size_t startIdx = 0);

  friend std::ostream& operator<<(std::ostream& os, Node n)
    { os.write(n.data(), 3); return os; }
};

Node::Node(std::string_view s, std::size_t startIdx)
  : std::array<char, 3>{ s[startIdx], s[startIdx + 1], s[startIdx + 2] }
{
}

int main(int argc, char *argv[])
{
  int steps = 0;

  auto input = openInput(argc, argv);
  std::string directions;
  std::getline(input, directions);
  input.ignore(1, '\n');

  DEBUG(std::cout << directions << "\n\n");

  std::map<Node, std::pair<Node, Node>> nodes;
  for (auto line : InputByLine(input))
  {
    //                               "AAA = (BBB, CCC)"
    //                                ^      ^    ^
    //                                |      |    |
    constexpr int startIdx = 0; // ---`      |    |
    constexpr int leftIdx  = 7; // ----------`    |
    constexpr int rightIdx = 12;// ---------------`

    Node start(line, startIdx);
    Node left(line, leftIdx);
    Node right(line, rightIdx);

    nodes[start] = std::pair{left, right};
    DEBUG(std::cout << start << " = (" << left << ", " << right << ")\n");
  }

  Node       currNode("AAA");
  const Node endNode("ZZZ");
  while (currNode != endNode)
  {
    for (auto dir : directions)
    {
      if ('L' == dir)
        currNode = nodes[currNode].first;
      else
        currNode = nodes[currNode].second;
      ++steps;
      if (currNode == endNode)
        break;
    }
  }

  std::cout << "result = " << steps << " steps" << std::endl;
}
