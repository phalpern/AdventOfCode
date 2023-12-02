#include <aoc_util.h>
#include <unordered_map>

using namespace aoc;

std::unordered_map<std::string, int> toDigit{
    { "0", 0 },
    { "1", 1 },
    { "2", 2 },
    { "3", 3 },
    { "4", 4 },
    { "5", 5 },
    { "6", 6 },
    { "7", 7 },
    { "8", 8 },
    { "9", 9 },
    { "zero", 0 },
    { "one", 1 },
    { "two", 2 },
    { "three", 3 },
    { "four", 4 },
    { "five", 5 },
    { "six", 6 },
    { "seven", 7 },
    { "eight", 8 },
    { "nine", 9 }
};

int main(int argc, char *argv[])
{
// The problem statement does not specify that "zero" is a valid digit
//  std::regex re("[0-9]|zero|one|two|three|four|five|six|seven|eight|nine");
    std::regex re("[0-9]|one|two|three|four|five|six|seven|eight|nine");

    int result = 0;

    auto input = openInput(argc, argv);
    for (auto line : InputByLine(input))
    {
        std::smatch m;

        ASSERT(std::regex_search(line, m, re));
        int f = toDigit[m[0]];
        auto next = m[0].first + 1;  // In case next match overlaps

        int l = f;
        while (std::regex_search(next, line.cend(), m, re))
        {
            l = toDigit[m[0]];
            next = m[0].first + 1;
        }

        result += 10 * f + l;

        // std::cout << line << " " << (10 * f + l) << std::endl;
    }

    std::cout << "result = " << result << std::endl;
}
