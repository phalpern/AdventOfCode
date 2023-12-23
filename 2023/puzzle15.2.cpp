// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT 1
#include <aoc_util.h>
#include <string_view>
#include <string>
#include <vector>
#include <array>

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

  DEBUG2(std::cout << "hash(" << s << ") = " << current << '\n');
  return current;
}

struct Lens
{
  std::string_view label;
  int              focalLen;
};

using Box = std::vector<Lens>;

void deleteLens(Box& b, std::string_view label)
{
  auto found =  std::find_if(b.begin(), b.end(), [label](const Lens& lens) {
                                                   return lens.label == label;
                                                 });
  if (found != b.end())
    b.erase(found);
}

void addLens(Box& b, std::string_view label, int focalLen)
{
  auto found =  std::find_if(b.begin(), b.end(),
                             [label](const Lens& lens) {
                               return lens.label == label;
                             });

  if (found == b.end())
    b.push_back({ label, focalLen });
  else
    found->focalLen = focalLen;
}

int main(int argc, char *argv[])
{
  std::array<Box, 256> boxes;

  auto input = openInput(argc, argv);
  std::string inputStr;
  std::getline(input, inputStr, '\0');  // Slurp entire file
  inputStr += ',';  // Trailing comma makes parsing easier
  DEBUG2(std::cout << "inputStr = " << inputStr << '\n');

  std::string::size_type stepBeginIdx = 0;
  for (auto stepEndIdx = inputStr.find(','); stepEndIdx != std::string::npos;
       stepEndIdx = inputStr.find(',', stepBeginIdx))
  {
    std::string_view step(&inputStr[stepBeginIdx], &inputStr[stepEndIdx]);
    auto opPos = step.find_first_of("=-");
    std::string_view label = step.substr(0, opPos);
    char operation = step[opPos];

    unsigned boxNum = hash(label);
    Box& box = boxes[boxNum];

    if (operation == '-')
      deleteLens(box, label);
    else
    {
      auto focalLen = strviewToInt(step.substr(opPos + 1));
      addLens(box, label, focalLen);
    }

    DEBUG(std::cout << "\nAfter \"" << step << "\":\nBox " << boxNum << ':';
    for (auto lens : box)
      std::cout << " [" << lens.label << ' ' << lens.focalLen << ']';
    std::cout << std::endl);

    stepBeginIdx = stepEndIdx + 1;
  }

  int64 result = 0;
  for (int boxNum = 0; boxNum < 256; ++boxNum)
  {
    const auto& box = boxes[boxNum];
    for (int slot = 0; slot < box.size(); ++slot)
    {
      auto power = (boxNum + 1) * (slot + 1) * box[slot].focalLen;
      result += power;
    }
  }

  std::cout << "result = " << result << "\n\n";
}
