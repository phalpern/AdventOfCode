// -*- mode: c++; c-basic-offset: 2 -*-

#include <aoc_util.h>
#include <algorithm>
#include <cctype>

using namespace aoc;

using int64 = long long;

int64 parseNumberWithSpaces(std::istream &is, std::string_view prefix)
{
  std::string inputStr;
  getline(is, inputStr);
  ASSERT(! is.fail());

  // Test and consume prefix
  ASSERT(inputStr.find(prefix) == 0);
  auto cursor = inputStr.cbegin() + prefix.length();

  int64 ret = 0;
  for (; cursor != inputStr.cend(); ++cursor)
  {
    const char digit = *cursor;
    if (std::isspace(digit)) continue;
    ASSERT(std::isdigit(digit));
    ret = 10 * ret + (digit - '0');
  }

  return ret;
}

inline
int64 computeDistance(int64 buttonPress, int64 raceTime)
{
  return buttonPress * (raceTime - buttonPress);
}

int main(int argc, char *argv[])
{
  auto input = openInput(argc, argv);
  auto raceTime = parseNumberWithSpaces(input, "Time:");
  auto recordDistance = parseNumberWithSpaces(input, "Distance:");

  int64 result = 0;

  // Note: This would be more efficient using a binary search or, better yet,
  // algebra, but this approach is plenty fast enough.
  for (int64 buttonPress = 1; buttonPress <= raceTime / 2; ++buttonPress)
  {
    auto distance = computeDistance(buttonPress, raceTime);
    if (distance > recordDistance) {
      auto beatCount = raceTime - 1 - 2 * (buttonPress - 1);
      ASSERT(beatCount >= 0);
      result = beatCount;
      break;
    }
  }

  std::cout << "result = " << result << std::endl;
}
