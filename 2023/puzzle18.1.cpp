// -*- mode: c++; c-basic-offset: 2 -*-

#define DEBUGPRINT
#include <aoc_util.h>
#include <vector>
#include <algorithm>
#include <cstdlib>

using namespace aoc;

struct Instruction
{
  char     dir;
  int      meters;
  unsigned color;
};

void doInstruction(int& row, int& col, char dir, int meters)
{
  switch (dir)
  {
   case 'U': row -= meters; break;
   case 'R': col += meters; break;
   case 'D': row += meters; break;
   case 'L': col -= meters; break;
  }
}

std::ostream& printGrid(const std::vector<std::vector<unsigned>>& grid)
{
  for (auto& scanRow : grid)
  {
    for (auto cell : scanRow)
      std::cout << (cell ? '#' : '.');
    std::cout << '\n';
  }

  return std::cout;
}

int main(int argc, char *argv[])
{
  int result = 0;

  std::vector<Instruction> plan;

  auto input = openInput(argc, argv);
  for (auto line : InputByLine(input))
  {
    Instruction step;

    char* endNum;
    step.dir = line[0];
    step.meters = std::strtol(&line[1], &endNum, 10);
    step.color  = std::strtoul(endNum + 3, &endNum, 16);
    ASSERT(*endNum == ')');

    ASSERT(step.color != 0);  // Assume black is empty

    plan.push_back(step);
  }

  int minRow = 0, maxRow = 0;
  int minCol = 0, maxCol = 0;
  int row = 0, col = 0;
  for (auto step : plan)
  {
    doInstruction(row, col, step.dir, step.meters);
    minRow = std::min(row, minRow);
    maxRow = std::max(row, maxRow);
    minCol = std::min(col, minCol);
    maxCol = std::max(col, maxCol);
  }

  DEBUG(std::cout << "(minRow, minCol) = (" << minRow << ", " << minCol <<
        "), " << "(maxRow, maxCol) = (" << maxRow << ", " << maxCol << ")\n");

  auto numRows = maxRow - minRow + 1;
  auto numCols = maxCol - minCol + 1;
  std::vector grid(numRows + 2, std::vector(numCols + 1, 0U));

  row = -minRow + 1;
  col = -minCol;
  grid[row][col] = plan[0].color;
  for (auto step : plan)
  {
    for (int i = 0; i < step.meters; ++i)
    {
      doInstruction(row, col, step.dir, 1);
      grid[row][col] = step.color;
    }
  }
  ASSERT(row == -minRow + 1 && col == -minCol);
  DEBUG(printGrid(grid) << "\n");

  auto grid2 = grid;
  for (int i = 1; i < numRows + 1; ++i)
  {
    auto& scanRow = grid[i];
    unsigned fill = 0;

    for (int j = 0; j < numCols; ++j)
    {
      if (scanRow[j] == 0)
        grid2[i][j] = fill;
      else
      {
        auto endEdge = (std::find(scanRow.begin() + j, scanRow.end(), 0U) -
                        scanRow.begin() - 1);
        if ((grid[i + 1][j] == 0) == (grid[i - 1][endEdge] == 0))
        {
          //         #         #     #
          // Either  #  or  ####  or ####
          //         #      #           #
          fill = ~fill;
        }

        j = endEdge;
      }
    }
  }
  DEBUG(printGrid(grid2) << "\n");

  for (const auto& scanRow : grid2)
    for (auto cell : scanRow)
      if (cell)
        ++result;

  std::cout << "\nresult = " << result << "\n\n";
}
