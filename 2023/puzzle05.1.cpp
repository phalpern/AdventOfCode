// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT
#include <aoc_util.h>
#include <map>
#include <vector>
#include <sstream>
#include <climits>

using int64 = long long;

using namespace aoc;

std::vector<int64> parseNumbers(std::string_view s)
{
  std::istringstream is(std::string{s});

  std::vector<int64> ret;
  int64 v = 0;
  while (! (is >> v).fail())
  {
    DEBUG(std::cout << v << ' ');
    ret.push_back(v);
  }
  DEBUG(std::cout << std::endl);

  return ret;
}

struct TranslationEntry {
  int64 offset;
  int64 rangeLen;
};

struct TranslationMap {
  const char*                       mapName;
  std::map<int64, TranslationEntry> entries;

  int64 translate(int64 v) const;
};

int64 TranslationMap::translate(int64 v) const
{
  // Get entry *after* the one that might contain v.
  auto entryIter = entries.upper_bound(v);
  if (entryIter == entries.begin())
    return v;  // No entries might contain v.  Return v unchanged.

  const auto& [ source, entry ] = *--entryIter;
  if (source + entry.rangeLen <= v)
    return v;  // Range does not contain v.  Return v unchanged.

  return v + entry.offset;
}

TranslationMap almanac[] = {
  { "seed-to-soil" },
  { "soil-to-fertilizer" },
  { "fertilizer-to-water" },
  { "water-to-light" },
  { "light-to-temperature" },
  { "temperature-to-humidity" },
  { "humidity-to-location" }
};

int main(int argc, char *argv[])
{
  int64 result = LONG_LONG_MAX;

  auto input = openInput(argc, argv);
  std::string str;
  input >> str;
  ASSERT(str == "seeds:");
  getline(input, str);
  auto seeds = parseNumbers(str);

  getline(input, str);
  ASSERT(str.empty());

  for (auto& currMap : almanac)
  {
    input >> str;  // map name
    DEBUG(std::cout << "map name = " << str << std::endl);
    ASSERT(currMap.mapName == str);
    getline(input, str);  // Ignore " map:"

    while (! getline(input, str).fail() && ! str.empty())
    {
      auto nums = parseNumbers(str);
      ASSERT(nums.size() == 3);
      int64 dest   = nums[0];
      int64 src    = nums[1];
      int64 len    = nums[2];
      int64 offset = dest - src;
      currMap.entries[src] = TranslationEntry{offset, len};
    }
  }

  for (auto seed : seeds)
  {
    DEBUG(std::cout << "seed = " << seed << std::endl);

    auto xval = seed;
    for (const auto& xmap : almanac)
    {
      xval = xmap.translate(xval);
      DEBUG(std::cout << xmap.mapName << " -> " << xval << std::endl);
    }

    result = std::min(result, xval);
  }

  std::cout << "result = " << result << std::endl;
}
