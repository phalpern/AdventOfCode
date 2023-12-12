// -*- mode: c++; c-basic-offset: 2 -*-

#define DEBUGPRINT
#include <aoc_util.h>
#include <vector>
#include <string_view>

using namespace aoc;

// Directions as a bit map
enum Direction : signed char
{
  NO_DIR = -2, START_DIR, NORTH, EAST, SOUTH, WEST
};

struct Coord
{
  // Coordinate of a tile or delta change in a coordinate
  int row, col;

  friend constexpr Coord operator+(Coord a, Coord b)
     { return { a.row + b.row, a.col + b.col }; }

  friend bool operator==(const Coord&, const Coord&) = default;

  friend std::ostream& operator<<(std::ostream& os, const Coord& c)
    { return os << '(' << c.row << ", " << c.col << ')'; }
};

constexpr Coord errorCoord{ -2, -2 };

// Coordinate deltas for in each direction of motion
constexpr Coord deltas[] = {
  { -1,  0 },  // NORTH
  {  0,  1 },  // EAST
  {  1,  0 },  // SOUTH
  {  0, -1 }   // WEST
};

class Tile
{
public:
  // `edge1` and `edge2` are the edges of the tile connected by a pipe.
  // If `edge1` is 'NO_DIR', then there is no pipe in this tile
  // If `edge1` is `START_DIR`, then the pipe attributes are not known.
  Direction edge1;
  Direction edge2;

  // Create an empty tile
  constexpr Tile() : edge1(NO_DIR), edge2(NO_DIR) { }

  // Create a tile from one of '|', '-', 'L', 'J', '7', 'F', '.' or 'S'.
  explicit Tile(char symbol);

  void set(Direction e1, Direction e2) { edge1 = e1; edge2 = e2; }

  bool isEmpty() const { return NO_DIR == edge1; }
  bool isStart() const { return START_DIR == edge1; }
};

Tile::Tile(char symbol)
{
  switch (symbol)
  {
   case '|': set(NORTH, SOUTH);         break;
   case '-': set(EAST,  WEST );         break;
   case 'L': set(NORTH, EAST );         break;
   case 'J': set(NORTH, WEST );         break;
   case '7': set(SOUTH, WEST );         break;
   case 'F': set(EAST,  SOUTH);         break;
   case '.': set(NO_DIR, NO_DIR);       break;
   case 'S': set(START_DIR, START_DIR); break;
   default: ASSERT(false);
  }
}

class MazeGrid
{
  int               m_numCols;
  std::vector<Tile> m_tiles;
  Coord             m_startCoord;

public:
  MazeGrid() : m_numCols(0) { }

  void addRow(std::string_view rowStr);

  int nRows() const { return m_tiles.size() / m_numCols; }
  int nCols() const { return m_numCols; }
  Coord startCoord() const { return m_startCoord; }

  // Return the tile at the specified coordinate.
  Tile& operator[](Coord rowCol)
  {
    ASSERT(0 <= rowCol.row && rowCol.row < nRows());
    ASSERT(0 <= rowCol.col && rowCol.col < nCols());

    return m_tiles[rowCol.row * m_numCols + rowCol.col];
  }

  // Return the tile at the specified coordinate.  For const maze access,
  // return an empty tile if indexing exactly one row or column outside the
  // grid boundaries.
  const Tile& operator[](Coord rowCol) const
  {
    // Return this if we index outside the grid.
    static const Tile emptyTile{};

    // Allow one row and/or column beyond the boundaries of the grid.
    ASSERT(-1 <= rowCol.row && rowCol.row <= nRows());
    ASSERT(-1 <= rowCol.col && rowCol.col <= nCols());

    if (-1 == rowCol.row || rowCol.row == nRows() ||
        -1 == rowCol.col || rowCol.col == nCols())
      return emptyTile;  // Outside the grid
    else
      return m_tiles[rowCol.row * m_numCols + rowCol.col];
  }

  // Coming from `fromCoord`, compute where you end up going through the pipe
  // at 'pipeCoord'.  If 'pipeCoord' does not have a pipe end pointing to
  // 'fromCoord', return { -1, -1 }.
  Coord pipe(Coord fromCoord, Coord pipeCoord) const;

  // Return true if `pipe(fromCoord, pipeCoord)` is valid.
  bool canPipe(Coord fromCoord, Coord pipeCoord) const;
};

void MazeGrid::addRow(std::string_view rowStr)
{
  if (0 == m_numCols)
    m_numCols = rowStr.size();
  else
    ASSERT(m_numCols == rowStr.size());

  for (auto c : rowStr)
    m_tiles.push_back(Tile{c});

  auto startCol = rowStr.find('S');
  if (startCol != std::string_view::npos)
    m_startCoord = { nRows() - 1, int(startCol) };
}

bool MazeGrid::canPipe(Coord fromCoord, Coord pipeCoord) const
{
  return pipe(fromCoord, pipeCoord) != errorCoord;
}

Coord MazeGrid::pipe(Coord fromCoord, Coord pipeCoord) const
{
  const Tile& pipeTile = (*this)[pipeCoord];
  if (pipeTile.isEmpty() || pipeTile.isStart())
    return errorCoord;

  auto joint1 = pipeCoord + deltas[pipeTile.edge1];
  auto joint2 = pipeCoord + deltas[pipeTile.edge2];

  if (joint1 == fromCoord)
    return joint2;
  else if (joint2 == fromCoord)
    return joint1;
  else
    return errorCoord;
}

int main(int argc, char *argv[])
{
  int steps = 0;

  MazeGrid maze;

  auto input = openInput(argc, argv);
  for (auto line : InputByLine(input))
    maze.addRow(line);

  const auto startCoord = maze.startCoord();

  DEBUG(std::cout << "rows = " << maze.nRows()
        << ", columns = " << maze.nCols()
        << ", startCoord = " << startCoord << std::endl);

  Coord pipeCoord;
  for (auto delta : deltas)
  {
    pipeCoord = startCoord + delta;
    if (maze.canPipe(startCoord, pipeCoord))
      break;
  }

  int loopLen = 1;  // Include startCoord
  Coord prevCoord = startCoord;
  while (pipeCoord != startCoord)
  {
    auto nextCoord = maze.pipe(prevCoord, pipeCoord);
    ++loopLen;
    prevCoord = pipeCoord;
    pipeCoord = nextCoord;
  }

  auto result = (loopLen + 1) / 2;
  std::cout << "result = " << result << std::endl;
}
