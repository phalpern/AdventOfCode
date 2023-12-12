// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT
#include <aoc_util.h>
#include <vector>
#include <string_view>

using namespace aoc;

// Directions as a bit map
enum Direction : signed char
{
  NO_DIR = -2, START_DIR, NORTH, SOUTH, EAST, WEST
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
  {  1,  0 },  // SOUTH
  {  0,  1 },  // EAST
  {  0, -1 }   // WEST
};

class Tile
{
  struct TileAttributes
  {
    char      symbol;
    Direction edge1;
    Direction edge2;
  };

  static constexpr TileAttributes attributes[8] = {
    { '.', NO_DIR,    NO_DIR    },
    { 'S', START_DIR, START_DIR },
    { '|', NORTH,     SOUTH     },
    { 'L', NORTH,     EAST      },
    { 'J', NORTH,     WEST      },
    { '7', SOUTH,     WEST      },
    { 'F', SOUTH,     EAST      },
    { '-', EAST,      WEST      }
  };
  static constexpr unsigned char  emptyIdx = 0;  // Index of empty tile attr
  static constexpr unsigned char  startIdx = 1;  // Index of start tile attr

  unsigned char m_attrIdx;  // Index of tile attributes in attributes table

public:
  // Create an empty tile
  constexpr Tile() : m_attrIdx(emptyIdx) { }

  // Create a tile from one of '|', '-', 'L', 'J', '7', 'F', '.' or 'S'.
  explicit Tile(char symbol);

  char symbol()  const { return attributes[m_attrIdx].symbol; }
  bool isEmpty() const { return emptyIdx == m_attrIdx; }
  bool isStart() const { return startIdx == m_attrIdx; }

  // `edge1` and `edge2` are the edges of the tile connected by a pipe.
  // Invaraint: edge1() <= edge2().  Correllary: on elbow pipes, the vertical
  // direction is always edge1(), if either direction is NORTH then it must
  // edge1(), and if either direction is WEST then it must be edge2().
  constexpr Direction edge1() const { return attributes[m_attrIdx].edge1; }
  constexpr Direction edge2() const { return attributes[m_attrIdx].edge2; }

  friend bool operator==(const Tile&, const Tile&) = default;
};

Tile::Tile(char symbol)
{
  static constexpr auto numAttr = sizeof(attributes) / sizeof(attributes[0]);
  for (m_attrIdx = 0; m_attrIdx < numAttr; ++m_attrIdx)
    if (symbol == attributes[m_attrIdx].symbol)
      return;

  ASSERT(false && "Invalid symbol");
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

  auto joint1 = pipeCoord + deltas[pipeTile.edge1()];
  auto joint2 = pipeCoord + deltas[pipeTile.edge2()];

  if (joint1 == fromCoord)
    return joint2;
  else if (joint2 == fromCoord)
    return joint1;
  else
    return errorCoord;
}

// Two-D array of bool.
class BoolGrid
{
  // Use `vector<Boolish>` to avoid `vector<bool>` nonsense
  class Boolish {
    bool m_value;
  public:
    constexpr Boolish(bool v) : m_value(v) { }
    bool& operator=(bool v) { m_value = v; return m_value; }
    operator bool&() { return m_value; }
    operator const bool&() const { return m_value; }
  };

  int                  m_numCols;
  std::vector<Boolish> m_tiles;

public:
  BoolGrid(int rows, int cols) : m_numCols(cols), m_tiles(rows * cols, false)
    { }

  bool& operator[](Coord rowCol)
    { return m_tiles[rowCol.row * m_numCols + rowCol.col]; }
  const bool& operator[](Coord rowCol) const
    { return m_tiles[rowCol.row * m_numCols + rowCol.col]; }
};

int main(int argc, char *argv[])
{
  MazeGrid maze;

  auto input = openInput(argc, argv);
  for (auto line : InputByLine(input))
    maze.addRow(line);

  const auto startCoord = maze.startCoord();

  DEBUG(std::cout << "rows = " << maze.nRows()
        << ", columns = " << maze.nCols()
        << ", startCoord = " << startCoord << std::endl);

  // Map the loop, putting `true` whereever a pipe in the loop is detected
  BoolGrid loopMap(maze.nRows(), maze.nCols());

  // Compute pipe type for start tile
  Tile& startTile = maze[startCoord];
  for (char symbol : "L|JF-7")
  {
    Tile testTile(symbol);
    if (maze.canPipe(startCoord, startCoord + deltas[testTile.edge1()]) &&
        maze.canPipe(startCoord, startCoord + deltas[testTile.edge2()]))
    {
      startTile = testTile;
      break;
    }
  }

  loopMap[startCoord] = true;
  int loopLen = 1;  // Include startCoord
  Coord prevCoord = startCoord;
  Coord pipeCoord = startCoord + deltas[startTile.edge1()];
  while (pipeCoord != startCoord)
  {
    loopMap[pipeCoord] = true;
    auto nextCoord = maze.pipe(prevCoord, pipeCoord);
    ++loopLen;
    prevCoord = pipeCoord;
    pipeCoord = nextCoord;
  }

  // Now, scan loopMap and maze simultaneously.  When a vertical loop element
  // is found, toggle from outside to enclosed or vice-versa.  An elbow
  // followed by zero or more horizontal elements followed by another elbow
  // counts toggles the sentinel if the vertical edges of the elbows are
  // opposite and does not toggle it if they are the same, i.e, "F-J" toggles
  // the sentinel wheras "L-J" does not.
  int enclosed = 0, outside = 0;
  const Tile verticalTile('|');
  for (int row = 0; row < maze.nRows(); ++row)
  {
    Direction startVertical = NO_DIR;
    bool isEnclosed = false;
    std::string rowStr(maze.nCols(), '.');
    for (int col = 0; col < maze.nCols(); ++col)
    {
      Coord coord{ row, col };
      DEBUG(rowStr[col] = maze[coord].symbol());
      if (loopMap[coord])
      {
        Tile mazeTile = maze[coord];

        // Any pipe that doesn't have a westward connection is either a
        // vertical pipe or the start of a horizontal sequence.  Any pipe that
        // does have a horizontal connection is a continuation of a horizontal
        // sequence.
        if (mazeTile == verticalTile)
          isEnclosed = ! isEnclosed;
        else if (mazeTile.edge2() != WEST)
          // Elbow starting horizontal sequence
          startVertical = mazeTile.edge1();
        else if (mazeTile.edge1() != EAST)
          // Elbow ending horizontal sequence
          if (startVertical != mazeTile.edge1())
            isEnclosed = ! isEnclosed;
      }
      else
      {
        ++(isEnclosed ? enclosed : outside);
        DEBUG(rowStr[col] = (isEnclosed ? 'I' : 'O'));
      }
    }
    if (startCoord.row == row) rowStr[startCoord.col] = 'S';
    DEBUG(std::cout << rowStr << std::endl);
  }

  std::cout <<   "Total area    = " << maze.nRows() * maze.nCols()
            << "\nLoop length   = " << loopLen
            << "\nEnclosed area = " << enclosed
            << "\nOutside area  = " << outside << std::endl;
}
