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
    virtual void initialize();
    virtual void handleMessage(cMessage *msg);
  private:
    int nBS;
    int connectedBS;
    double k;
    double t;
    double T;
    bool transmitting;

    inet::TurtleMobility* mobility;
    inet::Coord* bsPositions;
    cPacketQueue queue;

    int getClosestBS();
    void handleInitialize(cMessage* msg);
    void handlePacketArrival(cMessage* msg);
    void handleCheckHandover(cMessage* msg);
    void handlePacketSent(cMessage* msg);
    void sendPacket(cPacket* pkt);
};

} //namespace

#endif
