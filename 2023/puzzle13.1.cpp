// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT
#include <aoc_util.h>

using namespace aoc;

// Avoid `vector<bool>` weirdness
enum Boolean : bool { False = false, True = true };

// Represent a single row or column of a pattern
class Slice
{
  const std::vector<Boolean>& m_array;
  int                         m_start;
  int                         m_size;
  int                         m_stride;

public:
  Slice(const std::vector<Boolean>& array,
        int                         start,
        int                         sz,
        int                         stride)
    : m_array(array), m_start(start), m_size(sz), m_stride(stride)
    { ASSERT(start + (sz - 1) * stride < array.size()); }

  int size() const { return m_size; }

  Boolean operator[](int idx) const
    { ASSERT(idx < m_size); return m_array[m_start + m_stride * idx]; }

  friend bool operator==(const Slice& a, const Slice& b)
  {
    if (a.size() != b.size())
      return false;

    for (int i = 0; i < a.size(); ++i)
      if (a[i] != b[i])
        return false;

    return true;
  }
};

class Pattern
{
  std::vector<Boolean> m_array;
  int          m_ncols;

public:
  void clear() { m_array.clear(); m_ncols = 0; }

  void addRow(std::string_view rowAsStr);

  int cols() const { return m_ncols; }
  int rows() const { return m_array.size() / m_ncols; }

  bool get(int r, int c) const { return m_array[r * m_ncols + c]; }
  bool operator()(int r, int c) { return get(r, c); }

  Slice getRow(int r) const { return { m_array, r * cols(), cols(), 1      }; }
  Slice getCol(int c) const { return { m_array, c         , rows(), cols() }; }
};

void Pattern::addRow(std::string_view rowAsStr)
{
  if (m_array.empty())
    m_ncols = rowAsStr.size();
  else
    ASSERT(rowAsStr.size() == m_ncols);

  for (auto c : rowAsStr)
    m_array.push_back(c == '#' ? True : False);
}

template <class GetSlice>
int findReflection(int n, GetSlice&& gs)
{
  for (int refLine = 1; refLine < n; ++refLine)
  {
    for (int a = refLine - 1, b = refLine; ; --a, ++b)
    {
      if (a < 0 || b >= n)
        return refLine;
      Slice sa = gs(a);
      Slice sb = gs(b);
      if (sa != sb)
        break;  // refLine is not the line of reflection
    }
  }

  return 0;  // No line of reflection
}

int64 computeReflections(const Pattern& pat)
{
  auto rowReflection = findReflection(pat.rows(),
                                      [&pat](int i){ return pat.getRow(i); });
  auto colReflection = findReflection(pat.cols(),
                                      [&pat](int i){ return pat.getCol(i); });

  // Only one line of reflection should exist
  ASSERT(! rowReflection || ! colReflection);

  return 100 * rowReflection + colReflection;
}

int main(int argc, char *argv[])
{
  int64 result = 0;

  Pattern currPattern;

  auto input = openInput(argc, argv);
  for (auto line : InputByLine(input))
  {
    if (line.empty())
    {
      result += computeReflections(currPattern);
      currPattern.clear();
    }
    else
      currPattern.addRow(line);
  }

  result += computeReflections(currPattern);

  std::cout << "result = " << result << std::endl;
}
