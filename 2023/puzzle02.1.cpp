// #define DEBUGPRINT

#include <aoc_util.h>
#include <unordered_map>

using namespace aoc;

int main(int argc, char *argv[])
{
  std::regex gameId_re("^Game ([0-9]+):");
  std::regex cubeCount_re("([0-9]+) (red|green|blue)([,;])");

    int result = 0;

  auto input = openInput(argc, argv);
  for (auto line : InputByLine(input))
  {
    line += ";";  // Force termination of line
    std::smatch m;

    ASSERT(std::regex_search(line, m, gameId_re));
    auto next  = m[0].second;
    int gameId = std::atoi(m[1].str().c_str());
    result += gameId;  // Tentative
    DEBUG(std::cout << "Game " << gameId << ": ");

    std::unordered_map<std::string, int> counts{
      { "red", 0 }, { "green", 0 }, { "blue", 0 }
    };

    while (std::regex_search(next, line.cend(), m, cubeCount_re))
    {
      next = m[0].second;
      counts[m[2]] = std::atoi(m[1].str().c_str());
      DEBUG(std::cout << counts[m[2]] << ' ' << m[2].str() << m[3] << ' ');
      if (m[3] == ';')
      {
        if (counts["red"] > 12 || counts["green"] > 13 || counts["blue"] > 14)
        {
          result -= gameId;  // Remove this game from the total
          break;
        }
        counts["red"] = counts["green"] = counts["blue"] = 0;
      }
    }
    DEBUG(std::cout << std::endl);
  }

  std::cout << "result = " << result << std::endl;
}
