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

#include "Receiver.h"
#include "DiscoveryMessage_m.h"
using namespace inet;
namespace aeronauticalcommunicationsimulator {

Define_Module(Receiver);

void Receiver::initialize()
{
    // Reference to own mobility module
    mobility = check_and_cast<StaticGridMobility*> ( getModuleByPath("^.mobility") );
}

void Receiver::handleMessage(cMessage *msg)
{
    if ( strcmp(msg->getName(), "Discovery") == 0 ) {
        // Get own position and send back to the aircraft though the arrival gate
        DiscoveryMessage* disc = (DiscoveryMessage*) msg;
        inet::Coord position = mobility->getCurrentPosition();
        disc->setBsID(getIndex());
        disc->setX(position.getX());
        disc->setY(position.getY());
        send(disc, "in", msg->getArrivalGate()->getIndex());
    }
}

} //namespace
