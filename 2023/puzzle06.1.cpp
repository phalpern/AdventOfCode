// -*- mode: c++; c-basic-offset: 2 -*-

#include <aoc_util.h>
#include <algorithm>

using namespace aoc;

using int64 = long long;

int64 computeDistance(int64 buttonPress, int64 raceTime)
{
  return buttonPress * (raceTime - buttonPress);
}

int main(int argc, char *argv[])
{
  int result = 1;

  auto input = openInput(argc, argv);
  auto raceTimes       = parseNumbers<int64>(input, "Time:");
  auto recordDistances = parseNumbers<int64>(input, "Distance:");
  ASSERT(raceTimes.size() == recordDistances.size());

  for (std::size_t i = 0; i < raceTimes.size(); ++i)
  {
    auto raceTime       = raceTimes[i];
    auto recordDistance = recordDistances[i];

    // Note: This would be more efficient using a binary search:
    for (int64 buttonPress = 1; buttonPress <= raceTime / 2; ++buttonPress)
    {
      auto distance = computeDistance(buttonPress, raceTime);
      if (distance > recordDistance) {
        auto beatCount = raceTime - 1 - 2 * (buttonPress - 1);
        ASSERT(beatCount >= 0);
        result *= beatCount;
        break;
      }
    }
  }

  std::cout << "result = " << result << std::endl;
}
