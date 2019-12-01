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
#include "DiscoveryMessage_m.h"
#include <string>

using namespace inet;
using namespace std;

namespace aeronauticalcommunicationsimulator {

Define_Module(Transmitter);

void Transmitter::initialize(int stage)
{
    nBS = par("nBS").intValue();
    bsPositions = new Coord[nBS];

    // Reference to own mobility module
    mobility = check_and_cast<TurtleMobility*> ( getModuleByPath("^.mobility") );
//    EV<< mobility->getCurrentPosition()<<endl;

    DiscoveryMessage* msg = new DiscoveryMessage("Discovery");
    // BS position discovery request
    for ( int i = 0; i < nBS; i++ ) {
        send(msg, "out", i);
    }
}

void Transmitter::handleMessage(cMessage *msg)
{
    if ( strcmp(msg->getName(), "Discovery") == 0 ) {
        // Get bs position and store it into bsPositions vector
        DiscoveryMessage* disc = (DiscoveryMessage*) msg;
        bsPositions[disc->getBsID()].setX(disc->getX());
        bsPositions[disc->getBsID()].setY(disc->getY());
    }
}

int Transmitter::getClosestBS() {
    Coord aircraftPosition = mobility->getCurrentPosition();
    double max = 0;
    int closest;
    double distance;
    for ( int i = 0; i < nBS; i++ ) {
        distance = bsPositions[i].distance(aircraftPosition);
        if ( distance > max ) {
            max = distance;
            closest = i;
        }
    }
    return closest;
}

} //namespace
