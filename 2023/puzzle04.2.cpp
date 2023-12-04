// -*- mode: c++; c-basic-offset: 2 -*-

#include <aoc_util.h>
#include <unordered_set>
#include <string_view>
#include <sstream>
#include <vector>

using namespace aoc;

std::unordered_set<int> parseNumbers(std::string_view s)
{
  DEBUG(std::cout << s << std::endl);
  std::istringstream is(std::string{s});

  std::unordered_set<int> ret;
  int count = 0;
  int v = 0;
  while (! (is >> v).fail())
  {
    DEBUG(std::cout << v << ' ');
    ++count;
    ret.insert(v);
  }
  DEBUG(std::cout << std::endl);


  ASSERT(ret.size() == count);
  return ret;
}

int main(int argc, char *argv[])
{
  int result = 0;

  std::vector<std::pair<int, int>> cards;

  auto input = openInput(argc, argv);
  for (std::string_view line : InputByLine(input))
  {
    auto start = line.find(':');
    ASSERT(start != std::string::npos);
    ++start;
    auto end = line.find('|', start);
    ASSERT(end != std::string::npos);
    auto cardNums = parseNumbers(line.substr(start, end - start));
    start = end + 1;
    auto myNums = parseNumbers(line.substr(start));

    int winningNums = 0;
    for (auto num : myNums)
      winningNums += cardNums.count(num);

    cards.push_back({winningNums, 1});
  }

  for (std::size_t i = 0; i < cards.size(); ++i)
  {
    auto [ score, count ] = cards[i];

    for (std::size_t j = i + 1; j <= i + score; ++j)
      cards[j].second += count;

    result += count;
  }

  std::cout << "result = " << result << std::endl;
}
