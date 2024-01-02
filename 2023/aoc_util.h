// -*- mode: c++; c-basic-offset: 2 -*-

#include <cstdlib>
#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <regex>
#include <string>

#ifndef DEBUGPRINT
# define DEBUGPRINT 0
#elif (1 - DEBUGPRINT - 1) == 2  // if defined as blank
# undef DEBUGPRINT
# define DEBUGPRINT 1
#endif

# define DEBUG_N(LEVEL, ...) do { if (LEVEL <= DEBUGPRINT)       \
    { __VA_ARGS__; } } while(false)
#define DEBUG(...) DEBUG_N(1, __VA_ARGS__)
#define DEBUG2(...) DEBUG_N(2, __VA_ARGS__)
#define DEBUG3(...) DEBUG_N(3, __VA_ARGS__)

namespace aoc {

using int64  = long long;
using uint64 = unsigned long long;

template <class... Args>
inline void bail(const std::string& a0, const Args&... args)
{
  std::cerr << (a0 + ... + args) << std::endl;
  std::exit(1);
}

inline void assertFail(const char* file, int line, const char* expr)
{
  std::cerr << file << ':' << line << ": assertion failed: " << expr
            << std::endl;
  std::exit(1);
}

#define ASSERT(...) do { \
  if (false == (__VA_ARGS__)) assertFail(__FILE__, __LINE__, #__VA_ARGS__); \
} while (false)

inline
std::ifstream openInput(int argc, char *argv[])
{
  std::string fname(argv[0]);
  auto puzzle = fname.find("bin/puzzle");
  if (puzzle != std::string::npos)
  {
    // replace "bin/" with "input/"
    fname.replace(puzzle, 3, "input/");
    auto dot = fname.find('.', puzzle);
    if (dot != std::string::npos)
      fname.resize(dot);

    fname += '_';
    fname += argc > 1 ? argv[1] : "input";
    fname += ".txt";
  }
  else
  {
    ASSERT(argc > 1);
    fname = argv[1];
  }

  std::ifstream ret(fname);
  if (! ret)
    bail("Cannot open " + fname);

  return ret;
}

class InputLineIterator;
class InputLineSentinel { };

// Range to traverse an input file line-by-line
class InputByLine {
  std::istream& m_input;             // input stream
  std::string   m_current;           // look-ahead line
  bool          m_lookAhead = false; // true if look-ahead has occured

public:
  using iterator = InputLineIterator;
  using sentinel = InputLineSentinel;

  InputByLine(std::istream& is) : m_input(is) { } // implicit

  iterator begin();
  sentinel end()   { return {}; }

  const std::string& current()
  {
    if (! m_lookAhead)
    {
      m_current.clear();
      getline(m_input, m_current);
      m_lookAhead = ! m_input.fail();
    }
    return m_current;
  }

  void next() { if (! m_lookAhead) current(); m_lookAhead = false; }

  bool eof() { (void) current(); return m_input.fail(); }
};

// Iterator to traverse an input file line by line
class InputLineIterator {
  InputByLine* m_inputByLine;

public:
  explicit InputLineIterator(InputByLine *ibl) : m_inputByLine(ibl) { }

  const std::string& operator*()  const { return  m_inputByLine->current(); }
  const std::string* operator->() const { return &m_inputByLine->current(); }

  InputLineIterator& operator++() { m_inputByLine->next(); return *this; }

  friend bool operator==(const InputLineIterator& i, InputLineSentinel)
    { return i.m_inputByLine->eof(); }
};

inline InputLineIterator InputByLine::begin()
{
  m_lookAhead = false;
  (void) current();
  return iterator{this};
}

// Return the entire contents of the input stream as a string.
// Assumes that file doesn't contain an 0xff character.
std::string slurp(std::istream& is)
{
  std::string ret;
  getline(is, ret, '\xff');
  return ret;
}

// Read a vector of integers from `s`.  If `prefix` is not empty, it must match
// the start of the line, before the first integer to be read.
template <class INT_TYPE = int>
std::vector<INT_TYPE> parseNumbers(std::string_view s,
                                   std::string_view prefix = "")
{
  // Test and remove prefix
  ASSERT(s.substr(0, prefix.length()) == prefix);
  s.remove_prefix(prefix.length());

  std::istringstream is(std::string{s});

  std::vector<INT_TYPE> ret;
  INT_TYPE v = 0;
  while (! (is >> v).fail())
    ret.push_back(v);

  return ret;
}

// Parse the specified string view as an integral value
int64 strviewToInt(std::string_view s, int radix = 0)
{
  char *end;
  int64 result = strtoll(s.data(), &end, radix);
  ASSERT(end <= &*s.end());

  return result;
}

// Read a vector of integers from a single line in `is`.  If `prefix` is not
// empty, it must match the start of the line, before the first integer to be
// read.
template <class INT_TYPE = int>
std::vector<INT_TYPE> parseNumbers(std::istream&    is,
                                   std::string_view prefix = "")
{
  std::string str;
  getline(is, str);
  ASSERT(! is.fail());
  return parseNumbers<INT_TYPE>(str, prefix);
}

template <class Item>
std::ostream& printItem(std::ostream& os, const Item& v)
{
  return os << v;
}

template <class Key, class Val>
std::ostream& printItem(std::ostream& os, const std::pair<Key, Val>& p)
{
  return os << '(' << p.first << ", " << p.second << ')';
}

template <class Container>
std::ostream& printContainer(std::ostream& os, const Container& c,
                             std::string_view separator = " ")
{
  for (auto&& item : c)
    printItem(os, item) << separator;
  return os;
}

}  // close namespace aoc
