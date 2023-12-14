// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT 1
#include <aoc_util.h>
#include <utility>
#include <span>
#include <algorithm>

using namespace aoc;

// Break line up into a pattern string and vector of groups
std::pair<std::string, std::vector<int>> parseLine(std::string line)
{
  auto endPattern = line.find(' ');
  line[endPattern++] = '.';  // Terminate every pattern with a dot

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

  DEBUG_N(2, std::cout << "match(" <<
          pattern.substr(0, std::min(std::size_t(groupSize)+1,pattern.size()))
          << ", " << groupSize << ')');

  for (std::size_t i = 0; i < groupSize; ++i)
  {
    if (pattern[i] == '.')
    {
      DEBUG_N(2, std::cout << " FAILED\n");
      return false;  // Found a non '#' or '?'
    }
  }

  DEBUG_N(2, std::cout << (pattern[groupSize] != '#'
                           ? " SUCCEEDED" : " FAILED") << std::endl);
  return pattern[groupSize] != '#';
}

// Recursively count the number of solutions
int solve(std::string_view pattern, std::span<int> groups)
{
  DEBUG_N(2, printContainer(std::cout << "solve(" << pattern << ", ", groups)
          << ")\n");

  constexpr auto npos = std::string_view::npos;

  int result = 0;

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
        auto solutions = solve(pattern.substr(group + 1), groups.subspan(1));
        result += solutions;
      }
    }

    if ('#' == pattern[0]) return result;

    // Do the '.' action: skip the first character
    start = pattern.find_first_not_of('.', 1);
  }

  // Add 1 to results if end of pattern AND end of groups.  If end of pattern
  // but there are still groups left, no new solution exists at this branch of
  // the tail recursion.
  if (groups.empty())
    ++result;

  return result;
}

int main(int argc, char *argv[])
{
  int result = 0;

  auto input = openInput(argc, argv);
  for (auto line : InputByLine(input))
  {
    auto [ pattern, groups ] = parseLine(std::move(line));
    DEBUG(printContainer(std::cout << pattern << ' ', groups) << std::flush);
    auto solutions = solve(pattern, groups);
    DEBUG(std::cout << "-> " << solutions << std::endl);
    result += solutions;
  }

  std::cout << "result = " << result << std::endl;
}
