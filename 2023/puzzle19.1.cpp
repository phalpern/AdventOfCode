// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT
#include <aoc_util.h>
#include <vector>
#include <unordered_map>

using namespace aoc;

constexpr auto npos = std::string_view::npos;

enum Category {
  CAT_x, CAT_m, CAT_a, CAT_s, CAT_none, CAT_max = CAT_none
};

using PartRatings = std::array<int, CAT_max>;

std::ostream& printPartRatings(const PartRatings& pr)
{
  for (int i = 0; i < pr.size(); ++i)
    std::cout << (0 == i ? '{' : ',') << "xmas"[i] << '=' << pr[i];
  return std::cout << '}';
}

struct Op
{
  enum OpCode { ALWAYS_TRUE, LT, GT };

  OpCode      m_opCode;
  Category    m_operand1;
  int         m_operand2;
  std::string m_target;

  // Return target if operation returns true, else return an empty string.
  const std::string& apply(const PartRatings& pr) const;

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

const std::string& Op::apply(const PartRatings& pr) const
{
  static const std::string emptyStr{};

  switch (m_opCode)
  {
   case ALWAYS_TRUE: return m_target;
   case LT: if (pr[m_operand1] < m_operand2) return m_target; break;
   case GT: if (pr[m_operand1] > m_operand2) return m_target; break;
  }

  return emptyStr;
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

PartRatings parseRatings(std::string_view line)
{
  PartRatings ret;

  ASSERT(line[0] == '{');
  line.remove_prefix(1);
  for (int i = 0; i < CAT_max; ++i)
  {
    ASSERT(line[0] == "xmas"[i] && line[1] == '=');
    auto delim = line.find_first_of(",}");
    ASSERT(npos != delim);
    ret[i] = strviewToInt(line.substr(2, delim - 2));
    line.remove_prefix(delim + 1);
  }

  ASSERT(line.empty());
  return ret;
}

[[noreturn]] void unreachable()
{
  ASSERT(false && "unreachable");
  std::abort();
}

const std::string& processWorkflow(const Workflow& wf, const PartRatings& pr)
{
  for (const auto& op : wf)
  {
    const std::string& target = op.apply(pr);
    if (! target.empty())
      return target;
  }

  unreachable();
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

  std::vector<PartRatings> ratings;
  for (auto line : ibl)
  {
    ratings.push_back(parseRatings(line));
    DEBUG2(printPartRatings(ratings.back()) << '\n');
  }
  DEBUG2(std::cout << '\n');

  int64 result = 0;
  int   numAccepted = 0;

  for (const auto& part : ratings)
  {
    DEBUG(printPartRatings(part) << ": ");

    std::string wfName = "in";
    while (wfName != "A" && wfName != "R")
    {
      DEBUG(std::cout << wfName << " -> ");
      wfName = processWorkflow(workFlows[wfName], part);
    }
    DEBUG(std::cout << wfName);
    int64 sum = 0;
    if (wfName == "A")
    {
      ++numAccepted;
      sum = part[CAT_x] + part[CAT_m] + part[CAT_a] + part[CAT_s];
    }
    DEBUG(std::cout << '(' << sum << ")\n");
    result += sum;
  }

  std::cout << numAccepted << " parts accepted";
  std::cout << "\nresult = " << result << "\n\n";
}
