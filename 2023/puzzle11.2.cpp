// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT
#include <aoc_util.h>
#include <vector>
#include <set>
#include <string>
#include <algorithm>
#include <cstdlib>
#include <climits>

using namespace aoc;

struct Coord
{
  int64 row, col;

  friend
  std::strong_ordering operator<=>(const Coord&, const Coord&) = default;

  friend std::ostream& operator<<(std::ostream& os, const Coord& c)
    { return os << '(' << c.row << ", " << c.col << ')'; }

  friend Coord operator-(const Coord& a, const Coord& b)
    { return { a.row - b.row, a.col - b.col }; }

  friend int diff(const Coord& a, const Coord& b)
    { return std::abs(a.row - b.row) + std::abs(a.col - b.col); }
};

void expandSpace(std::vector<Coord>& galaxies,
                 std::vector<int64>  emptyRows,
                 std::set<int64>     emptyCols)
{
  constexpr int64 expansionVal = 1'000'000;

  // Sort galaxies by column
  std::sort(galaxies.begin(), galaxies.end(),
            [](Coord a, Coord b) { return a.col < b.col; });

  auto giter = galaxies.begin();
  int64 expansion = 0;
  emptyCols.insert(LONG_LONG_MAX);
  for (auto emptyCol : emptyCols)
  {
    // Apply expansion to any col preceding emptyCol.
    for ( ; giter != galaxies.end(); ++giter)
    {
      if (giter->col >= emptyCol)
        break;
      else
        giter->col += expansion;
    }
    expansion += expansionVal - 1; // Subsequent cols will expand more
  }

  // Sort galaxies by natural order, for which row is higher-order
  std::sort(galaxies.begin(), galaxies.end());
  giter = galaxies.begin();
  expansion = 0;
  emptyRows.push_back(LONG_LONG_MAX);
  for (auto emptyRow : emptyRows)
  {
    // Apply expansion to any row preceding emptyRow.
    for ( ; giter != galaxies.end(); ++giter)
    {
      if (giter->row >= emptyRow)
        break;
      else
        giter->row += expansion;
    }
    expansion += expansionVal - 1; // Subsequent rows will expand more
  }
}

int main(int argc, char *argv[])
{
  std::vector<Coord> galaxies;
  std::vector<int64> emptyRows;
  std::set<int64>    emptyCols;

  int64 rowIdx = 0;
  auto input = openInput(argc, argv);
  for (auto line : InputByLine(input))
  {
    if (emptyCols.empty())
      for (int64 i = 0; i < line.size(); ++i)
        emptyCols.insert(i);

    bool rowIsEmpty = true;
    for (int64 i = 0; i < line.size(); ++i)
    {
      if (line[i] != '.') {
        emptyCols.erase(i);
        galaxies.push_back({ rowIdx, i });
        rowIsEmpty     = false;
      }
    }

    if (rowIsEmpty)
      emptyRows.push_back(rowIdx);

    ++rowIdx;
  }

  DEBUG(printContainer(std::cout << "Galaxies: ", galaxies) << '\n');
  DEBUG(printContainer(std::cout << "Empty rows: ", emptyRows) << '\n');
  DEBUG(printContainer(std::cout << "Empty cols: ", emptyCols) << std::endl);

  expandSpace(galaxies, std::move(emptyRows), std::move(emptyCols));

  int64 result = 0;

  for (int i = 0; i < galaxies.size(); ++i)
  {
    for (int j = i + 1; j < galaxies.size(); ++j)
      result += diff(galaxies[j], galaxies[i]);
  }

  std::cout << "result = " << result << std::endl;
}
