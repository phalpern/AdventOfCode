// puzzle24.2d.cpp                                                    -*-C++-*-

#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <string_view>
#include <variant>
#include <vector>

#include <cassert>
#include <cstdlib>

struct Range
{
    // Range of integer values.  A function returning this aggregate can be
    // used with structured bindings.

    int min;
    int max;

    constexpr Range() : min(0), max(0) { }
    explicit constexpr Range(int val) : min(val), max(val) {}
    constexpr Range(int mn, int mx) : min(mn), max(mx) { assert(mn <= mx); }
    constexpr Range(std::pair<int, int> minmax)
        : min(minmax.first), max(minmax.second) { }
};

std::ostream& operator<<(std::ostream& os, const Range& r)
{
    return os << '(' << r.min << ", " << r.max << ')';
}

constexpr int numRegs = 4;

using RegisterSet = std::array<Range, numRegs>;

class Register
{
public:
    constexpr explicit Register(int index) : m_index(index)
        { assert(0 <= index && index < numRegs); }

    constexpr Range getRange(const RegisterSet& regs) const
        { return Range(regs[m_index]); }

    void setRange(RegisterSet& regs, const Range& range) const
        { regs[m_index] = range; }

private:
    int m_index;
};

class Op
{
public:
    using ExecFunc = Range (const RegisterSet& registers, Range a, Range b);

    constexpr Op(ExecFunc* f, Register target, int source)
        : m_execFunc(f), m_target(target), m_source(source) { }
    constexpr Op(ExecFunc* f, Register target, Register source)
        : m_execFunc(f), m_target(target), m_source(source) { }

    bool isInp() const;

    void exec(RegisterSet& registers) const
    {
        Range a = m_target.getRange(registers);
        Range b;
        if (m_source.index() == 0)
        {
            int val = std::get<0>(m_source);
            b = Range(val, val);
        }
        else
        {
            b = std::get<1>(m_source).getRange(registers);
        }

        m_target.setRange(registers, m_execFunc(registers, a, b));
    //    std::cout << m_target.getRange(registers) << std::endl;
    }

private:
    // An instruction representing an opcode and two operands.
    ExecFunc*                   m_execFunc;
    Register                    m_target;
    std::variant<int, Register> m_source;
};

std::vector<int>* prefixValues_p;

Range opInp(const RegisterSet& registers, Range a, Range b)
{
    int inputNum = b.min;
    if (inputNum < prefixValues_p->size())
        return Range((*prefixValues_p)[inputNum]);
    else
        return Range(1, 9);
}

Range opAdd(const RegisterSet& registers, Range a, Range b)
{
    return Range(a.min + b.min, a.max + b.max);
}

Range opMul(const RegisterSet& registers, Range a, Range b)
{
    auto [minA, maxA] = a;
    auto [minB, maxB] = b;
    return std::minmax(
        { minA * minB, minA * maxB, maxA * minB, maxA * maxB });
}

Range opDiv(const RegisterSet& registers, Range a, Range b)
{
    auto [minA, maxA] = a;
    auto [minB, maxB] = b;
    assert(minB != 0 and maxB != 0);
    return std::minmax(
        { minA / minB, minA / maxB, maxA / minB, maxA / maxB });
}

Range opMod(const RegisterSet& registers, Range a, Range b)
{
    auto [minA, maxA] = a;
    auto [minB, maxB] = b;
    assert(minB > 0 and maxB > 0);
    return std::minmax(
        { minA % minB, minA % maxB, maxA % minB, maxA % maxB });
}

Range opEql(const RegisterSet& registers, Range a, Range b)
{
    if (a.max < b.min or a.min > b.max)
        return Range(0);     // No overlap in ranges
    else if (a.max == b.min and a.min == b.max)
        return Range(1);     // All the same values
    else
        return Range(0, 1);  // Could be equal or not
}

inline bool Op::isInp() const { return m_execFunc == opInp; }

const std::map<std::string_view, Op::ExecFunc*> operations {
    { "inp", &opInp },
    { "add", &opAdd },
    { "mul", &opMul },
    { "div", &opDiv },
    { "mod", &opMod },
    { "eql", &opEql }
};

Op parseInstr(const char* instrStr)
{
    static int inputCount = 0;

    std::string_view opcode(instrStr, 3);
    assert(' ' == instrStr[3]);
    auto operation = operations.at(opcode);
    Register target(instrStr[4] - 'w');

    if (operation == opInp)
        return Op(operation, target, inputCount++);
    else if (std::isalpha(instrStr[6]))
        return Op(operation, target, Register(instrStr[6] - 'w'));
    else
        return Op(operation, target, std::atoi(instrStr + 6));
}

void printDigits(const char* prefix, const std::vector<int>& digits)
{
    char buff[] = "              ";
    char* p = buff;
    for (int d : digits)
        *p++ = '0' + d;
    std::cout << prefix << buff << std::flush;
}

std::vector<int> solve(const RegisterSet&      startRegisters,
                       const std::vector<Op>&  instructions,
                       int                     startInstr = 0,
                       const std::vector<int>& startInpPrefix = { })
{
    if (startInpPrefix.size() >= 14)
        return startInpPrefix;

    std::vector<int> inpPrefix;
    inpPrefix.reserve(startInpPrefix.size() + 1);
    inpPrefix = startInpPrefix;
    inpPrefix.push_back(0);

    // Iterate last prefix value in range 1 to 9
    for (int i = 1; i < 10; ++i)
    {
        inpPrefix.back() = i;
        prefixValues_p = &inpPrefix;  // Must be reset every iteration

        RegisterSet registers = startRegisters;

        int nextGroupInstr = instructions.size();
        RegisterSet nextGroupRegs;

        // Execute instructions up to and including an `OpInp` instruction.
        for (int instIndex = startInstr; instIndex < instructions.size();
             ++instIndex)
        {
            auto& instruction = instructions[instIndex];
            instruction.exec(registers);
            if (instruction.isInp())
            {
                // Take snapshot after `opInp` instruction
                nextGroupInstr = instIndex + 1;
                nextGroupRegs  = registers;
                break;
            }
        }
        // Execute the remaining instructions.
        for (int instIndex = nextGroupInstr; instIndex < instructions.size();
             ++instIndex)
        {
            auto& instruction = instructions[instIndex];
            instruction.exec(registers);
        }

        auto [minE, maxE] = registers[3];  // z register
        if (minE <= 0 and 0 <= maxE)
        {
            // Found partial solution.  Recurse down another level.
            // Nested levels can start after last input, since everything up to
            // that point is fixed.
            // if (inpPrefix.size() < 8)
            //     printDigits("\rPartial = ", inpPrefix);
            auto solution = solve(nextGroupRegs, instructions, nextGroupInstr,
                                  inpPrefix);
            if (! solution.empty())
                return solution;  // Solved!
        }
    }  // end for digit values 1 to 9

    return {};
}

int main()
{
    std::ifstream infile("puzzle24_input.txt");

    std::vector<Op> instructions;
    while (infile)
    {
        char line[16];
        infile.getline(line, sizeof(line));
        if ('\0' == line[0])
            break;
        instructions.push_back(parseInstr(line));
    }

    std::cout << instructions.size() << " instructions processed. Solving..."
              << std::endl;

    auto solution = solve(RegisterSet{}, instructions);

    printDigits("\nSolution = ", solution);
}
