// puzzle03.1.cpp                                                     -*-C++-*-

#include <aoc_util.h>
#include <vector>

using namespace aoc;

int main(int argc, char *argv[])
{
    long result = 0;

    using size_type = std::string::size_type;
    constexpr auto npos = std::string::npos;

    // 2-D representation of engine schematic
    std::vector<std::string> schematic;

    auto input = openInput(argc, argv);
    for (auto line : InputByLine(input))
    {
        // Insert a row of dots before first real row
        if (schematic.empty())
            schematic.emplace_back(line.length() + 2, '.');
        // Add row, with an extra dot at the front and back.
        schematic.push_back("." + line + '.');
    }

    // Append a row of dots after last real row
    schematic.emplace_back(schematic[0].length(), '.');

    for (size_type i = 1; i < schematic.size() - 1; ++i)
    {
        const std::string& row = schematic[i];
        size_type nstart = 0, nend = 0;
        while ((nstart = row.find_first_of("0123456789", nend)) != npos)
        {
            nend = row.find_first_not_of("0123456789", nstart);
            bool adjacent = false;
            if (row[nstart - 1] != '.' || row[nend] != '.')
                adjacent = true;
            else
            {
                auto sym = schematic[i - 1].find_first_not_of("0123456789.",
                                                              nstart - 1);
                if (sym != npos && sym <= nend)
                    adjacent = true;
                else
                {
                    sym = schematic[i + 1].find_first_not_of("0123456789.",
                                                              nstart - 1);
                    if (sym != npos && sym <= nend)
                        adjacent = true;
                }
            }

            if (adjacent)
            {
                auto partnum = std::strtol(&row[nstart], nullptr, 10);
                result += partnum;
            }
        }
    }

    std::cout << "result = " << result << std::endl;
}
