// Advent of code day 24, part 1
// Find largest MONAD model number.

// This is a C++ re-implementation of `puzzle24.1.py`

#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <memory>
#include <string>
#include <string_view>
#include <utility>
#include <variant>
#include <vector>

#include <cassert>
#include <climits>
#include <cstdlib>

namespace {

struct Range
{
    int min, max;

    friend std::ostream& operator<<(std::ostream& os, const Range& rng)
    {
        os << '[';
        if (rng.min == INT_MIN && rng.max == INT_MAX)
            os << "FULL_RANGE";
        else
        {
            if (rng.min == INT_MIN) os << "INT_MIN, ";
            else os << rng.min << ", ";
            if (rng.max == INT_MAX) os << "INT_MAX";
            else os << rng.max;
        }
        return os << ']';
    }
};

constexpr Range fullRange{INT_MIN, INT_MAX};

std::vector<int> trialInputVals{INT_MAX};

enum class RoundingMode { Zero, Floor, Ceiling };

// Return `a` divided by `b` using the specified rounding `mode`.
int div(int a, int b, RoundingMode mode = RoundingMode::Zero)
{
    if (RoundingMode::Zero == mode)
        return a / b;  // Truncation towards zero is natural for C++

    bool isneg = (a < 0) != (b < 0);
    if (isneg == (RoundingMode::Ceiling == mode))
    {
        // Either positive rounding towards the floor or negative rounding
        // towards the ceiling.  In both cases, the result is equivalent to
        // rounding towards zero, i.e., the C++ natural mode.
        return a / b;
    }
    else
    {
        // Either negative rounding towards the floor or positive rounding
        // towards the ceiling.  In both cases, the result is rounded away from
        // zero.
        int adjustment = a < 0 ? -b + 1 : -b - 1;
        return (a + adjustment) / b;
    }
}

class Op;  // Forward declaration

using OpPtr          = std::shared_ptr<Op>;

class Expression
{
    std::variant<std::monostate, int, OpPtr> m_exp;

public:

    static const Expression zero;
    static const Expression one;

    constexpr Expression() { }
    constexpr Expression(int i)   : m_exp(i) { }
    Expression(OpPtr p) : m_exp(std::move(p)) { }

    // Follows rule of zero for copy and destruction

    bool isNull() const { return m_exp.index() == 0; }
    bool isInt()  const { return m_exp.index() == 1; }
    bool isOp()   const { return m_exp.index() == 2; }

    Range range() const;

    int asInt() const { assert(isInt()); return std::get<1>(m_exp); }
    OpPtr asOp() const { assert(isOp());  return std::get<2>(m_exp); }

    operator int()     const { return asInt(); }
    OpPtr operator->() const { return asOp();  }
    Op& operator*()    const { return *asOp(); }

    // Recursively simplify this expression and return the simplified version.
    Expression simplify() const;

    void dump(int depth = 1, int indent = 0) const;

    friend bool operator==(const Expression& lhs, const Expression& rhs)
        { return lhs.m_exp == rhs.m_exp; }
    friend bool operator!=(const Expression& lhs, const Expression& rhs)
        { return lhs.m_exp != rhs.m_exp; }
};

const Expression Expression::zero{0};
const Expression Expression::one{1};

// Note that opcode names are capitalized because `not` and `eql` are C++
// keywords.
enum class Opcode { Inp, Add, Mul, Div, Mod, Eql, Not, NumOpcodes };

const char* const OpcodeNames[] = {
    "inp", "add", "mul", "div", "mod", "eql", "not"
};

Opcode nameToOpcode(std::string_view name)
{
    const char* const* found = std::find(std::begin(OpcodeNames),
                                         std::end(OpcodeNames), name);
    return static_cast<Opcode>(found - OpcodeNames);
}

// Representation of an operation
class Op
{
    using StepSimplifier = Expression (*)(OpPtr&&);

    Opcode         m_opcode;
    Expression     m_operand1;
    Expression     m_operand2;
    Range          m_range;

    std::size_t opIndex() const { return static_cast<std::size_t>(m_opcode); }

    static Expression replaceRange(const OpPtr& p, const Range& newRange);

    // Simplifiers
    static Expression Inp(OpPtr&& opp);
    static Expression Add(OpPtr&& opp);
    static Expression Mul(OpPtr&& opp);
    static Expression Div(OpPtr&& opp);
    static Expression Mod(OpPtr&& opp);
    static Expression Eql(OpPtr&& opp);
    static Expression Not(OpPtr&& opp);

    // Lookups for names and simplifiers
    static const StepSimplifier s_simplifiers[(std::size_t)Opcode::NumOpcodes];

  public:
    template <typename T1>
    Op(Opcode oc, T1&& operand1, const Range& range)
        : m_opcode(oc)
        , m_operand1(std::forward<T1>(operand1))
        , m_range(range) { }

    template <typename T1, typename T2>
    Op(Opcode oc, T1&& operand1, T2&& operand2, const Range& range)
        : m_opcode(oc)
        , m_operand1(std::forward<T1>(operand1))
        , m_operand2(std::forward<T2>(operand2))
        , m_range(range) { }

    // Not assignable
    Op& operator=(const Op&) = delete;

    const char*       name()     const { return OpcodeNames[opIndex()]; }
    const Opcode      opcode()   const { return m_opcode; }
    const Expression& operand1() const { return m_operand1; }
    const Expression& operand2() const { return m_operand2; }
    const Range&      range()    const { return m_range; }

    // Must be `static` rather than member function because the equivalent of
    // `this` is passed as a `shared_ptr` instead of a raw pointer.
    static Expression simplifyStep(OpPtr thisOp)
    {
        auto simplifier =
            s_simplifiers[static_cast<std::size_t>(thisOp->opcode())];
        return simplifier(std::move(thisOp));
    }

    void dump(int depth = 1, int indent = 0) const;
};

Expression Op::replaceRange(const OpPtr& p, const Range& newRange)
{
    if (newRange.min == newRange.max)
        return newRange.min;  // Return scalar
    else
    {
        p->m_range = newRange;
        return p;
    }
}

Expression Op::Inp(OpPtr&& opp)
{
    Op& op = *opp;
    if (op.m_operand1 < trialInputVals.size())
        return trialInputVals[op.m_operand1];
    else
        op.m_range = {1, 9};
    return opp;
}

Expression Op::Add(OpPtr&& opp)
{
    const Expression& a = opp->operand1();
    const Expression& b = opp->operand2();
    if (Expression::zero == a)
        return b;
    else if (Expression::zero == b)
        return a;
    else if (a.isInt() and b.isInt())
        return a.asInt() + b.asInt();

    auto [minA, maxA] = a.range();
    auto [minB, maxB] = b.range();
    return replaceRange(opp, { minA + minB, maxA + maxB });
}

Expression Op::Mul(OpPtr&& opp)
{
    const Expression& a = opp->operand1();
    const Expression& b = opp->operand2();
    if (a.isInt() && b.isInt())
        return a.asInt() * b.asInt();
    else if (Expression::zero == a || Expression::zero == b)
        return Expression::zero;
    else if (Expression::one == a)
        return b;
    else if (Expression::one == b)
        return a;
    auto [minA, maxA] = a.range();
    auto [minB, maxB] = b.range();
    int minR = std::min({minA*minB, minA*maxB, maxA*minB, maxA*maxB});
    int maxR = std::max({minA*minB, minA*maxB, maxA*minB, maxA*maxB});
    return replaceRange(opp, { minR, maxR });
}

Expression Op::Div(OpPtr&& opp)
{
    const Expression& a = opp->operand1();
    const Expression& b = opp->operand2();
    if (a.isInt() && b.isInt())
        return div(a, b);
    else if (Expression::zero == a)
        return Expression::zero;
    else if (a == b)
        return 1;

    auto [minA, maxA] = a.range();
    auto [minB, maxB] = b.range();

    if (0 == minB) minB =  1;  // No divide by zero
    if (0 == maxB) maxB = -1;  // No divide by zero
    if (1 == minB && 1 == maxB)
        return a;

    int minR = std::min({div(minA, minB), div(minA, maxB),
            div(maxA, minB), div(maxA, maxB)});
    int maxR = std::max({div(minA, minB), div(minA, maxB),
            div(maxA, minB), div(maxA, maxB)});
    if (minR == maxR) return minR;  // Convert to scalar?
    return replaceRange(opp, { minR, maxR });
}

Expression Op::Mod(OpPtr&& opp)
{
    const Expression& a = opp->operand1();
    const Expression& b = opp->operand2();
    if (a.isInt() && b.isInt())
        return a.asInt() % b.asInt();
    else if (Expression::zero == a)
        return Expression::zero;
    else if (a == b)
        return 0;

    auto [minA, maxA] = a.range();
    auto [minB, maxB] = b.range();

    if (minA < 0) minA = 0;  // Guaranteed no negative values
    if (minB < 1) minB = 1;  // Guaranteed no values < 1

    if (0 == minA && 0 == maxA)
        return Expression::zero;
    else if (1 == maxB)
        return Expression::zero;
    else if (maxA < minB)
        return a;
    else
        return replaceRange(opp, { 0, std::min(maxA, maxB - 1) });
}

Expression Op::Eql(OpPtr&& opp)
{
    const Expression& a = opp->operand1();
    const Expression& b = opp->operand2();

    if (a == b)
        return 1;
    else if (a.isInt() && b.isInt())
        return a.asInt() == b.asInt();

    auto [minA, maxA] = a.range();
    auto [minB, maxB] = b.range();

    if (minB > maxA || minA > maxB)
        return 0;  // No overlap, cannot be equal
    if (minA == 0 && maxA == 1)
    {
        // `a` is Boolean
        if (Expression::zero == b)
            // `a == 0` is equivalent to `not a`
            return Not(std::make_shared<Op>(Opcode::Not, a, Range{ 0, 1 }));
        else if (Expression::one == b)
            // `a == 1` is equivalent to `a`
            return a;
    }
    else if (minB == 0 && maxB == 1)
    {
        // `b` is Boolean
        if (Expression::zero == a)
            // `0 == b` is equivalent to `not b`
            return Not(std::make_shared<Op>(Opcode::Not, b, Range{ 0, 1 }));
        else if (Expression::one == a)
            // `1 == b` is equivalent to `b`
            return b;
    }

    return replaceRange(opp, { 0, 1 });
}

// `Not` is a synthetic opcode, not found directly in the input file.
Expression Op::Not(OpPtr&& opp)
{
    const Expression& a = opp->operand1();
    if (a.isInt())
        return 1 - a;  // Negate Boolean value expressed as an `int`
    else if (a->opcode() == Opcode::Not)
        return a->operand1();  // Double negation
    else
        return replaceRange(opp, { 0, 1 });
}

const Op::StepSimplifier Op::s_simplifiers[(std::size_t) Opcode::NumOpcodes] {
    Op::Inp, Op::Add, Op::Mul, Op::Div, Op::Mod, Op::Eql, Op::Not
};

void Op::dump(int depth, int indent) const
{
    static constexpr char spaces[]= "                                        "
                                    "                                        ";

    constexpr int maxIndent = sizeof(spaces) - 1;
    if (indent > maxIndent)
        indent = maxIndent;

    const char* indentStr = spaces + maxIndent - indent;
    std::cout << indentStr << range() << " = " << name();
    if (depth < 1)
        return;

    std::cout << '(';
    m_operand1.dump(0);
    if (! m_operand2.isNull())
    {
        std::cout << ", ";
        m_operand2.dump(0);
    }
    std::cout << ")\n";
    if (depth < 2)
        return;

    m_operand1.dump(depth - 1, indent + 2);
    if (! m_operand2.isNull())
        m_operand2.dump(depth - 1, indent + 2);
}

inline Range Expression::range() const
{
    assert(! isNull());
    if (isInt())
        return { asInt(), asInt() };
    else
        return asOp()->range();
}

Expression Expression::simplify() const
{
    if (! isOp())
        return *this;

    OpPtr opp = asOp();
    Opcode     opcode   = opp->opcode();
    Expression operand1 = opp->operand1().simplify();  // Recursively simplify
    Expression operand2 = opp->operand2().simplify();  // Recursively simplify
    if (opcode != Opcode::Inp)
    {
        if (operand1 == opp->operand1() && operand2 == opp->operand2())
            return *this;
    }

    OpPtr newOpp = std::make_shared<Op>(opcode, operand1, operand2, range());
    return Op::simplifyStep(newOpp);
}

void Expression::dump(int depth, int indent) const
{
    static constexpr char spaces[]= "                                        "
                                    "                                        ";

    if (isNull())
        return;
    else if (isInt())
    {
        constexpr int maxIndent = sizeof(spaces) - 1;
        if (indent > maxIndent)
            indent = maxIndent;

        const char* indentStr = spaces + maxIndent - indent;
        std::cout << indentStr << asInt();
        if (depth > 0) std::cout << '\n';
    }
    else
        asOp()->dump(depth, indent);
}

using RegisterSet = std::array<Expression, 4>;

// Parse and process the specified instruction, modifying the
// registers. Processing involves updating the instruction tree for a register.
// No I/O actually occurs.
void processInstr(RegisterSet& registers, const std::string& line)
{
    static int inputCount = 0;  // Which input is next

    std::string_view opcodeName(line.data(), 3);
    Opcode opcode = nameToOpcode(opcodeName);
    int registerId = line[4] - 'w';

    OpPtr opp;
    if (Opcode::Inp == opcode)
    {
        opp = std::make_shared<Op>(opcode, ++inputCount, Range{1, 9});
    }
    else {
        Expression operand1(registers[registerId]);
        Expression operand2;
        if ('w' <= line[6] && line[6] <= 'z')
            operand2 = registers[line[6] - 'w'];
        else
            operand2 = std::atoi(line.c_str() + 6);
        opp = std::make_shared<Op>(opcode, operand1, operand2, fullRange);
    }

    registers[registerId] = Op::simplifyStep(std::move(opp));
}

std::vector<int> solve(const Expression& expression)
{
    if (trialInputVals.size() > 14)
        return trialInputVals;  // Solved!

    for (int i = 9; i > 0; --i)
    {
        trialInputVals.push_back(i);
        Expression simplifiedExpr = expression.simplify();
        auto [minE, maxE] = simplifiedExpr.range();
        if (minE <= 0 && 0 <= maxE)
        {
            // Found partial solution, recurse down another level.
            if (trialInputVals.size() < 9)
            {
                std::cout << "\rPartial = ";
                for (int x = 1; x < 15; ++x) {
                    if (x < trialInputVals.size())
                        std::cout << trialInputVals[x];
                    else
                        std::cout << ' ';
                }
                std::cout << std::flush;
                auto solution = solve(simplifiedExpr);
                if (! solution.empty()) return solution;
            }
        }
        trialInputVals.pop_back();
    }

    return {};  // Solution not found
}

}  // Close unnamed namespace

int main()
{
    std::ifstream infile("puzzle24_input.txt");

    RegisterSet registers{ 0, 0, 0, 0 };;
    std::string line;
    while (std::getline(infile, line))
        processInstr(registers, line);

    std::cout << "Input processed, solving..." << std::endl;

    registers.back().dump(4);

    // auto solution = solve(registers.back());
    // std::cout << "\nSolution = ";
    // for (auto i = solution.begin() + 1; i != solution.end(); ++i)
    //     std::cout << *i;
    // std::cout << std::endl;
}
