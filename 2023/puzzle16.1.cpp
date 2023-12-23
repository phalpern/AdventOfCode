// -*- mode: c++; c-basic-offset: 2 -*-

#define DEBUGPRINT
#include <aoc_util.h>
#include <vector>
#include <string>
#include <utility>

using namespace aoc;

// Bit pattern representing zero or more direction
enum Dir { NO_DIR, RIGHT = 1, DOWN = 2, LEFT = 4, UP = 8, ALL = 15 };

struct Beam
{
  int row;
  int col;
  Dir direction;

  constexpr operator bool() const { return direction != NO_DIR; }

  constexpr bool inGrid(int nRows, int nCols)
  {
    return direction != NO_DIR &&
      0 <= row && row < nRows && 0 <= col && col < nCols;
  }

  Beam next(Dir newDir) const;
};

Beam Beam::next(Dir newDir) const
{
  constexpr int X = 2;  // Unused delta

  // Direction:                     R   D      L            U
  constexpr int rowDeltas[] = { X,  0,  1, X,  0, X, X, X, -1 };
  constexpr int colDeltas[] = { X,  1,  0, X, -1, X, X, X,  0 };

  ASSERT(NO_DIR < newDir && newDir <= UP);

  auto rowDelta = rowDeltas[newDir];
  auto colDelta = colDeltas[newDir];
  ASSERT(rowDelta != X && colDelta != X);

  return { row + rowDelta, col + colDelta, newDir };
}

constexpr Beam nullBeam { 0, 0, NO_DIR };

// Return the beam or beams emerging from the specified cell.  Update
// activation to include the incoming direction.  If this is a repeat, return
// two null beams (to prevent infinite looping); if there is only one beam
// emerging, return one null and one non-null beam; if this is a splitter,
// return two non-null beams.
std::pair<Beam, Beam> processBeam(const Beam& beamIn, char cell,
                                  Dir& activation)
{
  constexpr Dir X = NO_DIR;  // Unused value

  // Map a direction to a new direction for '/' and '\'
  // Start Direction:             RIGHT   DOWN     LEFT             UP
  //                              -----  -----     ----           -----
  constexpr Dir slash[]     = { X,   UP,  LEFT, X, DOWN, X, X, X, RIGHT };
  constexpr Dir backslash[] = { X, DOWN, RIGHT, X,   UP, X, X, X,  LEFT };

  auto direction = beamIn.direction;

  if (activation & direction)
    return { nullBeam, nullBeam };  // Been here before

  activation = Dir(activation | direction);

  if ('|' == cell && (direction & (RIGHT | LEFT)))
    // Split into 2 vertical beams
    return { beamIn.next(DOWN), beamIn.next(UP) };
  else if ('-' == cell && (direction & (DOWN  | UP)))
    // Split into 2 horizontal beams
    return { beamIn.next(RIGHT), beamIn.next(LEFT) };
  else if ('/' == cell)
    // Reflect through / angled mirror
    return { beamIn.next(slash[direction]), nullBeam };
  else if ('\\' == cell)
    // Reflect through \ angled mirror
    return { beamIn.next(backslash[direction]), nullBeam };
  else
    // Pass through
    return { beamIn.next(direction), nullBeam };
}

std::ostream& printActivations(const std::vector<std::vector<Dir>>& activation)
{
  constexpr char sym[] = { '.', '>', 'V', 'J', '<', '=', 'L', 'W',
                           '^', 'P', '|', ']', 'F', 'A', '[', '+' };
  for (const auto& r : activation)
  {
    for (auto a : r)
      std::cout << sym[a];
    std::cout << '\n';
  }

  return std::cout;
}

int main(int argc, char *argv[])
{
  std::vector<std::string> grid;

  auto input = openInput(argc, argv);
  for (auto line : InputByLine(input))
  {
    grid.push_back(line);
  }

  int nRows = grid.size();
  int nCols = grid.front().size();

  std::vector activations( nRows, std::vector( nCols, NO_DIR ) );

  std::vector workQueue{ 1, Beam{ 0, 0, RIGHT } };
  while (! workQueue.empty())
  {
    Beam currBeam = workQueue.back();
    workQueue.pop_back();

    auto [ newBeam1, newBeam2 ] =
      processBeam(currBeam,
                  grid[currBeam.row][currBeam.col],
                  activations[currBeam.row][currBeam.col]);

    if (newBeam1.inGrid(nRows, nCols))
      workQueue.push_back(newBeam1);
    if (newBeam2.inGrid(nRows, nCols))
      workQueue.push_back(newBeam2);
  }

  int result = 0;

  DEBUG(printActivations(activations));

  for (const auto& activationRow : activations)
    for (auto activation : activationRow)
      if (activation != NO_DIR)
        ++result;

  std::cout << "\nresult = " << result << "\n\n";
}
