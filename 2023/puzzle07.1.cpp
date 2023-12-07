// -*- mode: c++; c-basic-offset: 2 -*-

// #define DEBUGPRINT
#include <aoc_util.h>
#include <array>
#include <algorithm>

using namespace aoc;

using Card = unsigned char;
using Hand = std::array<Card, 5>;

enum HandType {
  HighCard, OnePair, TwoPair, ThreeKind, FullHouse, FourKind, FiveKind
};

Card toCard(char v)
{
  switch (v)
  {
   case 'A' : return 14;
   case 'K' : return 13;
   case 'Q' : return 12;
   case 'J' : return 11;
   case 'T' : return 10;
  }

  ASSERT(std::isdigit(v));
  return v - '0';
}

Hand toHand(const std::string& handStr)
{
  Hand ret;

  int idx = 0;
  for (char c : handStr)
  {
    ASSERT(idx < 5);
    ret[idx++] = toCard(c);
  }

  return ret;
}

std::string toString(Hand h)
{
  constexpr char toChar[] = "__23456789TJQKA";
  std::string ret;
  for (Card c : h)
  {
    ASSERT(1 < c && c < 15);
    ret.push_back(toChar[c]);
  }

  ASSERT(ret.length() == 5);
  return ret;
}

HandType toHandType(Hand h)
{
  std::sort(h.begin(), h.end());

  Card prev = 0;
  int reps = 1;
  std::array repArray{ 0, 0, 0, 0, 0, 0 };
  for (Card c : h)
  {
    if (c == prev)
      ++reps;
    else if (reps > 1)
    {
      ++repArray[reps];
      reps = 1;
    }
    prev = c;
  }

  if (reps > 0)
    ++repArray[reps];

  if (repArray[5])
    return FiveKind;
  else if (repArray[4])
    return FourKind;
  else if (repArray[3])
    if (repArray[2])
      return FullHouse;
    else
      return ThreeKind;
  else if (2 == repArray[2])
    return TwoPair;
  else if (1 == repArray[2])
    return OnePair;
  else
    return HighCard;
}

// Return the value of a hand as a single interger.  This function produces a
// total ordering of hands.
int computeHandValue(Hand h)
{
  int result = (int) toHandType(h);
  DEBUG(std::cout << toString(h) << " has hand type " << result << std::endl);

  // Represent with one card per nibble.  Display in hex for best results.
  for (Card c : h)
    result = result * 16 + c;

  return result;
}

struct BidRecord
{
  Hand hand;
  int  bid;
  int  handValue;

  BidRecord(Hand h, int b)
    : hand(h), bid(b), handValue(computeHandValue(h)) { }

  friend int operator<=>(const BidRecord& a, const BidRecord& b)
  {
    return (a.handValue < b.handValue ? -1 :
            b.handValue < a.handValue ? 1 : 0);
  }
};

int main(int argc, char *argv[])
{
  int result = 0;

  auto input = openInput(argc, argv);

  std::vector<BidRecord> bids;
  while (input.good())
  {
    std::string cards;
    int         bid;

    input >> cards >> bid;
    if (input.fail())
      break;

    bids.push_back({toHand(cards), bid});
  }

  // Sort by ascending rank
  std::sort(bids.begin(), bids.end());

  auto rank = 0;
  for (const auto& bp : bids)
  {
    ++rank;  // Start counting at 1
    DEBUG(std::cout << rank << ": " << toString(bp.hand) << ' '
          << bp.bid << ' ' << std::hex << bp.handValue << std::dec
          << std::endl);
    result += rank * bp.bid;
  }

  std::cout << "result = " << result << std::endl;
}
