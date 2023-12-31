// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT 1
#include <aoc_util.h>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <utility>

using namespace aoc;

enum Direction { RIGHT, DOWN, LEFT, UP };

std::ostream& operator<<(std::ostream& os, Direction d)
{
  constexpr const char* names[] = { "RIGHT", "DOWN ", "LEFT ", "UP   " };
  return os << names[d];
}

// Edge types:
//
//           |                         |  |                 |          |
//  VERTICAL |    U_HORIZONTAL +==+ or +==+    Z_HORIZONTAL +==+ or +==+
//           |                 |  |                            |    |
//
enum EdgeType { VERTICAL, U_HORIZONTAL, Z_HORIZONTAL, UNKNOWN_HORIZONTAL };

std::ostream& operator<<(std::ostream& os, EdgeType et)
{
  constexpr const char* names[] = {
    "VERTICAL    ", "U_HORIZONTAL", "Z_HORIZONTAL", "UNKNOWN_HORIZONTAL"
  };
  return os << names[et];
}

struct Edge
{
  // Edge descriptor excludes both endpoints for vertical edge type and
  // includes both end points for horizontal edge types.
  // Note, these members are public to enable aggregate initialization.
  int64     m_startRow;
  int64     m_startCol;
  EdgeType  m_edgeType;
  int64     m_meters;

public:
  auto startRow() const { return m_startRow; }
  auto startCol() const { return m_startCol; }

  auto endRow() const
    { return m_startRow + (m_edgeType == VERTICAL ? m_meters : 1); }

  auto endCol() const
    { return m_startCol + (m_edgeType == VERTICAL ? 1 : m_meters); }

  auto edgeType() const { return m_edgeType; }

  auto meters() const { return m_meters; }

  void setEdgeType(EdgeType et) { m_edgeType = et; }

  friend std::strong_ordering operator<=>(const Edge&, const Edge&) = default;

  friend std::ostream& operator<<(std::ostream& os, const Edge& e)
  {
    return os << "{ (" << e.startRow() << ", " << e.m_startCol << "), "
              << e.m_edgeType << ", " << e.m_meters << " }";
  }
};

void doInstruction(int64& row, int64& col, Direction dir, int64 meters)
{
  switch (dir)
  {
   case LEFT:  col -= meters; break;
   case RIGHT: col += meters; break;
   case UP:    row -= meters; break;
   case DOWN:  row += meters; break;
  }
}

int main(int argc, char *argv[])
{
  auto input = openInput(argc, argv);

  std::vector<Edge>  trench;
  int64 row = 0, col = 0;

  for (auto line : InputByLine(input))
  {
    auto startRow = row;
    auto startCol = col;
    auto hashMark = line.find('#');
    auto rawNum   = std::strtoul(line.data() + hashMark + 1, nullptr, 16);
    auto dir      = Direction(rawNum & 0x00000f);
    int64 meters  = rawNum >> 4;

    doInstruction(row, col, dir, meters);  // Modifies row & col

    // This switch statement modifies meters
    EdgeType edgeType;
    switch (dir)
    {
     case LEFT:  edgeType = UNKNOWN_HORIZONTAL; startCol -= meters++; break;
     case RIGHT: edgeType = UNKNOWN_HORIZONTAL;             meters++; break;
     case UP:    edgeType = VERTICAL; startRow -= --meters; break;
     case DOWN:  edgeType = VERTICAL; startRow++; --meters; break;
    }

    trench.push_back({ startRow, startCol, edgeType, meters });
  }

  ASSERT(row == 0 && col == 0);
  DEBUG(std::cout << "num edges = " << trench.size() << '\n');

  // Break graph into horizontal bands at each horizontal transition.
  // The `horizontalBands` vector contains the starting and ending rows of each
  // horizontal band.
  std::vector<int64> horizontalBands;
  for (int i = 0; i < trench.size(); ++i)
  {
    Edge& e = trench[i];
    if (UNKNOWN_HORIZONTAL == e.edgeType())
    {
      const Edge& prev = trench[(i + trench.size() - 1) % trench.size()];
      const Edge& next = trench[(i + 1) % trench.size()];
      e.setEdgeType((prev.startRow() == next.startRow() ||
                     prev.endRow() == next.endRow()) ?
                    U_HORIZONTAL : Z_HORIZONTAL);
    }

    horizontalBands.push_back(e.startRow());
    horizontalBands.push_back(e.endRow());
  }

  // Sort edges by startCol()
  DEBUG2(printContainer(std::cout, trench, "\n"));
  std::ranges::sort(trench, [](const Edge& a, const Edge& b) -> bool
                            { return a.startCol() < b.startCol(); });
  DEBUG3(printContainer(std::cout << "*** Sorted:\n", trench, "\n"));

  // Sort and remove duplicate horizontal bands
  std::ranges::sort(horizontalBands);
  auto eraseIter = std::unique(horizontalBands.begin(), horizontalBands.end());
  horizontalBands.erase(eraseIter, horizontalBands.end());
  DEBUG(std::cout << horizontalBands.size() << " horizontal bands\n");

  int64 result = 0;

  // A band is defined as the interval from the start of a band up to but not
  // including the start of the next band.  Traverse the bands and compute the
  // filled areas added by each band.
  for (int i = 0; i < horizontalBands.size() - 1; ++i)
  {
    auto bandStart  = horizontalBands[i];
    auto bandEnd    = horizontalBands[i + 1];
    auto bandHeight = bandEnd - bandStart;

    bool fill = false;
    auto fillStartCol = 0;
    int64 fillArea = 0;

    for (const auto& e : trench)
    {
      if (e.endRow() <= bandStart || bandEnd <= e.startRow())
        continue;  // edge does not overlap band

      fillArea = 0;

      switch (e.edgeType())
      {
       case Z_HORIZONTAL:
        ASSERT(1 == bandHeight);
        [[fallthrough]];
       case VERTICAL:
        if (! fill)
        {
          fillStartCol = e.startCol();
          fill = true;
        }
        else
        {
          fillArea = bandHeight * (e.endCol() - fillStartCol);
          fill = false;
        }
        break;
       case U_HORIZONTAL:
        if (! fill)
          fillArea = e.meters();
        // No change to fill flag.  If fill flag is true, segment is
        // automatically part of the computed area.
        break;
       case UNKNOWN_HORIZONTAL:
        ASSERT(! "Unreachable");
      }

      DEBUG(if (fill || fillArea)
              std::cout << "band = (" << bandStart << ", " << bandEnd <<
                "], edge = " << e << ", fillArea = " << fillArea << '\n');

      result += fillArea;
    }

    ASSERT(! fill);
  }

  std::cout << "\nresult = " << result << "\n\n";
}
