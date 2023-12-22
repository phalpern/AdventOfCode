// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT
#include <aoc_util.h>
#include <utility>

using namespace aoc;

int main(int argc, char *argv[])
{
  std::vector<std::string> platform;

  auto input = openInput(argc, argv);
  for (auto line : InputByLine(input))
    platform.push_back(std::move(line));

  // For each column c, nextSlot[c] is the index of the next row that will hold
  // a round rock after it has rolled north.  Initialize it to all zeros.
  std::vector<int> nextSlot(platform.front().size(), 0);

  int64 result = 0;

  for (int r = 0; r < platform.size(); ++r)
  {
    const auto& row = platform[r];

    for (int c = 0; c < row.size(); ++c)
    {
      auto rock = row[c];
      if (rock == 'O')
      {
        // Round rock will occupy the next slot.  No need to actually track the
        // invidivual rocks.
        auto rockSlot = nextSlot[c]++;  // Slot occupied by this rock
        result += (platform.size() - rockSlot);
      }
      else if (rock == '#')
        nextSlot[c] = r + 1;
    }
  }

  std::cout << "result = " << result << std::endl;
}
