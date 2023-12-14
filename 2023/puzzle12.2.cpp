// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT 1
#include <aoc_util.h>
#include <utility>
#include <span>
#include <algorithm>
#include <map>
#include <tuple>

using namespace aoc;

// Break line up into a pattern string and vector of groups
std::pair<std::string, std::vector<int>> parseLine(std::string line)
{
  auto endPattern = line.find(' ');

  for (auto comma = line.find(',', endPattern); comma != std::string::npos;
       comma = line.find(',', comma + 1))
    line[comma] = ' ';

  auto groups = parseNumbers(std::string_view(line).substr(endPattern));
  line.resize(endPattern);

  return { std::move(line), std::move(groups) };
}

// Return whether first group in pattern can be groupSize long
bool match(std::string_view pattern, int groupSize)
{
  // A matching group contains groupSize '#' or '?' characters and ends with a
  // '. or '?' character.  Note that pattern always ends with a '.', so a match
  // will aways succeed or fail before running out of string.

  DEBUG2(std::cout << "match(" <<
         pattern.substr(0, std::min(std::size_t(groupSize)+1,pattern.size()))
         << ", " << groupSize << ')');

  for (std::size_t i = 0; i < groupSize; ++i)
  {
    if (pattern[i] == '.')
    {
      DEBUG2(std::cout << " FAILED\n");
      return false;  // Found a non '#' or '?'
    }
  }

  DEBUG2(std::cout << (pattern[groupSize] != '#'
                       ? " SUCCEEDED" : " FAILED") << std::endl);
  return pattern[groupSize] != '#';
}

// Represent a key to the memo map
struct MemoKey
{
  std::string_view     pattern;
  std::span<const int> groups;

  friend std::strong_ordering operator<=>(const MemoKey& a, const MemoKey& b)
  {
    return (std::tuple{a.pattern.data(), a.pattern.size(),
                       a.groups.data(), a.groups.size()} <=>
            std::tuple{b.pattern.data(), b.pattern.size(),
                       b.groups.data(), b.groups.size()});
  }

};

using MemoType = std::map<MemoKey, int64>;

// Recursively count the number of solutions
int64 solve(std::string_view pattern, std::span<const int> groups,
            MemoType& memos)
{
  DEBUG2(printContainer(std::cout << "solve(" << pattern << ", ", groups)
         << ")\n");

  constexpr auto npos = std::string_view::npos;

  auto memoIter = memos.find({ pattern, groups });
  if (memoIter != memos.end())
  {
    DEBUG3(printContainer(std::cout << "memo hit: " << pattern << ' ', groups)
           << std::endl);
    return memoIter->second;
  }

  int64 result = 0;

  auto originalPattern = pattern;
  auto start = pattern.find_first_not_of('.');
  while (npos != start)
  {
    pattern.remove_prefix(start);

    // Next character is either '#' or '?'.  If '#', match the next group and
    // recursively match remaining groups, returning the result.  If '?', do
    // the same as '#' (as if the '?' were a '#', but instead of returning the
    // result, continue searching for the first group, skipping the current
    // character (as if the '?'  were a '.')

    // Do the '#' action.  If there are no more groups to match, then no
    // solutions can be added to the result.
    if (! groups.empty())
    {
      auto group = groups.front();
      if (match(pattern, group))
      {
        // Matched the first group, now recursively match the remaining groups,
        // accumulating the results
        auto solutions = solve(pattern.substr(group + 1), groups.subspan(1),
                               memos);
        result += solutions;
      }
    }

    if ('#' == pattern[0])
    {
      memos[{ originalPattern, groups }] = result;
      return result;
    }

    // Do the '.' action: skip the first character
    start = pattern.find_first_not_of('.', 1);
  }

  // Add 1 to results if end of pattern AND end of groups.  If end of pattern
  // but there are still groups left, no new solution exists at this branch of
  // the tail recursion.
  if (groups.empty())
    ++result;

  memos[{ originalPattern, groups }] = result;
  return result;
}

int main(int argc, char *argv[])
{
  int64 result = 0;

  auto input = openInput(argc, argv);
  int lineCount = 0;
  for (auto line : InputByLine(input))
  {
    ++lineCount;

    auto [ pattern, groups ] = parseLine(std::move(line));
    DEBUG(printContainer(std::cout << pattern << ' ', groups) << std::flush);

    // Make 5 copies of the pattern and groups
    auto patternCopy = pattern;
    auto groupsCopy = groups;
    pattern.reserve(5 * pattern.size() + 5);
    groups.reserve(5 * groups.size());
    for (int i = 0; i < 4; ++i)
    {
      pattern += '?';  // Separate pattern repititions with '?'
      pattern += patternCopy;
      groups.insert(groups.end(), groupsCopy.begin(), groupsCopy.end());
    }
    // Always end with a '.', to avoid end-of-string special cases
    pattern += '.';
    MemoType memos;
    auto solutions = solve(pattern, groups, memos);
    DEBUG(std::cout << "-> " << solutions << std::endl);
    result += solutions;

    if (lineCount % 10 == 0)
      DEBUG_N(0, std::cout << "Processed " << lineCount << " patterns" << '\r'
              << std::flush);
  }

  DEBUG_N(0, std::cout << "Processed " << lineCount << " patterns"
          << std::endl);

  std::cout << "\nresult = " << result << std::endl;
}
