// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT
#include <aoc_util.h>
#include <utility>
#include <algorithm>
#include <span>
#include <string>
#include <unordered_map>

using namespace aoc;

class Platform
{
  std::string m_array;
  int         m_ncols;

public:
  int rows() const { return m_array.size() / m_ncols; }
  int cols() const { return m_ncols; }

  void addRow(const std::string& row)
  {
    if (m_array.empty())
      m_ncols = row.size();
    m_array += row;
  }

  std::span<char> operator[](int r)
    { return { &m_array[r * m_ncols], std::size_t(m_ncols) }; }
  std::span<const char> operator[](int r) const
    { return { &m_array[r * m_ncols], std::size_t(m_ncols) }; }

  const std::string& asString() const { return m_array; }

  friend std::ostream& operator<<(std::ostream& os, const Platform& plat)
  {
    for (std::size_t i = 0; i < plat.m_array.size(); i += plat.m_ncols)
      os << std::string_view(plat.m_array.data() + i, plat.m_ncols) << '\n';
    return os;
  }
};

enum Dir { NORTH, SOUTH, WEST, EAST };

class RotatedPlatform
{
  struct RotMatrix {
    // These elements of the rotation matrix are broken out and given names.
    int m_hiRowMul,  m_hiColMul;
    int m_loRowMul,  m_loColMul;
    int m_rowOffset, m_colOffset;
  };

  // One matrix for each possible rotation
  static const RotMatrix s_rotations[4];

  Platform& m_plat;
  RotMatrix m_rot;

  // Shape of traversal space
  int m_hiDim, m_loDim;

public:
  RotatedPlatform(Platform& plat, Dir rotation);

  char& operator()(int hi, int lo);
  char  operator()(int hi, int lo) const;

  int hiDim() const { return m_hiDim; }
  int loDim() const { return m_loDim; }
};

const RotatedPlatform::RotMatrix RotatedPlatform::s_rotations[4] = {
  {  1,  0,
     0,  1,
     0,  0 },  // NORTH  (0 degree rotation)
  { -1,  0,
     0, -1,
     1,  1 },  // SOUTH  (180 degree rotation)
  {  0,  1,
    -1,  0,
     1,  0 },  // WEST   (90 degree clockwise rotation)
  {  0, -1,
     1,  0,
     0,  1 }   // EAST   (90 degree counterclockwise rotation)
};

RotatedPlatform::RotatedPlatform(Platform& plat, Dir rotation)
  : m_plat(plat), m_rot(s_rotations[rotation])
  , m_hiDim(plat.rows()), m_loDim(plat.cols())
{
  if (rotation > SOUTH)
    std::swap(m_hiDim, m_loDim);

  if (m_rot.m_rowOffset)
    m_rot.m_rowOffset = plat.rows() - 1;
  if (m_rot.m_colOffset)
    m_rot.m_colOffset = plat.cols() - 1;
}

char& RotatedPlatform::operator()(int hi, int lo)
{
  int row = hi*m_rot.m_hiRowMul + lo*m_rot.m_loRowMul + m_rot.m_rowOffset;
  int col = hi*m_rot.m_hiColMul + lo*m_rot.m_loColMul + m_rot.m_colOffset;

  return m_plat[row][col];
}

char RotatedPlatform::operator()(int hi, int lo) const
{
  int row = hi*m_rot.m_hiRowMul + lo*m_rot.m_loRowMul + m_rot.m_rowOffset;
  int col = hi*m_rot.m_hiColMul + lo*m_rot.m_loColMul + m_rot.m_colOffset;

  return m_plat[row][col];
}

void tilt(Platform& platform, Dir direction)
{
  RotatedPlatform rotPlat(platform, direction);

  for (int lo = 0; lo < rotPlat.loDim(); ++lo)
  {
    int nextSlot = 0;

    for (int hi = 0; hi < rotPlat.hiDim(); ++hi)
    {
      char& cell = rotPlat(hi, lo);
      if (cell == 'O')
      {
        std::swap(cell, rotPlat(nextSlot, lo));
        ++nextSlot;
      }
      else if (cell == '#')
        nextSlot = hi + 1;
    }
  }
}

void spin(Platform& platform, int64 n)
{
  // Map patterns that have been seen before to the rep count where they were
  // last seen.
  static std::unordered_map<std::string, int64> memos;

  // Increment occurs inside loop
  for (int64 i = 0; i < n; )
  {
    tilt(platform, NORTH);
    tilt(platform, WEST);
    tilt(platform, SOUTH);
    tilt(platform, EAST);

    ++i;  // Increment now to avoid memoizing zero

    int64& lastSeen = memos[platform.asString()];
    if (lastSeen == 0)
      lastSeen = i;
    else
    {
      // We've made a complete cycle from this pattern to the same pattern.  We
      // are guaranteed to continue seeing this pattern after the same number
      // of steps.
      auto cycleLen = i - lastSeen;
      std::cout << "Cycle length = " << cycleLen << std::endl;
      i = n - (n - i) % cycleLen;  // Fast forward as much as possible
      // Kill all other memos (which are obsolete, and record just this one
      memos.clear();
      memos[platform.asString()] = i;
    }
  }
}

int64 totalLoad(const Platform& platform)
{
  int64 result = 0;

  for (int col = 0; col < platform.cols(); ++col)
  {
    for (int row = 0; row < platform.rows(); ++row)
      if (platform[row][col] == 'O')
        result += (platform.rows() - row);
  }

  return result;
}

int main(int argc, char *argv[])
{
  Platform platform;

  auto input = openInput(argc, argv);
  for (auto line : InputByLine(input))
    platform.addRow(std::move(line));

  spin(platform, 1'000'000'000);

  std::cout << "Final platform:\n" << platform;

  std::cout << "total load = " << totalLoad(platform) << '\n' << std::endl;
}
