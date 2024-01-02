// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT
#include <aoc_util.h>
#include <vector>
#include <unordered_map>
#include <set>

using namespace aoc;

constexpr auto npos = std::string_view::npos;

enum Category {
  CAT_x, CAT_m, CAT_a, CAT_s, CAT_none, CAT_max = CAT_none
};

struct RatingRange
{
  // Range is the half-open interval [start, finish).  If start is 0, the range
  // is considered empty.
  int start  = 1;
  int finish = 4001;

  bool isEmpty() const { return 0 == start || start == finish; }
  int64 rangeSize() const { return finish - start; }

  friend std::strong_ordering
  operator<=>(const RatingRange&, const RatingRange&) = default;
};

using PartRatings = std::array<RatingRange, CAT_max>;

constexpr PartRatings emptyPartRatings{
  RatingRange{0,0}, RatingRange{0,0}, RatingRange{0,0}, RatingRange{0,0}
};

inline bool isEmptyPart(const PartRatings& pr) { return pr[0].isEmpty(); }

std::ostream& printPartRatings(const PartRatings& pr)
{
  for (int i = 0; i < pr.size(); ++i)
    std::cout << (0 == i ? "{ " : ", ") << "xmas"[i] << " = ("
              << pr[i].start << ", " << pr[i].finish << ')';
  return std::cout << " }";
}

const std::string accepted("A");
const std::string rejected("R");

struct Op
{
  enum OpCode { ALWAYS_TRUE, LT, GT };

  OpCode      m_opCode;
  Category    m_operand1;
  int         m_operand2;
  std::string m_target;

  // Compute the subset of of `pr` for which the operation would be true.
  // Modifies `pr` to the reflect range of values for which the operation would
  // be false and sets `jumpPr` to the range of values for which the operation
  // would be true.  Returns the name of the workflow to jump to on true, or
  // "A" or "R" for accept or rejecting the part.
  const std::string& apply(PartRatings& pr, PartRatings& jumpPr) const;

  friend std::ostream& operator<<(std::ostream& os, const Op& op)
  {
    char opSym = '\0';
    switch (op.m_opCode)
    {
     case ALWAYS_TRUE: return os << op.m_target;
     case LT: opSym = '<'; break;
     case GT: opSym = '>'; break;
    }

    return os << "xmas"[op.m_operand1] << opSym << op.m_operand2
              << ':' << op.m_target;
  }
};

const std::string& Op::apply(PartRatings& pr, PartRatings& jumpPr) const
{
  jumpPr = pr;

  switch (m_opCode)
  {
   case ALWAYS_TRUE:
    pr = emptyPartRatings;
    return m_target;

   case LT:
   {
     auto ceiling = m_operand2;
     jumpPr[m_operand1].finish = std::min(jumpPr[m_operand1].finish, ceiling);
     pr[m_operand1].start      = std::max(pr[m_operand1].start, ceiling);
     break;
   }

   case GT:
   {
     auto floor = m_operand2 + 1;
     jumpPr[m_operand1].start = std::max(jumpPr[m_operand1].start, floor);
     pr[m_operand1].finish    = std::min(pr[m_operand1].finish, floor);
     break;
   }
  }

  if (jumpPr[m_operand1].isEmpty())
    jumpPr = emptyPartRatings;

  if (pr[m_operand1].isEmpty())
    pr = emptyPartRatings;

  return m_target;
}

Op parseOp(std::string_view s)
{
  constexpr std::string_view categoryChars = "xmas";

  auto colon = s.find(':');
  if (colon == npos)
    return { Op::ALWAYS_TRUE, CAT_none, 0, std::string(s) };

  Op result;
  auto op1 = categoryChars.find(s[0]);
  ASSERT(op1 != npos);
  result.m_operand1 = Category(op1);

  if (s[1] == '<')
    result.m_opCode = Op::LT;
  else
  {
    ASSERT(s[1] == '>');
    result.m_opCode = Op::GT;
  }

  result.m_operand2 = strviewToInt(s.substr(2, colon - 2));

  result.m_target = s.substr(colon + 1);

  return result;
}

using Workflow = std::vector<Op>;
using RuleMap  = std::unordered_map<std::string, Workflow>;
using Rule     = RuleMap::value_type;

Rule parseRule(std::string_view line)
{
  auto delim = line.find('{');
  ASSERT(delim != npos);
  auto name = line.substr(0, delim);
  line.remove_prefix(delim + 1);

  Workflow ops;
  while (! line.empty())
  {
    delim = line.find_first_of(",}");
    ASSERT(delim != npos);

    ops.push_back(parseOp(line.substr(0, delim)));
    line.remove_prefix(delim + 1);
  }

  return Rule{ name, std::move(ops) };
}

std::ostream& printRule(const Rule& rule)
{
  std::cout << rule.first;
  char delim = '{';
  for (const auto& op : rule.second)
  {
    std::cout << delim << op;
    delim = ',';
  }

  return std::cout << '}';
}

[[noreturn]] void unreachable()
{
  ASSERT(false && "unreachable");
  std::abort();
}

const void processWorkflow(const RuleMap& rmap, const std::string& wfName,
                           PartRatings pr,
                           std::set<PartRatings>& acceptedParts,
                           int depth = 0)
{
  DEBUG(printPartRatings(pr) << " -> " << wfName << '\n');

  if (acceptedParts.size() < depth)
  {
    DEBUG(std::cout << "Detected infinite recursion\n");
    return;  // infinite recursion detected, pr is not a valid input
  }

  const Workflow& wf = rmap.find(wfName)->second;
  for (const auto& op : wf)
  {
    PartRatings jumpPr;
    const std::string& target = op.apply(pr, jumpPr);

    if (isEmptyPart(jumpPr))
      ; // Discard jumpPr
    else if (accepted == target)
      acceptedParts.insert(jumpPr);
    else if (rejected != target)
      // Recursively
      processWorkflow(rmap, target, jumpPr, acceptedParts);

    if (pr.empty())
      break;
  }
}

int main(int argc, char *argv[])
{
  auto input = openInput(argc, argv);
  InputByLine ibl(input);

  RuleMap workFlows;
  for (auto line : ibl)
  {
    if (line.empty()) break;
    auto rule = parseRule(line);
    DEBUG2(printRule(rule) << '\n');
    workFlows.insert(std::move(rule));
  }
  DEBUG2(std::cout << '\n');

  int64 result = 0;

  std::set<PartRatings> acceptedParts;

  processWorkflow(workFlows, "in", {}, acceptedParts);

  std::cout << acceptedParts.size() << " parts accepted";

  for (const auto& part : acceptedParts)
  {
    int64 partCombos = 1;
    for (auto rateRange : part)
      partCombos *= rateRange.rangeSize();
    result += partCombos;
  }

  std::cout << "\nresult = " << result << "\n\n";
}
