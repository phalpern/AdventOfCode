// #define DEBUGPRINT

#include <aoc_util.h>
#include <unordered_map>
#include <algorithm>  // for std::min
#include <climits>

using namespace aoc;

int main(int argc, char *argv[])
{
  std::regex gameId_re("^Game ([0-9]+):");
  std::regex cubeCount_re("([0-9]+) (red|green|blue)[,;]?");

  int result = 0;

  auto input = openInput(argc, argv);
  for (auto line : InputByLine(input))
  {
    std::smatch m;

    ASSERT(std::regex_search(line, m, gameId_re));
    auto next  = m[0].second;
    int gameId = std::atoi(m[1].str().c_str());
    DEBUG(std::cout << "Game " << gameId << ": ");

    std::unordered_map<std::string, int> mincounts{
      { "red", 0 }, { "green", 0 }, { "blue", 0 }
    };

    while (std::regex_search(next, line.cend(), m, cubeCount_re))
    {
      next = m[0].second;
      int newcount = std::atoi(m[1].str().c_str());
      mincounts[m[2]] = std::max(mincounts[m[2]], newcount);

      DEBUG(std::cout << mincounts[m[2]] << ' ' << m[2].str() << ", ");
    }
    DEBUG(std::cout << std::endl);

    int power = 1;
    for (auto [color, mincount] : mincounts)
      power *= mincount;

    result += power;
  }

  std::cout << "result = " << result << std::endl;
}
