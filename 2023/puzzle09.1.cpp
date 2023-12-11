// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT
#include <aoc_util.h>

using namespace aoc;

int64 computeNextVal(const std::vector<int64>& sequence)
{
  std::vector<int64> lastValues;       // Last sequence value at each level
  lastValues.push_back(sequence.back());

  // Generational sequence generation
  std::vector<int64> currSeq(sequence), nextSeq;
  nextSeq.reserve(sequence.size());
  bool allzeros = false;
  while (! allzeros)
  {
    allzeros = true;
    nextSeq.clear();
    for (std::size_t i = 1; i < currSeq.size(); ++i)
    {
      auto diff = currSeq[i] - currSeq[i - 1];
      nextSeq.push_back(diff);
      if (diff != 0) allzeros = false;
    }
    lastValues.push_back(nextSeq.back());

    currSeq.swap(nextSeq);
  }

  int64 result = 0;
  DEBUG(std::cout << "last values:");
  for (auto val : lastValues)
  {
    DEBUG(std::cout << ' ' << val);
    result += val;
  }
  DEBUG(std::cout << std::endl);

  return result;
}

int main(int argc, char *argv[])
{
  int64 result = 0;

  auto input = openInput(argc, argv);
  for (auto line : InputByLine(input))
  {
    auto sequence = parseNumbers<int64>(line);
    int64 next = computeNextVal(sequence);
    DEBUG(std::cout << line << " (" << next << ")\n");
    result += next;
  }

  std::cout << "result = " << result << std::endl;
}
