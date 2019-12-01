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

#include "Transmitter.h"
#include <string>
#include "AircraftPacket_m.h"

using namespace inet;
using namespace std;

namespace aeronauticalcommunicationsimulator {

Define_Module(Transmitter);

void Transmitter::initialize()
{

    nBS = par("nBS").intValue();
    k = getAncestorPar("k").doubleValue();
    int rows = getAncestorPar("rows").intValue();
    int cols = getAncestorPar("cols").intValue();
    int M = getAncestorPar("M").intValue();

    bsPositions = new Coord[nBS];

    // Reference to own mobility module
    mobility = reinterpret_cast<TurtleMobility*> ( getModuleByPath("^.mobility") );
//    EV<< mobility->getCurrentPosition()<<endl;

    for ( int i = 0; i < rows; i++ ) {
        for ( int j = 0; j < cols; j++ ) {
            bsPositions[i*rows+j].setX(M/2 + j*M);
            bsPositions[i*rows+j].setY(M/2 + i*M );
            EV<<"BS " << i*rows+j << " in position "<< bsPositions[i*rows+j]<<endl;
        }
    }
    scheduleAt( simTime(), new cMessage("Initialize"));
}

void Transmitter::handleMessage(cMessage *msg)
{
    AircraftPacket* ap = NULL;
    if ( msg->isSelfMessage() ) {
        if ( strcmp(msg->getName(), "Initialize") == 0 ) {
            connectedBS = getClosestBS();
            EV<<"Closest BS: " << connectedBS <<endl;
            ap =  new AircraftPacket("AircraftPacket");
            ap->setAircraftID(getIndex());
            ap->setCreationTime(0.0);
            scheduleAt(simTime() + k + uniform(0,0.5), ap ); // random offset to desynchronize aircratfs
        } else if ( strcmp(msg->getFullName(),"AircraftPacket") == 0 ) {

            ap = (AircraftPacket*) msg;
            ap->setCreationTime(simTime().dbl());
            EV<< "Sending to " << connectedBS <<endl;
            send(ap, "out", connectedBS);
            ap =  new AircraftPacket("AircraftPacket");
            ap->setAircraftID(getIndex());
            ap->setCreationTime(0.0);
            scheduleAt(simTime() + k, ap );
        }
    }

}

int Transmitter::getClosestBS() {
    Coord aircraftPosition = mobility->getCurrentPosition();
    double min = getAncestorPar("rows").intValue()*getAncestorPar("M").intValue();
    int closest;
    double distance;
    for ( int i = 0; i < nBS; i++ ) {
        distance = bsPositions[i].distance(aircraftPosition);
        EV<< "distance from " << i << " " << distance <<endl;
        if ( distance < min ) {
            min = distance;
            closest = i;
        }
    }
    return closest;
}

} //namespace
