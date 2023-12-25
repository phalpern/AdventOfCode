// -*- mode: c++; c-basic-offset: 2 -*-

#define DEBUGPRINT
#include <aoc_util.h>
#include <vector>
#include <queue>
#include <climits>

using namespace aoc;

enum Dir { NORTH, EAST, SOUTH, WEST };

// Representation a step (including its direction and repeat count) and its
// target (row and column).
struct Step
{
  Dir direction;    // Direction of last movement
  int repeatCount;  // [0-3] Consecutive steps in same direction
  int row;          // target row
  int col;          // target column
};

// Grid that keeps track of the lowest-cost path to each possible step.
// It is a  maps a `Step` to an integral total heat loss for a path and is
// used to keep track of cheapest (least lossy) path that reaches any
// particular step.
class StepToHeatLoss
{
  // Four-demensional array indexed by row, column, direction, and repeat
  // count.
  std::vector<int> m_array;
  int              m_nRows;
  int              m_nCols;

  int calcIdx(const Step& s) const
  {
    constexpr int nDirs = 4;
    constexpr int nCounts = 3;
    // Since repeat count is typically in range [1-3], subtract one, but add
    // back one for initial-step repreat count of 0
    auto idx = (((s.row * m_nCols) + s.col) * nDirs +
                s.direction) * nCounts + (s.repeatCount - 1) + 1;
    ASSERT(0 <= idx && idx < m_array.size());
    return idx;
  }

public:
  StepToHeatLoss(int nRows, int nCols)
    // Leave one extra slot for initial repeat count of 0.
    : m_array(nRows * nCols * 4 * 3 + 1, INT_MAX)
    , m_nRows(nRows)
    , m_nCols(nCols)
    { }

  int& operator[](const Step& s)       { return m_array[calcIdx(s)]; }
  int  operator[](const Step& s) const { return m_array[calcIdx(s)]; }

  bool isValidStep(const Step& s) const
  {
    return (0 <= s.row && s.row < m_nRows && 0 <= s.col && s.col < m_nCols &&
            s.repeatCount < 4);
  }
};

// Compute the 3 possible steps to execute next.  Note that some of the
// resulting steps might not be valid; the caller is responsible for ignoring
// the invlid ones (as determined by `StepToHeatLoss::isValidStep`.
std::array<Step, 3> calcNextSteps(const Step& fromStep)
{
  // Row and column deltas for each of the 4 directions
  constexpr std::array deltas{
    std::pair{ -1,  0 }, // NORTH
    std::pair{  0,  1 }, // EAST
    std::pair{  1,  0 }, // SOUTH
    std::pair{  0, -1 }  // WEST
  };

  // First of three directions to return.  The direction opposite
  // `fromStep.direction`, is deliberately excluded because we are not allowed
  // to turn around 180%.
  Dir dir = Dir((fromStep.direction + 3) % 4);

  std::array<Step, 3> result;
  for (auto& resultStep : result)
  {
    resultStep.direction = dir;
    resultStep.repeatCount =
      ((dir == fromStep.direction) ? fromStep.repeatCount + 1 : 1);
    resultStep.row = fromStep.row + deltas[dir].first;
    resultStep.col = fromStep.col + deltas[dir].second;

    dir = Dir((dir + 1) % 4);  // Next direction
  }

  return result;
}

int main(int argc, char *argv[])
{
  int result = 0;

  auto input = openInput(argc, argv);
  std::vector<std::vector<short>> grid;
  std::vector<short> gridRow;
  for (auto line : InputByLine(input))
  {
    gridRow.resize(line.size());
    for (int i = 0; i < line.size(); ++i)
      gridRow[i] = line[i] - '0';
    grid.push_back(gridRow);
  }

  StepToHeatLoss heatLossMap(grid.size(), grid.front().size());

  std::priority_queue workQueue{
    [&heatLossMap](const Step& a, const Step& b) {
      // Higher priority is smaller heat loss
      return heatLossMap[a] > heatLossMap[b];
    }, std::vector<Step>{} };

  // The initial step is chosen so as to minimize special cases.  It is the
  // only step with a repeat count of 0.
  Step initialStep{ EAST, 0, 0, 0 };
  workQueue.push(initialStep);
  heatLossMap[initialStep] = 0;

  const int goalRow = grid.size() - 1;
  const int goalCol = grid.front().size() - 1;

  // Do breath-first search, always following the least-lossy path until the
  // end is reached.
  while (! workQueue.empty())
  {
    auto workItem = workQueue.top();
    workQueue.pop();

    auto currHeatLoss = heatLossMap[workItem];
    if (workItem.row == goalRow && workItem.col == goalCol)
    {
      // End iteration when we've reached the lower-right corner
      result = currHeatLoss;
      break;
    }

    for (auto step : calcNextSteps(workItem))
    {
      if (! heatLossMap.isValidStep(step))
        continue;

      auto& stepLoss = heatLossMap[step];  // Best score so far for this step
      auto nextLoss = currHeatLoss + grid[step.row][step.col];
      if (nextLoss < stepLoss)
      {
        // Founder cheaper way to get to this step
        stepLoss = nextLoss;  // Update to lower loss score
        workQueue.push(step); // Continue travel from here
      }
    }
  }

  std::cout << "\nresult = " << result << "\n\n";
}
