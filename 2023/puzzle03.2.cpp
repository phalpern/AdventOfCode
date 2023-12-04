// puzzle03.1.cpp                                                     -*-C++-*-

#include <aoc_util.h>
#include <vector>
#include <unordered_map>

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

    std::unordered_map<const char*, std::vector<long>> gearToParts;

    for (size_type i = 1; i < schematic.size() - 1; ++i)
    {
        const std::string& row = schematic[i];
        size_type nstart = 0, nend = 0;
        while ((nstart = row.find_first_of("0123456789", nend)) != npos)
        {
            nend = row.find_first_not_of("0123456789", nstart);
            const char* gear = nullptr;
            if (row[nstart - 1] == '*')
                gear = &row[nstart - 1];
            else if (row[nend] == '*')
                gear = &row[nend];
            else
            {
                auto sym = schematic[i - 1].find("*", nstart - 1);
                if (sym != npos && sym <= nend)
                    gear = &schematic[i - 1][sym];
                else
                {
                    sym = schematic[i + 1].find("*", nstart - 1);
                    if (sym != npos && sym <= nend)
                        gear = &schematic[i + 1][sym];
                }
            }

            if (gear)
            {
                auto partnum = std::strtol(&row[nstart], nullptr, 10);
                gearToParts[gear].push_back(partnum);
            }
        }
    }

    for (const auto& [gear, parts] : gearToParts)
    {
        if (parts.size() == 2)
            result += parts[0] * parts[1];
    }

    std::cout << "result = " << result << std::endl;
}
