// -*- mode: c++; c-basic-offset: 2 -*-

#include <cstdlib>
#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <regex>
#include <string>

#ifdef DEBUGPRINT
# define DEBUG(...) do { __VA_ARGS__; } while (false)
#else
# define DEBUG(...) ((void) 0)
#endif

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
    // Strip off "bin/"
    fname.erase(fname.begin() + puzzle, fname.begin() + puzzle + 4);
    auto dot = fname.find('.', puzzle);
    if (dot != std::string::npos)
      fname.resize(dot);

    fname = "input/" + fname;
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

class InputLineSentinel { };

// Iterator to traverse an input file line by line
class InputLineIterator {
  std::istream& m_input;
  std::string   m_current;

public:
  explicit InputLineIterator(std::istream& is) : m_input(is)
    { getline(is, m_current); }

  const std::string& operator*() const { return m_current; }
  const std::string* operator->() const { return &m_current; }

  InputLineIterator& operator++()
    { m_current.clear(); getline(m_input, m_current); return *this; }
  InputLineIterator operator++(int) { auto tmp(*this); ++*this; return tmp; }

  friend bool operator==(const InputLineIterator& i, InputLineSentinel)
    { return i.m_current.empty() && i.m_input.eof(); }
};

// Range to traverse an input file line-by-line
class InputByLine {
  std::istream& m_input;
public:
  using iterator = InputLineIterator;
  using sentinel = InputLineSentinel;

  InputByLine(std::istream& is) : m_input(is) { } // implicit

  iterator begin() { return iterator{m_input}; }
  sentinel end()   { return {}; }
};

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
std::ostream& printContainer(std::ostream& os, const Container& c)
{
    for (auto&& item : c)
        printItem(os, item) << ' ';
    return os;
}

}  // close namespace aoc