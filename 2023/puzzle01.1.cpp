#include <aoc_util.h>
#include <cassert>

using namespace aoc;

int main(int argc, char *argv[])
{
    std::regex first_re("^[^0-9]*([0-9])");
    std::regex last_re("([0-9])[^0-9]*$");

    int result = 0;

    auto input = openInput(argc, argv);
    for (auto line : InputByLine(input))
    {
        std::smatch m;

        ASSERT(std::regex_search(line, m, first_re));
        char f = m[1].str()[0];

        ASSERT(std::regex_search(line, m, last_re));
        char l = m[1].str()[0];

        result += 10 * (f - '0') + (l - '0');
    }

    std::cout << "result = " << result << std::endl;
}
