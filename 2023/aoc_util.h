// aoc_util.h -- Utilities for Advent of Code challenges

#include <cstdlib>
#include <fstream>
#include <iostream>
#include <regex>
#include <string>

namespace aoc {

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

inline
std::ifstream openInput(int argc, char *argv[])
{
  std::string fname(argv[0]);
  auto puzzle = fname.find("puzzle");
  if (puzzle != std::string::npos)
  {
    auto dot = fname.find('.', puzzle);
    if (dot != std::string::npos)
      fname.resize(dot);
  }

  fname += '_';
  fname += argc > 1 ? argv[1] : "input";
  fname += ".txt";

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

}  // close namespace aoc

#define ASSERT(...) do { \
  bool c = __VA_ARGS__;  \
  if (! c) assertFail(__FILE__, __LINE__, #__VA_ARGS__); \
} while (false)

#ifdef DEBUGPRINT
# define DEBUG(...) do { __VA_ARGS__; } while (false)
#else
# define DEBUG(...) ((void) 0)
#endif
