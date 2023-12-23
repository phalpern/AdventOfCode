// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT 1
#include <aoc_util.h>
#include <string_view>
#include <string>

using namespace aoc;

unsigned char hash(std::string_view s)
{
  unsigned current = 0;
  for (char c : s)
  {
    if (c == '\n') continue;  // Ignore line breaks
    current += static_cast<unsigned char>(c);
    current *= 17;
    current &= 255;
  }

  DEBUG(std::cout << "hash(" << s << ") = " << current << '\n');
  return current;
}

int main(int argc, char *argv[])
{
  int64 result = 0;

  auto input = openInput(argc, argv);
  std::string inputStr;
  std::getline(input, inputStr, '\0');  // Slurp entire file
  inputStr += ',';  // Trailing comma makes parsing easier
  DEBUG2(std::cout << "inputStr = " << inputStr << '\n');

  std::string::size_type stepBeginIdx = 0;
  for (auto stepEndIdx = inputStr.find(','); stepEndIdx != std::string::npos;
       stepEndIdx = inputStr.find(',', stepBeginIdx))
  {
    auto stepLen = stepEndIdx - stepBeginIdx;
    result += hash(std::string_view(inputStr).substr(stepBeginIdx, stepLen));
    stepBeginIdx = stepEndIdx + 1;
  }

  std::cout << "result = " << result << std::endl;
}
