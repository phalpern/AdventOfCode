// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT
#include <aoc_util.h>
#include <array>
#include <map>
#include <utility>
#include <string_view>
#include <algorithm>

using namespace aoc;

using uint64 = unsigned long long;

struct Node : std::array<char, 3>
{
  constexpr Node();
  Node(std::string_view s, std::size_t startIdx = 0);

  friend std::ostream& operator<<(std::ostream& os, Node n)
    { os.write(n.data(), 3); return os; }
};

constexpr Node::Node()
  : std::array<char, 3>{ '_', '_', '_' }
{
}

constexpr Node NullNode{};

Node::Node(std::string_view s, std::size_t startIdx)
  : std::array<char, 3>{ s[startIdx], s[startIdx + 1], s[startIdx + 2] }
{
}

// Record a traveler's current node, index of next direction in direction list,
// and steps taken so far.
struct Traveler
{
  Node    currNode;
  int     nextDirIdx;
  uint64  steps;
};

// Record an end point as a node and steps needed to get there
struct EndPoint
{
  Node   endNode;
  uint64 steps;
};

// Navigate to the next node ending in 'Z'.  Count number of steps and memoize
// the start and end points.
Traveler advanceToNextZ(std::map<Node, std::pair<Node, Node>>& nodes,
                        std::string_view directions, const Traveler& trav)
{
  // Map a start node and start direction index to an end node and number of
  // steps to get there from the start node.  Used to memoize partial paths.
  static std::map<std::pair<Node, int>, EndPoint> memos;

  constexpr auto memprogIncr = 1ULL;
  static auto memprog = memprogIncr;

  auto [ iter, isNew ] = memos.insert({{ trav.currNode, trav.nextDirIdx },
                                       { }});
  auto& end = iter->second;
  if (! isNew)
  {
    // We've mapped this path before!
    DEBUG(static uint64 hits = 0;
          ++hits;
          std::cout << "Hits = " << hits << "\n");

    int    dirIdx = (trav.nextDirIdx + end.steps) % directions.length();
    uint64 steps  = trav.steps + end.steps;
    return { end.endNode, dirIdx, steps };
  }

  if (memos.size() >= memprog) {
    std::cout << memos.size() << " memos\n";
    memprog += memprogIncr;
  }

  // Follow the directions from `trav`
  auto [ currNode, dirIdx, startSteps ] = trav;
  uint64 segmentSteps = 0;
  do
  {
    if ('L' == directions[dirIdx])
      currNode = nodes[currNode].first;
    else
      currNode = nodes[currNode].second;
    ++segmentSteps;
    dirIdx = (dirIdx + 1) % directions.length();
  } while (currNode[2] != 'Z');

  // Memoize this path; `end` already refers to the entry in the memos array
  // corresonding to the start.
  end = { currNode, segmentSteps };

  return { currNode, dirIdx, startSteps + segmentSteps };
}

int main(int argc, char *argv[])
{
  auto input = openInput(argc, argv);
  std::string directions;
  std::getline(input, directions);
  input.ignore(1, '\n');

  DEBUG(std::cout << directions << "\n\n");

  constexpr uint64 progIncr = 1'000'000'000'000ULL;
  uint64 progress = progIncr;

  std::map<Node, std::pair<Node, Node>> nodes;
  for (auto line : InputByLine(input))
  {
    //                                "AAA = (BBB, CCC)"
    //                                 ^      ^    ^
    //                                 |      |    |
    constexpr int startIdx = 0;  // ---`      |    |
    constexpr int leftIdx  = 7;  // ----------`    |
    constexpr int rightIdx = 12; // ---------------`

    Node start(line, startIdx);
    Node left(line, leftIdx);
    Node right(line, rightIdx);

    nodes[start] = std::pair{left, right};
    DEBUG(std::cout << start << " = (" << left << ", " << right << ")\n");
  }

  std::vector<Traveler> travelers;
  for (auto& [ key, value ] : nodes)
    if ('A' == key[2])
      travelers.push_back({ key, 0, 0 });

  std::cout << directions.size() << " instructions\n";
  std::cout << nodes.size() << " total nodes\n";
  std::cout << travelers.size() << " travelers\n";

  bool done = false;
  Traveler* firstTraveler = &travelers[0];
  for (;;)
  {
    // Advance traveler having fewest steps.
    *firstTraveler = advanceToNextZ(nodes, directions, *firstTraveler);

    // Find new traveler having fewest steps.
    uint64 minSteps = firstTraveler->steps;
    uint64 maxSteps = minSteps;
    for (auto& trav : travelers)
    {
      maxSteps = std::max(maxSteps, trav.steps);
      if (trav.steps < minSteps)
      {
        minSteps = trav.steps;
        firstTraveler = &trav;
      }
    }

    if (minSteps >= progress) {
      std::cout << "progress = " << minSteps << " steps\n";
      progress += progIncr;
    }

    if (minSteps == maxSteps)
      break;  // Success! All travelers have same step count
  }

  auto result = travelers[0].steps;
  std::cout << "result = " << result << " steps" << std::endl;
}
