// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT
#include <aoc_util.h>

using namespace aoc;

int64 computePrevVal(const std::vector<int64>& sequence)
{
  std::vector<int64> firstValues;       // Last sequence value at each level
  firstValues.push_back(sequence.front());

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
    firstValues.push_back(nextSeq.front());

    currSeq.swap(nextSeq);
  }

  int64 result = 0;
  DEBUG(printContainer(std::cout <<"old first values: ", firstValues) << '\n');
  DEBUG(std::cout << "new first values:");
  for (auto i = firstValues.rbegin(); i != firstValues.rend(); ++i)
  {
    int64 newFirst = *i - result;
    DEBUG(std::cout << ' ' << newFirst);
    result = newFirst;
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
    int64 prev = computePrevVal(sequence);
    DEBUG(printContainer(std::cout << "(" << prev << ") ", sequence) << "\n");
    result += prev;
  }

  std::cout << "result = " << result << std::endl;
}
