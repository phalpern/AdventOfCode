// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT
#include <aoc_util.h>
#include <map>
#include <vector>
#include <sstream>
#include <iterator>
#include <climits>

using int64 = long long;

using namespace aoc;

struct Range {
  int64 begin;
  int64 len;

  bool empty() const { return 0 == len; }

  friend int operator<=>(const Range&, const Range&) = default;

  friend std::ostream& operator<<(std::ostream& os, const Range& r)
    { return os << "{ " << r.begin << ", " << r.len << " }"; }
};

struct TranslationMap {
  const char*            name;
  std::map<int64, Range> entries;

  // Return the destination range corresponding to the first part of the first
  // part of `srcRange`, and modify `srcRange` to no longer include the part
  // mapped to the returned destination.
  Range lookupDestRange(Range& srcRange) const;
};

Range TranslationMap::lookupDestRange(Range& srcRange) const
{
  auto probe     = srcRange.begin;
  auto resultLen = srcRange.len;

  // Get entry *after* the one that might contain v.
  auto entryIter = entries.upper_bound(probe);
  if (entryIter != entries.end())
    resultLen = std::min(resultLen, entryIter->first - probe);

  if (entryIter != entries.begin())
  {
    const auto& [ source, entry ] = *--entryIter;
    int64 entryOffset = probe - source;
    if (entry.len > entryOffset)
    {
      resultLen = std::min(resultLen, entry.len - entryOffset);
      srcRange = { probe + resultLen, srcRange.len - resultLen };
      return { entry.begin + entryOffset, resultLen };
    }
  }

  srcRange = { probe + resultLen, srcRange.len - resultLen };
  return { probe, resultLen };
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

constexpr const TranslationMap* almanacEnd = std::end(almanac);

int64 applyTranslationMap(const TranslationMap* xmap, Range srcRange)
{
  if (xmap == almanacEnd)
    return srcRange.begin;

  int64 result = LONG_LONG_MAX;

  while (! srcRange.empty())
  {
    DEBUG(std::cout << srcRange << " -> ");
    auto destRange = xmap->lookupDestRange(srcRange);
    DEBUG(std::cout << xmap->name << " -> " << destRange << std::endl);

    result = std::min(result, applyTranslationMap(xmap + 1, destRange));
  }

  return result;
}

int main(int argc, char *argv[])
{
  int64 result = LONG_LONG_MAX;

  auto input = openInput(argc, argv);
  std::string str;
  getline(input, str);
  auto rawSeeds = parseNumbers<int64>(str, "seeds:");

  std::vector<Range> seedRanges;
  for (std::size_t i = 0; i < rawSeeds.size(); i += 2)
    seedRanges.push_back({rawSeeds[i], rawSeeds[i + 1]});

  getline(input, str);
  ASSERT(str.empty());

  for (auto& currMap : almanac)
  {
    input >> str;  // map name
    DEBUG(std::cout << "map name = " << str << std::endl);
    ASSERT(currMap.name == str);
    getline(input, str);  // Ignore " map:"

    while (! getline(input, str).fail() && ! str.empty())
    {
      auto nums = parseNumbers<int64>(str);
      ASSERT(nums.size() == 3);
      int64 dest   = nums[0];
      int64 src    = nums[1];
      int64 len    = nums[2];
      currMap.entries[src] = { dest, len };
    }
  }

  for (auto seedRange : seedRanges)
  {
    DEBUG(std::cout << "seedRange = { " << seedRange << std::endl);

    result = std::min(result, applyTranslationMap(almanac, seedRange));
  }

  std::cout << "result = " << result << std::endl;
}
