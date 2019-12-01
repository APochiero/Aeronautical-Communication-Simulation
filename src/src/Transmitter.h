//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

#ifndef __AERONAUTICALCOMMUNICATIONSIMULATOR_TRANSMITTER_H_
#define __AERONAUTICALCOMMUNICATIONSIMULATOR_TRANSMITTER_H_

#include <omnetpp.h>
#include "inet/mobility/single/TurtleMobility.h"

using namespace omnetpp;

namespace aeronauticalcommunicationsimulator {

/**
 * TODO - Generated class
 */
class Transmitter : public cSimpleModule
{
  protected:
    virtual void initialize(int stage);
    virtual int numInitStages() const { return 11; }
    virtual void handleMessage(cMessage *msg);
  private:
    int nBS;
    int connectedBS;
    inet::TurtleMobility* mobility;
    inet::Coord* bsPositions;

    int getClosestBS();
};

} //namespace

#endif
